import os, json, requests, base64, pdfkit, wkhtmltopdf
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.paginator import Paginator
from django.db.models import F, Q, Sum, ExpressionWrapper, DecimalField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from .funciones import CodGeneracion, Correlativo, getUrl, genJson, gen_qr, CantLetras
from .models import Empresa, DTECliente, DTEClienteDetalle, DTEClienteDetalleTributo, DtesEmpresa, TipoDocumento, Cliente, TributoResumen, Producto
from wkhtmltopdf.main import WKhtmlToPdf
wkhtml_to_pdf = os.path.join(settings.BASE_DIR, "wkhtmltopdf.exe")

@login_required(login_url='manager:login')
def index(request):
	#messages.success(request, 'settings.PROJECT_DIR: ' + settings.PROJECT_DIR)
	#messages.success(request, 'settings.STATIC_ROOT: ' + settings.STATIC_ROOT)
	#messages.success(request, 'settings.STATIC_DIR: ' + settings.STATIC_DIR)
	#messages.success(request, 'settings.STATIC_URL: ' + settings.STATIC_URL)
	#messages.success(request, 'settings.MEDIA_URL: ' + settings.MEDIA_URL)
	#messages.success(request, 'settings.MEDIA_ROOT: ' + settings.MEDIA_ROOT)
	request.session['empresa'] = request.user.userprofile.empresa.codigo
	list_docs = DtesEmpresa.objects.filter(empresa=request.session['empresa'])
	documentos = list_docs.select_related('dte').values('id', 'empresa_id', 'dte_id', nombre_documento=F('dte__nombre'))
	request.session['documentos'] = list(documentos)
	context = {'listaDocumentos':documentos}
	#messages.success(request, request.session['empresa'])
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
			return redirect('dte:perfil_usuario')  # Reemplaza 'profile' con el nombre de la URL de la página de perfil del usuario
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
			datos.save()

			messages.success(request, 'Respuesta del Ministerio: ' + respuesta_json['status'])

			return redirect('dte:index')
		else:
			return HttpResponse('Ocurrió un error durante la autenticación')	

	else:
		return HttpResponse('Solicitud incorrecta')



@login_required(login_url='manager:login')
def lista_dte(request, tipo):
	if tipo == 'cliente':
		dtes = DTECliente.objects.filter(emisor=request.session['empresa'])
	elif tipo == 'proveedor':
		pass
	
	paginator = Paginator(dtes, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	return render(request, 'dte/lista_dte.html', {'dtes':dtes, 'listaDocumentos':request.session['documentos'], 'page_obj': page_obj})


@login_required(login_url='manager:login')
def lista_cliente(request):
	clientes = Cliente.objects.filter(empresa_id=request.session['empresa'])
	paginator = Paginator(clientes, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	return render(request, 'dte/lista_clientes.html', {'clientes': page_obj, 'listaDocumentos':request.session['documentos']})
	
	

@login_required(login_url='manager:login')
def lista_producto(request):
	productos = Producto.objects.filter(empresa=request.session['empresa'])
	paginator = Paginator(productos, 10)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	return render(request, 'dte/lista_producto.html', {'productos':page_obj, 'listaDocumentos':request.session['documentos'], 'page_obj': page_obj})


class DTEInline():
	form_class = DTEForm
	model = DTECliente
	template_name = 'dte/dte_create_or_update.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cliente_frm = ClienteForm(initial=dict(codigo=CodGeneracion(), tipoDocumentoCliente= '13', 
			empresa = self.request.user.userprofile.empresa.codigo, actividadEconomica='10005', pais='9300',
			tipoContribuyente='002', tipoPersona=1))
		context['listaDocumentos'] = self.request.session.get('documentos', [])
		context['cliente_frm'] = cliente_frm
		return context

	def form_valid(self, form):
		named_formsets = self.get_named_formsets()
		#messages.success(self.request, {'named_formsets': named_formsets})

		if not all((x.is_valid() for x in named_formsets.values())):
			messages.warning(self.request, 'No se pudo guardar el DTE, por favor revise los datos')
			return self.render_to_response(self.get_context_data(form=form))
		self.object = form.save()

		# for every formset, attempt to find a specific formset save function
        # otherwise, just save.
		for name, formset in named_formsets.items():
			formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
			#messages.success(self.request, {'formset_save_func': formset_save_func})
			if formset_save_func is not None:
				formset_save_func(formset)
			else:
				formset.save()
		qr = gen_qr(codigo=self.object.codigoGeneracion, empresa=self.object.emisor_id)
		json = genJson(codigo=self.object.codigoGeneracion, tipo=self.object.tipoDte.codigo, empresa=self.object.emisor_id)
		messages.success(self.request, 'Documento guardado')
		#return redirect('dte:lista_dte', tipo='cliente')
		return redirect('dte:actualizar', pk=self.object.codigoGeneracion)

	def formset_detalles_valid(self, formset):
		detalles = formset.save(commit=False)
		#for obj in formset.deleted_objects:
		#	obj.delete()
		for detalle in detalles:
			detalle.dte = self.object
			detalle.save()

			# Inicio de cálculos
			total_gravada = DTEClienteDetalle.objects.filter(dte_id=detalle.dte_id).aggregate(total_gravada=Sum(F('ventaGravada')))['total_gravada']
			DTECliente.objects.filter(codigoGeneracion=detalle.dte_id).update(totalGravada=total_gravada,
				subTotalVentas=total_gravada,
				subTotal=total_gravada,
				ivaPerci1=float(total_gravada)*float(0.13),
				montoTotalOperacion=float(total_gravada)*float(1.13),
				totalPagar=float(total_gravada)*float(1.13))
			# Fin de cálculos

			instancia1 = DTEClienteDetalle.objects.get(codigoDetalle = detalle.codigoDetalle)
			instancia2 = TributoResumen.objects.get(codigo='20')
			t = DTEClienteDetalleTributo(codigoDetalle=instancia1, codigo=instancia2, descripcion=instancia2.nombre, valor=5.0)
			t.save()
		messages.success(self.request, 'Detalle guardado')



