import os, json, requests, base64, pdfkit
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.paginator import Paginator
from django.core.exceptions import ImproperlyConfigured
from django.db.models import (F, Q, Sum, ExpressionWrapper, DecimalField, Subquery,
	OuterRef, Min, DateTimeField)
from django.db.models.functions import ExtractDay
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from .correo import enviarCorreo
from .forms import *
from .funciones import (CodGeneracion, Correlativo, getUrl, genJson, genQr, genPdf,
	CantLetras, firmar, datosInicio, gen_prueba, subirArchivo, BitacoraDTE)
from .models import (Empresa, DTECliente, DTEClienteDetalle, DTEClienteDetalleTributo,
	DtesEmpresa, TipoDocumento, Cliente, TributoResumen, Producto, Configuracion, 
	TipoInvalidacion, DTEInvalidacion, EstadoDTE, TipoAccionUsuario, BitacoraAccionDte)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework import status
from wkhtmltopdf.views import PDFTemplateView
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from itertools import chain

from unittest.mock import Mock


if os.name == 'posix':
	wkhtml_to_pdf = os.path.join(settings.BASE_DIR, "wkhtmltopdf")
else:
	wkhtml_to_pdf = os.path.join(settings.BASE_DIR, "wkhtmltopdf.exe")

## Para actualizacion ##
@login_required(login_url='manager:login')
def index(request):
	config = Configuracion.objects.all().first()
	request.session['empresa'] = request.user.userprofile.empresa.codigo
	datos_empresa = get_object_or_404(Empresa, codigo=request.user.userprofile.empresa.codigo)
	#request.session['empresa_nombre'] = request.user.userprofile.empresa.nombreComercial
	request.session['logo'] = config.blobUrl + 'empresas/logos/' + request.user.userprofile.empresa.codigo + '_logo.png'
	#request.session['logo'] = os.path.join(settings.STATIC_DIR, 'clientes', 'logos', request.user.userprofile.empresa.codigo + '_logo.png')
	#messages.success(request, request.session['logo'])
	
	list_docs = DtesEmpresa.objects.filter(empresa=request.session['empresa']).order_by('dte')
	documentos = list_docs.select_related('dte').values('id', 'empresa_id', 'dte_id', nombre_documento=F('dte__nombre'))
	request.session['documentos'] = list(documentos)

	numDia, valorDia, numMes, valorMes = datosInicio(request.session['empresa'])
	valores = {'numDia':numDia, 'valorDia':valorDia, 'numMes': numMes, 'valorMes': valorMes}

	fecha_actual = datetime.now()
	cxc_queryset = DTECliente.objects.filter(emisor=request.session['empresa'], estadoPago=False).annotate(
		dias = ExpressionWrapper(fecha_actual - F('fecEmi'), output_field=DateTimeField()))
	cxc=[]
	for obj in cxc_queryset:
		obj.dias_transcurridos = (fecha_actual - obj.fecEmi).days
		cxc.append(obj)
	
	context = {'empresa': datos_empresa, 'listaDocumentos':documentos, 'valores':valores, 'cxc':cxc}
	
	return render(request, 'dte/index.html', context)


@login_required
def perfil_usuario(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=request.user)
		password_form = PasswordChangeForm(request.user, request.POST)
		if user_form.is_valid() and password_form.is_valid():
			user_form.save()
			password_form.save()
			update_session_auth_hash(request, request.user)  # Importante para mantener la sesión iniciada después de cambiar la contraseña
			return redirect('dte:perfil_usuario')
	else:
		user_form = UserForm(instance=request.user)
		password_form = PasswordChangeForm(request.user)

	return render(request, 'dte/perfil_usuario.html', {'user_form': user_form, 'password_form': password_form})

@login_required(login_url='manager:login')
def autenticar(request):
	return render(request, 'dte/autenticarMH.html')

@login_required(login_url='manager:login')
def loginMH(request):
	if request.method == 'POST':
		datos = Empresa.objects.get(codigo=request.session['empresa'])
		content_type = request.POST.get('content-Type')
		useragent = request.POST.get('User-Agent')
		user = datos.usuarioMH
		pwd = datos.passwordAPI
		url_auth = getUrl(request.session['empresa'], 'Autenticacion')
		data = {'content-Type': content_type, 'User-Agent': useragent, 'user': user, 'pwd': pwd,}
		response = requests.post(url_auth, data=data)
		respuesta_json = response.json()

		if respuesta_json:
			body = respuesta_json.get('body', {})
			token_val = body.get('token', None)
			context = {
			'status' : respuesta_json['status'],
			'body': respuesta_json['body'],
			}

			datos.token = token_val
			datos.fechaToken = datetime.now()
			if datos.token:
				datos.save()
				messages.success(request, 'Respuesta del Ministerio: ' + respuesta_json['status'])
			else:
				messages.info(request, 'Error en la autenticación con el Ministerio de Hacienda')

			return redirect('dte:index')
		else:
			return HttpResponse('Ocurrió un error durante la autenticación')	

	else:
		return HttpResponse('Solicitud incorrecta')