class DTECreate(DTEInline, CreateView):
	def get_initial(self):
		initial = super().get_initial()
		codigo = self.kwargs.get('pk')
		tipo_documento = get_object_or_404(TipoDocumento, codigo=codigo)
		session_key = self.request.session.session_key
		session_store = SessionStore(session_key=session_key)
		empresa = self.request.session['empresa']

		initial['codigoGeneracion'] = CodGeneracion().upper()
		initial['emisor'] = self.request.session['empresa']
		initial['tipoDte'] = tipo_documento

		return initial

	def get_context_data(self, **kwargs):
		ctx = super(DTECreate, self).get_context_data(**kwargs)
		nombreTipoDoc = TipoDocumento.objects.get(codigo=self.kwargs.get('pk'))
		ctx['TipoDocumento'] = nombreTipoDoc
		ctx['named_formsets'] = self.get_named_formsets()
		ctx['empresa'] = self.request.session['empresa']
		ctx['codigoDetalle'] = CodGeneracion()
		return ctx

	def get_named_formsets(self):
		if self.request.method == 'GET':
			return {
				'detalles' : DTEClienteDetalleFormSet(prefix='detalles')
			}
		else:
			return {
				'detalles' : DTEClienteDetalleFormSet(self.request.POST or None, self.request.FILES or None, prefix='detalles'),
			}

			#messages.success(self.request, DTEClienteDetalleFormSet(prefix='detalles')) #Borrar


class DTEUpdate(DTEInline, UpdateView):
	def get_context_data(self, **kwargs):
		ctx = super(DTEUpdate, self).get_context_data(**kwargs)
		nombreTipoDoc = get_object_or_404(DTECliente, codigoGeneracion=self.kwargs.get('pk'))
		ctx['TipoDocumento'] = nombreTipoDoc.tipoDte
		ctx['named_formsets'] = self.get_named_formsets()
		#messages.success(self.request, {'DTEUpdate: ':'update', 'ctx':ctx})
		return ctx

	def get_named_formsets(self):
		#messages.success(self.request, {'DTEUpdate: ':self.request})
		return {
		'detalles': DTEClienteDetalleFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='detalles')
		}


def autocompletar_producto(request):
	term = request.GET.get('term')
	productos = Producto.objects.filter(nombre__icontains=term).values_list('nombre', flat=True)
	return JsonResponse(list(productos), safe=False)

@login_required(login_url='manager:login')
def eliminar_detalle(request, pk):
	try:
		detalle = DTEClienteDetalle.objects.get(codigoDetalle=pk)
	except DTEClienteDetalle.DoesNotExist:
		messages.success(
			request, 'Objeto no existe'
			)
		return redirect('dte:actualizar', pk=detalle.dte.codigoGeneracion)

	detalle.delete()

	messages.success(
		request, 'Detalle eliminado con éxito'
		)

	return redirect('dte:actualizar', pk=detalle.dte.codigoGeneracion)



@login_required(login_url='manager:login')
def firmarDte(request, codigo, tipo):
	if tipo in {'01','03'}:
		dte = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	
	emisor = Empresa.objects.get(codigo=dte.emisor_id)
	usuariomh = emisor.usuarioMH
	pwd = emisor.passwordPri

	archivo = os.path.join(settings.STATIC_DIR, emisor.codigo, f'{codigo}.json').replace('/', '\\')
	
	with open(archivo, 'rb') as file:
		json_data = json.load(file)

	firma_url = getUrl(request.session['empresa'], 'Firmadodte')

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

	headers = {'content-Type': 'application/JSON'}
	response = requests.post(firma_url, json=data, headers=headers)

	if response.status_code == 200:
		response_data = json.loads(response.text)
		status_value = response_data.get("status", None)
		body_value = response_data.get("body", None)

		if tipo in {'01','03','04','05','06','08','09','11','14','15'}:
			guardar_firma = DTECliente.objects.get(codigoGeneracion=codigo)
			guardar_firma.docfirmado = body_value
			guardar_firma.save()
		elif tipo in {'07'}:
			pass

		with open(archivo, 'r') as json_file:
			data = json.load(json_file)

		try:
			with open(archivo, 'r') as json_file:
					contenido_actual = json.load(json_file)
		except FileNotFoundError:
			contenido_actual = {}

		contenido_actual['token'] = body_value

		#return redirect('dte:index')
		return redirect('dte:actualizar', pk=codigo)
		#return JsonResponse(data1)
	else:
		return JsonResponse({'resp':data, 'codigo':response.status_code, 'url':firma_url})



@login_required(login_url='manager:login') ########### Borrar #############
def cliente_detail(request, pk):
	cliente = get_object_or_404(Cliente, pk=pk)
	return render(request, 'dte/cliente_detalle.html', {'cliente': cliente, 'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login')
def cliente_create(request):
	codigo = CodGeneracion().upper()
	if request.method == 'POST':
		form = ClienteForm(request.POST)
		if form.is_valid():
			cliente = form.save()
			return redirect('dte:cliente_update', pk=cliente.pk)
	else:		
		form = ClienteForm(initial = {'codigo':codigo, 'pais':'9300','tipoDocumentoCliente':'13' , 'actividadEconomica':'10005', 'tipoContribuyente':'002'})
	return render(request, 'dte/cliente_detalle.html', {'form': form,'listaDocumentos':request.session['documentos']})


@login_required(login_url='manager:login')
def producto(request, pk=None):
	if pk:
		producto = get_object_or_404(Producto, codigo=pk)
	else:
		producto = None

	if request.method=='POST':
		form = ProductoForm(request.POST, instance=producto)
		if form.is_valid():
			producto = form.save()
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
		'no-outline': None
	}

	emisor = Empresa.objects.get(codigo = request.session['empresa'])
		
	if tipo == '01':
		template_path = 'plantillas/dte_fcf.html'
		Dte = DTECliente.objects.filter(codigoGeneracion = codigo).annotate(
			totalExentaIVA = ExpressionWrapper(F('totalExenta') * 1.13, output_field = DecimalField()),
			totalGravadaIVA = ExpressionWrapper(F('totalGravada') * 1.13, output_field = DecimalField()),
			subTotalVentasIVA = ExpressionWrapper(F('subTotalVentas') * 1.13, output_field = DecimalField()),
			totalPagarIVA = ExpressionWrapper(F('totalPagar'), output_field = DecimalField())
		).first()
		receptor = Cliente.objects.get(codigo = Dte.receptor_id)
		DteDetalle = DTEClienteDetalle.objects.filter(dte = Dte).annotate(
			precio_con_iva = ExpressionWrapper(F('precioUni') * 1.13, output_field = DecimalField()),
			subt_precio_con_iva = ExpressionWrapper(F('ventaGravada') * 1.13, output_field = DecimalField())
		)

	letras = CantLetras(Dte.totalPagar)
	fecha = Dte.fecEmi.strftime("%d/%m/%Y")

	context={'dte':Dte,'emisor':emisor, 'receptor':receptor, 'dte_detalle':DteDetalle, 'letras':letras, 'qr':'qr', 'fecha':fecha}

	template = get_template(template_path)
	html = template.render(context)
	config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)
	pdf = pdfkit.from_string(html, False, configuration=config, options=options)

	# Generate download
	response = HttpResponse(pdf, content_type='application/pdf')

	#response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
	# print(response.status_code)
	if response.status_code != 200:
		return HttpResponse('Huston!, We had some errors <pre>' + html + '</pre>')
	return response


def cerrar_sesion(request):
    logout(request)
    return redirect('manager:login')	