@login_required(login_url='manager:login')
def lista_dte_todos(request, tipo):
	if tipo == 'cliente':
		vEmisor = get_object_or_404(Empresa, codigo=request.session['empresa'])
		dtes_cliente = DTECliente.objects.filter(emisor=vEmisor, ambiente=vEmisor.ambiente.codigo)
		dtes_proveedor = DTEProveedor.objects.filter(emisor=vEmisor, ambiente=vEmisor.ambiente.codigo)
		dtes = list(chain(dtes_cliente, dtes_proveedor))
		lista = sorted(dtes, key=lambda x: x.fecEmi, reverse = True)
		#dtes = DTEProveedor.objects.filter(emisor=vEmisor, ambiente=vEmisor.ambiente.codigo)

	elif tipo == 'proveedor':
		pass
	
	paginator = Paginator(lista, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	return render(request, 'dte/lista_dte.html', {'dtes':dtes, 'listaDocumentos':request.session['documentos'], 'page_obj': page_obj})


def lista_dte(request, tipo):
	vEmisor = get_object_or_404(Empresa, codigo=request.session['empresa'])
	tipoDocumento = get_object_or_404(TipoDocumento, codigo=tipo)
	nombreDoc = tipoDocumento.nombre
	if tipo in {'07', '14'}:
		dtes = DTEProveedor.objects.filter(emisor=vEmisor, ambiente=vEmisor.ambiente.codigo, tipoDte=tipo)
	else:
		dtes = DTECliente.objects.filter(emisor=vEmisor, ambiente=vEmisor.ambiente.codigo, tipoDte=tipo)
	
		
	paginator = Paginator(dtes, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	return render(request, 'dte/lista_dte.html', {'dtes':dtes, 'listaDocumentos':request.session['documentos'], 'page_obj': page_obj, 'nombreDoc':nombreDoc})


@login_required(login_url='manager:login')
def lista_cliente(request):
	clientes = Cliente.objects.filter(empresa_id=request.session['empresa'])
	paginator = Paginator(clientes, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(request, 'dte/lista_clientes.html', {'clientes': page_obj, 'listaDocumentos':request.session['documentos']})
	


@login_required(login_url='manager:login')
def lista_proveedor(request):
	proveedores = Proveedor.objects.filter(empresa_id=request.session['empresa'])
	paginator = Paginator(proveedores, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(request, 'dte/lista_proveedores.html', {'proveedores': page_obj, 'listaDocumentos':request.session['documentos']})
	


@login_required(login_url='manager:login')
def lista_producto(request):
	productos = Producto.objects.filter(empresa=request.session['empresa'])
	paginator = Paginator(productos, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	return render(request, 'dte/lista_producto.html', {'productos':page_obj, 'listaDocumentos':request.session['documentos'], 'page_obj': page_obj})


#@login_required(login_url='manager:login')
class DTEInline():
	model = None
	form_class = None
	template_name = 'dte/dte_create_or_update.html'
	accion = None


	def set_dynamic_attributes(self, tipo, tipoAccion):
		self.accion = tipoAccion
		if tipo in {'01','03','04','05','06','11'}:
			self.model = DTECliente
			self.form_class = DTEClienteForm
		elif tipo in {'07','14'}:
			self.model = DTEProveedor
			self.form_class = DTEProveedorForm
		elif tipo in {'contingencia'}:
			self.model = DTEContingencia
			self.form_class = DTEContingenciaForm


	def get_context_data(self, **kwargs):
		self.set_dynamic_attributes(kwargs.get('tipo'), self.accion)
		context = super().get_context_data(**kwargs)
		#cliente_frm = ClienteForm(initial=dict(codigo=CodGeneracion(), tipoDocumentoCliente= '13', 
		#	empresa = self.request.user.userprofile.empresa.codigo, actividadEconomica='10005', pais='9300',
		#	tipoContribuyente='002', tipoPersona=1))
		context['listaDocumentos'] = self.request.session.get('documentos', [])
		context['bitacora'] = BitacoraAccionDte.objects.filter(dte = self.object.codigoGeneracion) if self.object else ''
		return context

	def form_valid(self, form):
		named_formsets = self.get_named_formsets()
		#messages.success(self.request, {'named_formsets': named_formsets})

		if not all((x.is_valid() for x in named_formsets.values())):
			messages.warning(self.request, 'No se pudo guardar el DTE, por favor revise los datos')
			return self.render_to_response(self.get_context_data(form=form))
		
		empresa = get_object_or_404(Empresa, codigo=self.request.session['empresa'])

		self.object = form.save()
		BitacoraDTE(self.request, usuario=self.request.user, dte=form.instance.codigoGeneracion, tipo=self.kwargs.get('tipo'), accion=self.accion)

		if self.kwargs.get('tipo') in {'01','03','04','05','06','11'}:
			DTECliente.objects.filter(codigoGeneracion=form.instance.codigoGeneracion).update(ambiente=empresa.ambiente.codigo)
		elif self.kwargs.get('tipo') in {'07','14'}:
			DTEProveedor.objects.filter(codigoGeneracion=form.instance.codigoGeneracion).update(ambiente=empresa.ambiente.codigo)
		elif self.kwargs.get('tipo') in {'contingencia'}:
			DTEContingencia.objects.filter(codigoGeneracion=form.instance.codigoGeneracion).update(ambiente=empresa.ambiente.codigo)


		# for every formset, attempt to find a specific formset save function
        # otherwise, just save.
		for name, formset in named_formsets.items():
			formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
			if formset_save_func is not None:
				formset_save_func(formset)
			else:
				formset.save()

		if not self.object.selloRecepcion:
			if self.object.numeroControl and self.object.tipoDte.codigo in ('01','03','04','05','06','07','11','14'):
				qr = genQr(codigo=self.object.codigoGeneracion, empresa=self.object.emisor_id)
				json = genJson(codigo=self.object.codigoGeneracion, tipo=self.object.tipoDte.codigo, empresa=self.object.emisor_id)
				firma = firmar(codigo=self.object.codigoGeneracion, tipo=self.object.tipoDte.codigo)
			if self.object.tipoDte.codigo == 'contingencia':
				json = genJson(codigo=self.object.codigoGeneracion, tipo=self.object.tipoDte.codigo, empresa=self.object.emisor_id)
				firma = firmar(codigo=self.object.codigoGeneracion, tipo=self.object.tipoDte.codigo)

		messages.success(self.request, 'Documento guardado')
		return redirect('dte:actualizar', tipo=self.object.tipoDte.codigo, pk=self.object.codigoGeneracion)

	def formset_detalles_valid(self, formset):
		detalles = formset.save(commit=False)
		#for obj in formset.deleted_objects:
		#	obj.delete()
		for detalle in detalles:
			#messages.info(self.request, detalle)
			detalle.dte = self.object
			detalle.save()

			#
			
			if self.kwargs.get('tipo') in {'01','03','04','05','06','11'}:
				dte = DTECliente.objects.get(codigoGeneracion=detalle.dte_id)
				receptor = Cliente.objects.get(codigo=dte.receptor_id)
			if self.kwargs.get('tipo') in {'07','14'}:
				dte = DTEProveedor.objects.get(codigoGeneracion=detalle.dte_id)
				receptor = Proveedor.objects.get(codigo=dte.receptor_id)
			if self.kwargs.get('tipo') in {'contingencia'}:
				dte = DTEContingencia.objects.get(codigoGeneracion=detalle.dteContingencia_id)


			# Inicio de cálculos
			#messages.info(self.request, str(receptor.tipoContribuyente.codigo) + ' - ' + str(receptor.tipoContribuyente))
			if dte.tipoDte.codigo in {'01','03','04','05','06','11'}:
				total_gravada = DTEClienteDetalle.objects.filter(dte_id=detalle.dte_id).aggregate(total_gravada=Sum(F('ventaGravada')))['total_gravada']
				
				if receptor.tipoContribuyente.codigo == '001':
					if dte.tipoDte.codigo == '01':
						retencion = round(((float(total_gravada) / float(1.13)) * float(0.01)),2)
					else:
						retencion = round((float(total_gravada) * float(0.01)),2)
				else:
					retencion = 0

			if dte.tipoDte.codigo in {'01'}:
				DTECliente.objects.filter(codigoGeneracion=detalle.dte_id).update(
					totalGravada = total_gravada,
					subTotalVentas = total_gravada,
					subTotal = total_gravada,
					ivaPerci1 = float(total_gravada) - (float(total_gravada) / float(1.13)),
					ivaRete1 = retencion,
					montoTotalOperacion = float(total_gravada),
					totalPagar = float(total_gravada) - float(retencion))

			if dte.tipoDte.codigo in {'03'}:
				DTECliente.objects.filter(codigoGeneracion=detalle.dte_id).update(
					totalGravada=total_gravada,
					subTotalVentas=total_gravada,
					subTotal=total_gravada,
					ivaPerci1=0, #float(total_gravada)*float(0.13),
					ivaRete1 = retencion,
					montoTotalOperacion= round((float(total_gravada)*float(1.13)),2),
					totalPagar = round((float(total_gravada)*float(1.13)),2) - float(retencion))
			if dte.tipoDte.codigo in {'05','06'}:
				DTECliente.objects.filter(codigoGeneracion=detalle.dte_id).update(
					totalGravada=total_gravada,
					subTotalVentas=total_gravada,
					subTotal=total_gravada,
					ivaPerci1=0, #float(total_gravada)*float(0.13),
					montoTotalOperacion=float(total_gravada)*float(1.13),
					totalPagar=float(total_gravada)*float(1.13))
			if dte.tipoDte.codigo in {'11'}:
				DTECliente.objects.filter(codigoGeneracion=detalle.dte_id).update(
					totalGravada=total_gravada,
					montoTotalOperacion=total_gravada,
					totalPagar=total_gravada)
			if dte.tipoDte.codigo in {'14'}:
				total_compra = DTEProveedorDetalle.objects.filter(dte_id=detalle.dte_id).aggregate(total_compra=Sum(F('compra')))['total_compra']
				DTEProveedor.objects.filter(codigoGeneracion=detalle.dte_id).update(
					totalCompra=total_compra,
					reteRenta=round((float(total_compra)*float(0.1)),2),
					subTotal=total_compra,
					totalPagar=round((float(total_compra)-(float(total_compra)*0.1)),2))

			# Fin de cálculos

			if self.object.tipoDte.codigo in {'01','03','04','05','06','11'}:
				instancia1 = DTEClienteDetalle.objects.get(codigoDetalle = detalle.codigoDetalle)
				instancia2 = TributoResumen.objects.get(codigo='20')
				obj, created = DTEClienteDetalleTributo.objects.get_or_create(
					codigoDetalle=instancia1,
					codigo=instancia2,
					defaults={'descripcion': instancia2.nombre, 'valor': instancia1.ventaGravada * Decimal(0.13)}
				)

			# Si el registro ya existía, actualiza el valor
				if not created:
					#if tipo not in {'contingencia',}:
					obj.valor = instancia1.ventaGravada * Decimal(0.13)
					obj.save()


			if self.object.tipoDte.codigo in {'dte proveedor'}:
				instancia1 = DTEProveedorDetalle.objects.get(codigoDetalle = detalle.codigoDetalle)
				instancia2 = TributoResumen.objects.get(codigo='20')
				obj, created = DTEProveedorDetalleTributo.objects.get_or_create(
					codigoDetalle=instancia1,
					codigo=instancia2,
					defaults={'descripcion': instancia2.nombre, 'valor': instancia1.ventaGravada * Decimal(0.13)}
				)

			# Si el registro ya existía, actualiza el valor
				if not created:
					#if tipo not in {'contingencia',}:
					obj.valor = instancia1.ventaGravada * Decimal(0.13)
					obj.save()
		messages.success(self.request, 'Detalle guardado')



class DTECreate(DTEInline, CreateView):
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['empresa'] = self.request.session.get('empresa')
		tipo = self.kwargs.get('tipo')
		accion = get_object_or_404(TipoAccionUsuario, id=1)
		self.set_dynamic_attributes(tipo, 1)
		kwargs['tipo'] = tipo
		#kwargs['request'] = self.request
		#messages.info(self.request, kwargs['tipo'])
		#messages.info(self.request, tipo)
		return kwargs


	def get_form_class(self):
		tipo = self.kwargs.get('tipo')
		self.set_dynamic_attributes(tipo, 1)  # Asegurarse de que el modelo y el formulario estén configurados
		if self.form_class is None:
			raise ImproperlyConfigured("No se ha definido form_class.")
		#messages.info(self.request, self.form_class)
		return self.form_class


	def get_queryset(self):
		tipo = self.kwargs.get('tipo')
		self.set_dynamic_attributes(tipo)  # Asegurarse de que el modelo esté configurado
		if self.model:
			#messages.info(self.request, self.model)
			return self.model.objects.all()
		else:
			raise ImproperlyConfigured("El modelo no está definido correctamente")



	def get_initial(self):
		initial = super().get_initial()
		codigo = self.kwargs.get('tipo')
		tipo_documento = get_object_or_404(TipoDocumento, codigo=codigo)
		#messages.info(self.request, {'tipo':tipo_documento})
		session_key = self.request.session.session_key
		session_store = SessionStore(session_key=session_key)
		empresa = get_object_or_404(Empresa, codigo=self.request.session['empresa'])
		#empresa = self.request.session['empresa']
		if codigo in {'01','07','08','09','11','14','15'}:
			version = 1
		elif codigo in {'03','04','05','06'}:
			version = 3
		elif codigo == 'contingencia':
			version = 3

		initial['codigoGeneracion'] = CodGeneracion().upper()
		initial['emisor'] = self.request.session['empresa']
		initial['tipoDte'] = tipo_documento
		initial['version'] = version
		initial['ambiente'] = empresa.ambiente.codigo
		#messages.info(self.request, empresa.ambiente.codigo)

		return initial

	def get_context_data(self, **kwargs):
		ctx = super(DTECreate, self).get_context_data(**kwargs)
		nombreTipoDoc = TipoDocumento.objects.get(codigo=self.kwargs.get('tipo'))
		#messages.info(self.request, {'tipo':nombreTipoDoc.codigo})
		ctx['TipoDocumento'] = nombreTipoDoc
		ctx['named_formsets'] = self.get_named_formsets()
		ctx['codigoDetalle'] = CodGeneracion()
		return ctx

	def get_named_formsets(self):
		formDetalle = None
		if self.kwargs.get('tipo') in {'01','03'}:
			formDetalle = FCCFDetalleFormSet
		elif self.kwargs.get('tipo') in {'05','06'}:
			formDetalle = NCDDetalleFormSet
		elif self.kwargs.get('tipo') == '11':
			formDetalle = FEXDetalleFormSet
		elif self.kwargs.get('tipo') == '14':
			formDetalle = FSEDetalleFormSet
		elif self.kwargs.get('tipo') == 'contingencia':
			formDetalle = ContingenciaDetalleFormSet

		if self.request.method == 'GET':
			#messages.info(self.request, self.kwargs.get('pk'))
			return {
				'detalles' : formDetalle(prefix='detalles')
			}
		else:
			#messages.info(self.request, self.kwargs.get('pk'))
			return {
				'detalles' : formDetalle(self.request.POST or None, self.request.FILES or None, prefix='detalles'),
			}

			#messages.success(self.request, DTEClienteDetalleFormSet(prefix='detalles')) #Borrar


class DTEUpdate(DTEInline, UpdateView):
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['empresa'] = self.request.session.get('empresa')
		tipo = self.kwargs.get('tipo')
		#self.set_dynamic_attributes(tipo)
		kwargs['tipo'] = tipo
		#kwargs['request'] = self.request
		#messages.info(self.request, kwargs['tipo'])
		return kwargs


	def get_form_class(self):
		tipo = self.kwargs.get('tipo')
		self.set_dynamic_attributes(tipo, 2)  # Asegurarse de que el modelo y el formulario estén configurados
		if self.form_class is None:
			raise ImproperlyConfigured("No se ha definido form_class.")
		return self.form_class


	def get_queryset(self):
		tipo = self.kwargs.get('tipo')
		self.set_dynamic_attributes(tipo, 2)  # Asegurarse de que el modelo esté configurado
		if self.model:
			return self.model.objects.all()
		else:
			raise ImproperlyConfigured("El modelo no está definido correctamente")

		
	def get_context_data(self, **kwargs):
		ctx = super(DTEUpdate, self).get_context_data(**kwargs)
		#messages.info(self.request, self.kwargs.get('tipo'))
		if self.kwargs.get('tipo')=='contingencia':
			Documento = get_object_or_404(DTEContingencia, codigoGeneracion=self.kwargs.get('pk'))
		elif self.kwargs.get('tipo') in {'01','03','04','05','06','11'}:
			Documento = get_object_or_404(DTECliente, codigoGeneracion=self.kwargs.get('pk'))
		elif self.kwargs.get('tipo') in {'07','14'}:
			Documento = get_object_or_404(DTEProveedor, codigoGeneracion=self.kwargs.get('pk'))

		anulado = DTEInvalidacion.objects.filter(codigoDte=self.kwargs.get('pk')).first()
		ctx['Documento'] = Documento
		ctx['sello'] = Documento.selloRecepcion
		ctx['anulado'] = anulado if anulado else None
		ctx['named_formsets'] = self.get_named_formsets()
		#messages.success(self.request, {'DTEUpdate: ':'update', 'ctx':ctx})
		return ctx

	def get_named_formsets(self):
		#messages.info(self.request, {'DTEUpdate: ':self.request})
		#messages.info(self.request, self.kwargs.get('tipo'))
		if str(self.kwargs.get('tipo'))=='contingencia':
			dte = get_object_or_404(DTEContingencia, codigoGeneracion=self.kwargs.get('pk'))
		elif str(self.kwargs.get('tipo')) in {'01','03','04','05','06','11'}:
			dte = get_object_or_404(DTECliente, codigoGeneracion=self.kwargs.get('pk'))
		elif str(self.kwargs.get('tipo')) in {'07','14'}:
			dte = get_object_or_404(DTEProveedor, codigoGeneracion=self.kwargs.get('pk'))

		if dte.tipoDte.codigo in {'01','03'}:
			formDetalle = FCCFDetalleFormSet
		elif dte.tipoDte.codigo in {'05','06'}:
			formDetalle = NCDDetalleFormSet
		elif dte.tipoDte.codigo == '11':
			formDetalle = FEXDetalleFormSet
		elif dte.tipoDte.codigo == '14':
			formDetalle = FSEDetalleFormSet
		elif self.kwargs.get('tipo') == 'contingencia':
			formDetalle = ContingenciaDetalleFormSet
		#messages.info(self.request, formDetalle)
		return {
		'detalles': formDetalle(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='detalles')
		}


def eliminar_detalle(request, tipo, pk):
	try:
		detalle = DTEClienteDetalle.objects.get(codigoDetalle=pk)
	except DTEClienteDetalle.DoesNotExist:
		messages.success(
			request, 'Objeto no existe'
			)
		return redirect('dte:actualizar', tipo=tipo, pk=detalle.dte.codigoGeneracion)

	detalle.delete()

	messages.success(
		request, 'Detalle eliminado con éxito'
		)

	return redirect('dte:actualizar', tipo=tipo, pk=detalle.dte.codigoGeneracion)


class EnviarDTEView(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, tipo, codigo=None, cod_anulacion=None):

		if tipo in {'01','03','04','05','06','11'}:
			modelo = DTECliente.objects.get(codigoGeneracion=codigo)
			emisor = get_object_or_404(Empresa, codigo=modelo.emisor.codigo)
			ambiente = modelo.ambiente.codigo
			version = modelo.version
			docfirmado = modelo.docfirmado
		elif tipo in {'07','14'}:
			modelo = DTEProveedor.objects.get(codigoGeneracion=codigo)
			emisor = get_object_or_404(Empresa, codigo=modelo.emisor.codigo)
			ambiente = modelo.ambiente.codigo
			version = modelo.version
			docfirmado = modelo.docfirmado
		elif tipo == 'anulacion':
			modelo = DTEInvalidacion.objects.get(codigoGeneracion=cod_anulacion)
			codigo = modelo.codigoDte
			emisor = get_object_or_404(Empresa, codigo=modelo.emisor.codigo)
			ambiente = emisor.ambiente.codigo
			version = 2
			docfirmado = modelo.docfirmado
		elif tipo == 'contingencia':
			modelo = DTEContingencia.objects.get(codigoGeneracion=codigo)
			emisor = get_object_or_404(Empresa, codigo=modelo.emisor.codigo)
			ambiente = emisor.ambiente.codigo
			version = 3
			docfirmado = modelo.docfirmado
			#return redirect('dte:index')

		if os.name == 'posix':
			archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{cod_anulacion if cod_anulacion else codigo}.json')
		else:
			archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{cod_anulacion if cod_anulacion else codigo}.json').replace('/', '\\')

		with open(archivo, 'rb') as file:
			archivo_adjunto = file.read()
			nombre_archivo = os.path.basename(archivo)

		if tipo in {'01','03','04','05','06','07','07A','08','09','11','14','15'}:
			url = getUrl(emisor.codigo, 'Recepciondte')
			headers = {
				'Authorization': emisor.token,
				'User-Agent': 'alfa/1.0',
				'Content-Type': 'application/json',
			}			
			data={
				'ambiente': ambiente,
				'idEnvio': 1,
				'version': version,
				'tipoDte': tipo,
				'documento': docfirmado,
				'codigoGeneracion': codigo,
			}
		if tipo in {'anulacion'}:
			url = getUrl(emisor.codigo, 'Anulardte')
			headers = {
				'Authorization': emisor.token,
				'User-Agent': 'alfa/1.0',
				'Content-Type': 'application/json'
			}			
			data={
				'ambiente': ambiente,
				'idEnvio': 1,
				'version': 2,
				'documento': docfirmado
			}
		if tipo in {'contingencia'}:
			url = getUrl(emisor.codigo, 'Contingencia')
			headers = {
				'Authorization': emisor.token,
				'User-Agent': 'alfa/1.0',
				'Content-Type': 'application/json',
			}			
			data={
				'nitEmisor': emisor.nit,
				'documento': docfirmado,
			}

		response = requests.post(url, headers=headers, json=data)
		#response = Mock()
		#response.status_code = 200

		if response.status_code == 666:
			messages.info(request, {'request':request, 'user':request.user})
			return redirect('dte:actualizar', tipo='01', pk=codigo)

		if response.status_code == 200:
			respuesta_servicio = response.json()
			#respuesta_servicio = {'selloRecibido':'20249i923u09nnsdif'}
			estado = get_object_or_404(EstadoDTE, codigo='002')

			if tipo in {'01','03','04','05','06','08','09','11','15'}:
				gsello = DTECliente.objects.get(codigoGeneracion=codigo)
				gsello.selloRecepcion = respuesta_servicio['selloRecibido']
				gsello.estadoDte = estado
				gsello.save()
			elif tipo in {'07','14'}:
				gsello = DTEProveedor.objects.get(codigoGeneracion=codigo)
				gsello.selloRecepcion = respuesta_servicio['selloRecibido']
				gsello.estadoDte = estado
				gsello.save()
			elif tipo in {'anulacion'}:
				gsello = DTEInvalidacion.objects.get(codigoGeneracion=cod_anulacion)
				gsello.selloRecepcion = respuesta_servicio['selloRecibido']
				gsello.save()
			elif tipo in {'contingencia'}:
				gsello = DTEContingencia.objects.get(codigoGeneracion=codigo)
				gsello.selloRecepcion = respuesta_servicio['selloRecibido']
				gsello.save()

			try:
				with open(archivo, 'r') as json_file:
					contenido_actual = json.load(json_file)
			except FileNotFoundError:
				contenido_actual = {}

			contenido_actual['selloRecepcion'] = respuesta_servicio

			with open(archivo, 'w') as json_file:
				json.dump(contenido_actual, json_file, indent=2)

			subirArchivo(modelo.emisor.codigo, f'{codigo}.json')

			#if not cod_anulacion or tipo != 'contingencia':
			if not tipo in {'anulacion','contingencia'}:
				genPdf(codigo=codigo, tipo=tipo, empresa=emisor.codigo)
				BitacoraDTE(request=request, usuario=request.user, dte=codigo, tipo=tipo, accion=3)
				if emisor.ambiente.codigo=='01':
					correo = enviarCorreo(request, codigo=codigo, tipo=tipo)
				#messages.info(correo)
			#res = gen_pdf(codigo, tipo, version, ambiente)
			#estado = EstadoDTE.objects.get(codigo='005')
			#cambiarEstadoDte(tipo, codigo, estado)
			#messages.success(request, res)
			messages.success(request, respuesta_servicio)
			#return redirect(template, codigo=codigo)
			if tipo=='anulacion':
				#messages.warning(request, {'Reenvío después de enviar a MH': modelo.tipoDte.codigo})
				return redirect('dte:actualizar', tipo=modelo.tipoDte.codigo, pk=modelo.codigoDte)
			else:
				return redirect('dte:actualizar', tipo=tipo, pk=codigo)

		else:
			error_message = f"Error en la solicitud: {response.status_code} - {response.text}"
			#error_message = response
			messages.info(request, error_message)
			#return redirect(template, codigo=codigo)
			if tipo=='anulacion':
				#messages.warning(request, {'Reenvío después de enviar a MH': modelo.tipoDte.codigo})
				return redirect('dte:actualizar', tipo=modelo.tipoDte.codigo, pk=modelo.codigoDte)
			else:
				return redirect('dte:actualizar', tipo=tipo, pk=codigo)
	
	def post(self, request, codigo, doc_firmado):
		# Manejar la lógica para solicitudes GET si es necesario
		return Response({"detail": "Solicitud POST procesada correctamente."})


def firmarDte(request, codigo, tipo): ########## BORRAR ###################
	
	emisor = Empresa.objects.get(codigo=request.session['empresa'])
	usuariomh = emisor.usuarioMH
	pwd = emisor.passwordPri

	if os.name == 'posix':
		archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{codigo}.json')
	else:
		archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{codigo}.json').replace('\\', '/')

	#messages.info(request, 'Archivo: ' + archivo)
	
	with open(archivo, 'rb') as file:
		json_data = json.load(file)

	firma_url = getUrl(emisor.codigo, 'Firmadodte')

	data = {
		'nit': usuariomh,
		'passwordPri': pwd,
		'dteJson':json_data
	}

	data1 = {
		'nit': usuariomh,
		'passwordPri': pwd,
		'dteJson':json_data
	}

	#messages.info(request, {'data1': data1})

	headers = {'content-Type': 'application/JSON'}
	#messages.info(request, 'Firmado: ' + codigo)
	response = requests.post(firma_url, json=data, headers=headers)


	if response.status_code == 200:
		response_data = json.loads(response.text)
		#messages.info(request, {'response': response_data})
		status_value = response_data.get("status", None)
		body_value = response_data.get("body", None)

		#if tipo in {'01','03','04','05','06','08','09','11','14','15'}:
		#	guardar_firma = DTECliente.objects.get(codigoGeneracion=codigo)
		#	guardar_firma.docfirmado = body_value
		#	guardar_firma.save()
		#elif tipo in {'07'}:
		#	pass

		#with open(archivo, 'r') as json_file:
		#	data = json.load(json_file)

		#try:
		#	with open(archivo, 'r') as json_file:
		#			contenido_actual = json.load(json_file)
		#except FileNotFoundError:
		#	contenido_actual = {}

		#contenido_actual['token'] = body_value

		#return redirect('dte:index')
		#return redirect('dte:actualizar', pk=codigo)
		#return JsonResponse(response_data)
		#messages.success(request, body_value)
		return redirect('dte:enviar_mh_prueba', tipo=tipo, codigo=codigo, doc=body_value)
	else:
		messages.info(request, data)
		return JsonResponse({'resp':data, 'codigo':response.status_code, 'url':firma_url})


class EnviarDTEView_prueba(APIView):
	def get(self, request, tipo, codigo, doc, cod_anulacion=None):
		#messages.info(request, doc)
	#	template = 'sitria:actualizar_dte'
	#def get(self, request, codigo, tipo, version, ambiente, docfirmado):
		if tipo in {'01','07','08','09','11','14','15'}:
			versionN = 1
		elif tipo in {'03','04','05','06'}:
			versionN = 3

		tConfiguracion = None #Configuracion.objects.filter(empresa='001').first()
		if tipo in {'01','03','04','05','06','11','14','anulacion'}:
			#modelo = DTECliente.objects.get(codigoGeneracion=codigo)
			emisor = get_object_or_404(Empresa, codigo=request.session['empresa'])
			ambiente = '00' #modelo.ambiente.codigo
			version = versionN #modelo.version
			docfirmado = doc #modelo.docfirmado				
		

		if os.name == 'posix':
			archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{codigo}.json')
		else:
			archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{codigo}.json').replace('/', '\\')

		with open(archivo, 'rb') as file:
			archivo_adjunto = file.read()
			nombre_archivo = os.path.basename(archivo)

		if tipo in {'01','03','04','05','06','07','07A','08','09','11','14','15'}:
			url = getUrl(emisor.codigo, 'Recepciondte')
			headers = {
				'Authorization': emisor.token,
				'User-Agent': 'alfa/1.0',
				'Content-Type': 'application/json',
			}			
			data={
				'ambiente': ambiente,
				'idEnvio': 1,
				'version': version,
				'tipoDte': tipo,
				'documento': docfirmado,
				'codigoGeneracion': codigo,
			}
		if tipo in {'anulacion'}:
			url = getUrl(emisor.codigo, 'Anulardte')
			headers = {
				'Authorization': emisor.token,
				'User-Agent': 'alfa/1.0',
				'Content-Type': 'application/json'
			}			
			data={
				'ambiente': ambiente,
				'idEnvio': 1,
				'version': version,
				'documento': docfirmado
			}
		if tipo in {'contingencia'}:
			url = getUrl(emisor.codigo, 'Contingencia')
			headers = {
				'Authorization': emisor.token,
				'User-Agent': 'alfa/1.0',
				'Content-Type': 'application/json',
			}			
			data={
				'nitEmisor': '06142407620011',
				'documento': docfirmado,
			}

			#consol={'url':url, 'headers':headers, 'data':data}

		#files = {(nombre_archivo, archivo_adjunto)}

		response = requests.post(url, headers=headers, json=data)

		if response.status_code == 200:
			respuesta_servicio = response.json()

			#if tipo in {'01','03','04','05','06','08','09','11','14','15'}:
			#	gsello = DTECliente.objects.get(codigoGeneracion=codigo)
			#	gsello.selloRecepcion = respuesta_servicio['selloRecibido']
			#	gsello.save()
			#elif tipo in {'07'}:
			#	gsello = DTEProveedor.objects.get(codigoGeneracion=codigo)
			#	gsello.selloRecepcion = respuesta_servicio['selloRecibido']
			#	gsello.save()

			try:
				with open(archivo, 'r') as json_file:
					contenido_actual = json.load(json_file)
			except FileNotFoundError:
				contenido_actual = {}

			contenido_actual['selloRecepcion'] = respuesta_servicio

			with open(archivo, 'w') as json_file:
				json.dump(contenido_actual, json_file, indent=2)

			#genPdf(codigo=codigo, tipo=tipo, empresa=emisor.codigo)
			#res = gen_pdf(codigo, tipo, version, ambiente)
			#estado = EstadoDTE.objects.get(codigo='005')
			#cambiarEstadoDte(tipo, codigo, estado)
			#messages.success(request, res)
			messages.success(request, respuesta_servicio)
			#return redirect(template, codigo=codigo)
			#return redirect('dte:actualizar', tipo=tipo, pk=codigo)
			return redirect('dte:prueba')

		else:
			error_message = f"Error en la solicitud: {response.status_code} - {response.text}"
			messages.info(request, error_message)
			#return redirect(template, codigo=codigo)
			#return redirect('dte:actualizar', pk=codigo)
			return redirect('dte:prueba')
	
	def post(self, request, codigo, doc_firmado):
		# Manejar la lógica para solicitudes GET si es necesario
		return Response({"detail": "Solicitud POST procesada correctamente."})


def autocompletar_producto(request):
	term = request.GET.get('term')
	productos = Producto.objects.filter(nombre__icontains=term).values_list('nombre', flat=True)
	return JsonResponse(list(productos), safe=False)


@login_required(login_url='manager:login') ########### Borrar #############
def cliente_detail(request, pk):
	cliente = get_object_or_404(Cliente, pk=pk)
	return render(request, 'dte/cliente_detalle.html', {'cliente': cliente, 'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login')
def cliente_create(request):
	codigo = CodGeneracion().upper()
	if request.method == 'POST':
		form = ClienteForm(request.POST)
		empresa = get_object_or_404(Empresa, codigo=request.session['empresa'])
		form.instance.empresa = empresa
		if form.is_valid():
			cliente = form.save()
			messages.success(request, 'Cliente guardado')
			return redirect('dte:cliente_update', pk=cliente.pk)
	else:		
		form = ClienteForm(initial = {'codigo':codigo, 'pais':'9300','tipoDocumentoCliente':'13' , 'actividadEconomica':'10005', 'tipoContribuyente':'003'})
	return render(request, 'dte/cliente_detalle.html', {'form': form,'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login') ########### Borrar #############
def proveedor_detail(request, pk):
	proveedor = get_object_or_404(Proveedor, pk=pk)
	return render(request, 'dte/proveedor_detalle.html', {'proveedor': proveedor, 'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login')
def proveedor_create(request):
	codigo = CodGeneracion().upper()
	if request.method == 'POST':
		form = ProveedorForm(request.POST)
		empresa = get_object_or_404(Empresa, codigo=request.session['empresa'])
		form.instance.empresa = empresa
		if form.is_valid():
			proveedor = form.save()
			messages.success(request, 'Proveedor guardado')
			return redirect('dte:proveedor_update', pk=proveedor.pk)
	else:		
		form = ProveedorForm(initial = {'codigo':codigo, 'pais':'9300','tipoDocumentoCliente':'13' , 'actividadEconomica':'10005', 'tipoContribuyente':'003'})
	return render(request, 'dte/proveedor_detalle.html', {'form': form,'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login')
def producto(request, pk=None):
	if pk:
		producto = get_object_or_404(Producto, codigo=pk)
	else:
		producto = None

	if request.method=='POST':
		form = ProductoForm(request.POST, instance=producto)
		#messages.success(request, form.empresa_id)
		if form.is_valid():
			empresa = get_object_or_404(Empresa, codigo=request.session['empresa'])
			form.instance.empresa = empresa
			producto = form.save()
			#messages.success(request, form.empresa)
			messages.success(request, 'Producto guardado')
			return redirect('dte:producto_detalle', pk=producto.codigo)
	else:
		if pk:
			form = ProductoForm(instance=producto)
		else:
			form = ProductoForm(initial={'codigo':CodGeneracion})
	return render(request, 'dte/producto_detalle.html', {'form': form})



@login_required(login_url='manager:login')
def guardar_cliente_modal(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            # Redireccionar a una página de éxito o cualquier otra página que desees
            #return redirect('ruta_hacia_pagina_exito')
    # Si el formulario no es válido, puedes manejarlo aquí
    # por ejemplo, renderizando nuevamente la página con el formulario y mostrando los errores
    # return redirect(request, 'tu_template.html', {'form': form})
    return HttpResponse('guardado')


@login_required(login_url='manager:login')
def cliente_update(request, pk):
	cliente = get_object_or_404(Cliente, codigo=pk)
	if request.method == 'POST':
		form = ClienteForm(request.POST, instance=cliente)
		if form.is_valid():
			cliente = form.save()
			messages.success(request, 'Cliente guardado')
			return redirect('dte:cliente_update', pk=pk)
	else:
		form = ClienteForm(instance=cliente)
	return render(request, 'dte/cliente_detalle.html', {'form': form, 'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login')
def proveedor_update(request, pk):
	proveedor = get_object_or_404(Proveedor, codigo=pk)
	if request.method == 'POST':
		form = ProveedorForm(request.POST, instance=proveedor)
		if form.is_valid():
			proveedor = form.save()
			messages.success(request, 'Proveedor guardado')
			return redirect('dte:proveedor_update', pk=pk)
	else:
		form = ProveedorForm(instance=proveedor)
	return render(request, 'dte/proveedor_detalle.html', {'form': form, 'listaDocumentos':request.session['documentos']})




@login_required(login_url='manager:login')
def perfil_empresa(request):
	empresa = get_object_or_404(Empresa, codigo=request.session['empresa'])
	if request.method == 'POST':
		form = EmpresaPerfilForm(request.POST, instance=empresa)
		if form.is_valid():
			empresa = form.save()
			messages.success(request, 'Datos actualizados')
			return redirect('dte:perfil_empresa')
	else:
		form = EmpresaPerfilForm(instance=empresa)
	return render(request, 'dte/perfil_empresa.html', {'form':form})


@login_required(login_url='manager:login')
def cliente_delete(request, pk):
	cliente = get_object_or_404(Cliente, pk=pk)
	if request.method == 'POST':
		cliente.delete()
		return redirect('dte:cliente_list')
	return render(request, 'dte/cliente_confirm_delete.html', {'cliente': cliente, 'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login')
def proveedor_delete(request, pk):
	proveedor = get_object_or_404(Proveedor, pk=pk)
	if request.method == 'POST':
		proveedor.delete()
		return redirect('dte:proveedor_list')
	return render(request, 'dte/proveedor_confirm_delete.html', {'proveedor': proveedor, 'listaDocumentos':request.session['documentos']})


class VistaPreviaHTML(TemplateView):
	template_name = None

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		emisor = Empresa.objects.get(codigo=self.request.session['empresa'])

		tipo = self.kwargs['tipo']
		codigo = self.kwargs['codigo']

		if tipo == '01':
			self.template_name = 'plantillas/dte_fcf.html'
			dte = DTECliente.objects.get(codigoGeneracion=codigo)
			receptor = Cliente.objects.get(codigo=dte.receptor_id)
			dte_detalle = DTEClienteDetalle.objects.filter(dte=dte)

		if tipo == '03':
			self.template_name = 'plantillas/dte_ccf.html'
			dte = DTECliente.objects.filter(codigoGeneracion=codigo).annotate(
				totalExentaIVA=ExpressionWrapper(F('totalExenta') * 1.13, output_field=DecimalField()),
				totalGravadaIVA=ExpressionWrapper(F('totalGravada') * 1.13, output_field=DecimalField()),
				subTotalVentasIVA=ExpressionWrapper(F('subTotalVentas') * 1.13, output_field=DecimalField()),
				totalPagarIVA=ExpressionWrapper(F('totalPagar'), output_field=DecimalField())
			).first()
			receptor = Cliente.objects.get(codigo=dte.receptor_id)
			dte_detalle = DTEClienteDetalle.objects.filter(dte=dte).annotate(
				precio_con_iva=ExpressionWrapper(F('precioUni') * 1.13, output_field=DecimalField()),
				subt_precio_con_iva=ExpressionWrapper(F('ventaGravada') * 1.13, output_field=DecimalField())
			)

		letras = CantLetras(dte.totalPagar)
		fecha = dte.fecEmi.strftime('%d/%m/%Y')

		ruta_logo = f'https://alfadte.azurewebsites.net/static/clientes/logos/{self.request.session["empresa"]}.png'
		#ruta_qr = f'https://alfadte.azurewebsites.net/static/clientes/{self.request.session["empresa"]}/{dte.codigoGeneracion}.png'
		ruta_qr = 'https://almacendte.blob.core.windows.net/clientes/799B7357-74F8-4D43-B097-F0DD9A1C8489.png'

		if self.request.session["empresa"] == 'A4BCBC83-4C59-4A3F-9C25-807D83AD0837':
			ruta_logo = 'https://alfadte.azurewebsites.net/media/logos/A4BCBC83-4C59-4A3F-9C25-807D83AD0837.png'

		context['dte'] = dte
		context['emisor'] = emisor
		context['receptor'] = receptor
		context['dte_detalle'] = dte_detalle
		context['letras'] = letras
		context['logo'] = str(ruta_logo)
		context['qr'] = str(ruta_qr)
		context['fecha'] = fecha

		return context

	def render_to_response(self, context, **response_kwargs):
		return render(self.request, self.template_name, context, **response_kwargs)


def vista_previa_correo(request, tipo, codigo):
	datos = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	empresa = get_object_or_404(Empresa, codigo=datos.emisor.codigo)
	logo = request.session['logo']
	#logo_local = 
	enlace = f'https://admin.factura.gob.sv/consultaPublica?ambiente={empresa.ambiente.codigo}&codGen={datos.codigoGeneracion}&fechaEmi={datos.fecEmi.strftime("%Y-%m-%d")}'
	context={'datos':datos, 'logo':logo, 'enlace':enlace}
	return render(request, 'plantillas/correo_receptor.html', context)



def vista_previa_pdf_dte(request, tipo, codigo, *args, **kwargs):
	options = {
		'page-size': 'Letter',
		'page-height': "11in",
		'page-width': "8.5in",
		'margin-top': '0.5in',
		'margin-right': '0.5in',
		'margin-bottom': '0.5in',
		'margin-left': '0.5in',
		'encoding': "UTF-8",
	}

	template_path = ''
	emisor = Empresa.objects.get(codigo=request.session['empresa'])
	codigo = codigo
	
	
	if tipo == '01':
		template_name = 'plantillas/dte_fcf.html'
		dte = DTECliente.objects.get(codigoGeneracion=codigo)
		receptor = Cliente.objects.get(codigo=dte.receptor_id)
		dte_detalle = DTEClienteDetalle.objects.filter(dte=dte)

	if tipo == '03':
		template_name = 'plantillas/dte_ccf.html'
		dte = DTECliente.objects.filter(codigoGeneracion=codigo).annotate(
			totalExentaIVA=ExpressionWrapper(F('totalExenta') * 1.13, output_field=DecimalField()),
			totalGravadaIVA=ExpressionWrapper(F('totalGravada') * 1.13, output_field=DecimalField()),
			IVA=ExpressionWrapper(F('totalGravada') * 0.13, output_field=DecimalField()),
			subTotalVentasIVA=ExpressionWrapper(F('subTotalVentas') * 1.13, output_field=DecimalField()),
			totalPagarIVA=ExpressionWrapper(F('totalPagar'), output_field=DecimalField())
		).first()
		receptor = Cliente.objects.get(codigo=dte.receptor_id)
		dte_detalle = DTEClienteDetalle.objects.filter(dte=dte).annotate(
			precio_con_iva=ExpressionWrapper(F('precioUni') * 1.13, output_field=DecimalField()),
			subt_precio_con_iva=ExpressionWrapper(F('ventaGravada') * 1.13, output_field=DecimalField())
		)

	if tipo == '05':
		template_name = 'plantillas/dte_nc.html'
		dte = DTECliente.objects.get(codigoGeneracion=codigo)
		receptor = Cliente.objects.get(codigo=dte.receptor_id)
		dte_detalle = DTEClienteDetalle.objects.filter(dte=dte)

	if tipo == '06':
		template_name = 'plantillas/dte_nd.html'
		dte = DTECliente.objects.get(codigoGeneracion=codigo)
		receptor = Cliente.objects.get(codigo=dte.receptor_id)
		dte_detalle = DTEClienteDetalle.objects.filter(dte=dte)

	if tipo == '11':
		template_name = 'plantillas/dte_fex.html'
		dte = DTECliente.objects.get(codigoGeneracion=codigo)
		receptor = Cliente.objects.get(codigo=dte.receptor_id)
		dte_detalle = DTEClienteDetalle.objects.filter(dte=dte)

	if tipo == '14':
		template_name = 'plantillas/dte_fse.html'
		dte = DTEProveedor.objects.get(codigoGeneracion=codigo)
		receptor = Proveedor.objects.get(codigo=dte.receptor_id)
		dte_detalle = DTEProveedorDetalle.objects.filter(dte=dte)

	letras = CantLetras(dte.totalPagar)
	fecha = dte.fecEmi.strftime("%d/%m/%Y")
	
	logo = request.session['logo']
	qr = f'https://almacendte.blob.core.windows.net/empresas/{emisor.codigo}/{dte.codigoGeneracion}.png'
	
	context = {'dte':dte, 'emisor':emisor, 'receptor':receptor, 'dte_detalle':dte_detalle, 'letras':letras, 'logo':logo, 'qr':qr, 'fecha':fecha}
	template = get_template(template_name)
	html = template.render(context)
	config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)

	pdf = pdfkit.from_string(html, False, configuration=config, options=options)
	#pdf = pdfkit.from_string(html, False, options=options)

	# Generate download
	response = HttpResponse(pdf, content_type='application/pdf')

	#response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
	# print(response.status_code)
	if response.status_code != 200:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response
	
def cerrar_sesion(request):
    logout(request)
    return redirect('manager:login')	


def direcciones(request):
	#messages.success(request, 'settings.PROJECT_DIR: ' + settings.PROJECT_DIR)
	#messages.success(request, 'settings.STATIC_ROOT: ' + settings.STATIC_ROOT)
	#messages.success(request, 'settings.STATIC_DIR: ' + settings.STATIC_DIR)
	#messages.success(request, 'settings.STATIC_URL: ' + settings.STATIC_URL)
	#messages.success(request, 'settings.MEDIA_URL: ' + settings.MEDIA_URL)
	#messages.success(request, 'settings.MEDIA_ROOT: ' + settings.MEDIA_ROOT)
	#messages.success(request, 'os.name: ' + os.name)
	dominio = request.build_absolute_uri('/')
	ruta_logo = f'https://alfadte.azurewebsites.net/media/logos/{request.session['empresa']}.png'
	context={
			'BASE_DIR': settings.BASE_DIR,
			'PROJECT_DIR':settings.PROJECT_DIR, 'STATIC_ROOT': 'settings.STATIC_ROOT', 
			'STATIC_DIR':settings.STATIC_DIR,
			'STATIC_DIR_IMG': os.path.join(settings.STATIC_DIR,'clientes','logos', f'{request.session['empresa']}.png'),
			'STATIC_URL':settings.STATIC_URL,
			'STATIC_URL_IMG': os.path.join(settings.STATIC_URL,'clientes','logos', f'{request.session['empresa']}.png'),
			'MEDIA_URL':settings.MEDIA_URL,
			'MEDIA_ROOT':settings.MEDIA_ROOT,
			'osName': os.name,
			'imagen': '',
			'logo': request.session['empresa'] + '.png',
			'url': dominio,
			'imagen_MEDIA': ruta_logo,
	}

	return render(request, 'dte/direcciones.html', context)


def cdn(request):
	context = {}
	if request.method=='POST':
		res = subir()
		messages.info(request, res)
		context = {'res':res}
		return render(request, 'dte/cdn.html', context)
	
	return render(request, 'dte/cdn.html', context)


def verCorreo(request, tipo, codigo):
	datos = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	empresa = get_object_or_404(Empresa, codigo=datos.emisor.codigo)
	logo = request.session['logo']
	enlace = f'https://admin.factura.gob.sv/consultaPublica?ambiente={empresa.ambiente.codigo}&codGen={datos.codigoGeneracion}&fechaEmi={datos.fecEmi.strftime("%Y-%m-%d")}'
	context={'datos':datos, 'logo':logo, 'enlace':enlace}
	return render(request, 'plantillas/correo_receptor.html', context)


def correoACliente(request, tipo, codigo, reenvio):
	enviar = enviarCorreo(request, tipo=tipo, codigo=codigo)
	if reenvio == 's':
		BitacoraDTE(request=request, usuario=request.user, dte=codigo, tipo=tipo, accion=4)
		messages.success(request, 'Correo enviado')
	return redirect('dte:actualizar', tipo=tipo, pk=codigo)

def pruebas(request):
	empresa = get_object_or_404(Empresa, codigo = request.session['empresa'])
	context = {'empresa':empresa}
	return render(request, 'dte/pruebas.html', context)

def enviarPrueba(request, tipo):
	res = gen_prueba(request, tipo=tipo, empresa=request.session['empresa'])
	#messages.success(request, res)
	return redirect('dte:firmardte', tipo=tipo, codigo=res)
	#return redirect('dte:enviar_mh', tipo=tipo, codigo=res)
	#messages.success(request, res)

	#return redirect('dte:prueba')

def invalidarDte(request, tipo, codigo):
	cod_anulacion = CodGeneracion()
	if tipo in {'07','14'}:
		dte = get_object_or_404(DTEProveedor, codigoGeneracion = codigo)
		receptor_instance = get_object_or_404(Proveedor, codigo=dte.receptor_id)
	else:
		dte = get_object_or_404(DTECliente, codigoGeneracion = codigo)
		receptor_instance = get_object_or_404(Cliente, codigo=dte.receptor_id)

	tipoI = get_object_or_404(TipoInvalidacion, codigo=2)
	emisor_instance = get_object_or_404(Empresa, codigo=request.session['empresa'])
	tipoDocumento_instance = get_object_or_404(TipoDocumento, codigo=dte.tipoDte_id)
	tipoInvalidacion_instance = get_object_or_404(TipoInvalidacion, codigo=2)
	estado = get_object_or_404(EstadoDTE, codigo='003')
	invalidado = DTEInvalidacion(codigoGeneracion = cod_anulacion,
		emisor = emisor_instance,
		receptor_tmp = dte.receptor_id,
		codigoDte = dte.codigoGeneracion,
		tipoDte = tipoDocumento_instance,
		fechaEmision = datetime.now(),
		tipoInvalidacion = tipoInvalidacion_instance,
		docfirmado='',
		selloRecepcion='')
	invalidado.save()
	dte.estadoDte = estado
	dte.save()
	BitacoraDTE(request, usuario=request.user, dte=codigo, tipo=tipo, accion=5)
	json = genJson(codigo=codigo, tipo='anulacion', empresa=request.session['empresa'], codigo_anulacion=cod_anulacion)
	firma = firmar(codigo=codigo, cod_anulacion=cod_anulacion, tipo='anulacion')

	#messages.success(request, json)

	#return redirect('dte:actualizar', pk=codigo)
	#messages.info(request, cod_anulacion)
	return redirect('dte:enviar_mh_anulacion', tipo='anulacion', cod_anulacion=cod_anulacion)


def cliente_auto_registro(request, cod_empresa):
	config = Configuracion.objects.all().first()
	codigo = CodGeneracion().upper()
	logo = config.blobUrl + 'empresas/logos/' + cod_empresa + '_logo.png'
	empresa = get_object_or_404(Empresa, codigo=cod_empresa)
	if request.method == 'POST':
		form = ClienteForm(request.POST)
		form.instance.empresa = empresa
		if form.is_valid():
			cliente = form.save()
			return redirect('dte:registro_de_cliente_gracias', cod_empresa=cod_empresa)
	else:		
		form = ClienteForm(initial = {
			'codigo':codigo,
			'pais':'9300',
			'tipoDocumentoCliente':'36',
			'actividadEconomica':'10005',
			'tipoContribuyente':'003'}
		)
	return render(request, 'dte/registro_de_cliente.html', {'form': form, 'logo':logo, 'empresa':empresa})


def registro_de_cliente_gracias(request, cod_empresa):
	config = Configuracion.objects.all().first()
	logo = config.blobUrl + 'empresas/logos/' + cod_empresa + '_logo.png'
	return render(request, 'dte/registro_de_cliente_gracias.html', {'logo':logo})


def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)


def bitacoraDte(request, codigo):
	bitacora = BitacoraAccionDte.objects.filter(dte = codigo)
	context = {'bitacora':bitacora}
	return render(request, 'dte/bitacoraDte.html', context)