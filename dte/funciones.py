import os, json, uuid, math, pdfkit, qrcode, requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F, Q, Sum, ExpressionWrapper, DecimalField
from django.template.loader import render_to_string, get_template
from .models import *
from .jsons import fcf, ccf, nc, nd, fex, fse, anulacion, contingencia
from .jsons_pruebas import fcf_p, ccf_p, nc_p, nd_p, fex_p, fse_p
from .guardarBlob import subirArchivo
from datetime import datetime, timedelta, timezone
from num2words import num2words

if os.name == 'posix':
	wkhtml_to_pdf = os.path.join(settings.BASE_DIR, "wkhtmltopdf")
else:
	wkhtml_to_pdf = os.path.join(settings.BASE_DIR, "wkhtmltopdf.exe")

def Correlativo(cod_empresa, cod_tipo):
	try:
		# Obtener el registro de ControlDocumento, si no existe, crearlo
		registro = ControlDocumento.objects.get(empresa=cod_empresa, tipo=cod_tipo)

		registro.numeroactual += 1
		registro.save()

		actual = registro.numeroactual

		return f"DTE-{cod_tipo}-00000000-{str(actual).zfill(15)}"

	except ControlDocumento.DoesNotExist:
		#return "Error: Registro no encontrado para empresa {} y tipo {}".format(cod_empresa, cod_tipo)
		return "Error"

	except Exception as e:
		# Manejar cualquier otra excepción que pueda ocurrir
		return "Error: {}".format(str(e))

def CodGeneracion():
	guuid = str(uuid.uuid4()).upper()
	return guuid

def getUrl(empresa, tipo):
	emp = Empresa.objects.get(codigo=empresa)
	ambiente = emp.ambiente
	url = UrlSistema.objects.get(tipo=tipo, ambiente=ambiente)
	#messages.info(request, {'emp':emp, 'ambiente':ambiente, 'tipo':tipo})

	return url.url


def genJson(codigo, tipo, empresa, codigo_anulacion=None, codigo_contingencia=None):
	dato_empresa = get_object_or_404(Empresa, codigo=empresa)
	archivo = {}
	if tipo == '01':
		json_data = fcf(codigo)
	elif tipo == '03':
		json_data = ccf(codigo)
	elif tipo == '05':
		json_data = nc(codigo)
	elif tipo == '06':
		json_data = nd(codigo)
	elif tipo == '11':
		json_data = fex(codigo)
	elif tipo == '14':
		json_data = fse(codigo)
	elif tipo == 'anulacion':
		json_data = anulacion(codAnulacion=codigo_anulacion, codigoDte=codigo)
	elif tipo == 'contingencia':
		json_data = contingencia(codigo)

	#qr_folder = os.path.join(settings.STATIC_DIR,'clientes', empresa, dato_empresa.codigo)
	if tipo == 'anulacion':
		ruta_archivo = os.path.join(settings.STATIC_DIR,'clientes', empresa, f'{codigo_anulacion}.json')
	else:
		ruta_archivo = os.path.join(settings.STATIC_DIR,'clientes', empresa, f'{codigo}.json')

	with open(ruta_archivo, 'w') as json_file:
		json.dump(json_data, json_file, indent=2, ensure_ascii=False)

	if tipo == 'anulacion':
		subirArchivo(empresa, f'{codigo_anulacion}.json')
	else:
		subirArchivo(empresa, f'{codigo}.json')

	return ruta_archivo
	#return ruta_archivo

def gen_prueba(request, tipo, empresa):
	codigo=CodGeneracion()
	#messages.success(request, 'Prueba generada: ' + tipo)
	if tipo=='01':
		json_data = fcf_p(empresa, codigo)
	if tipo=='03':
		json_data = ccf_p(empresa, codigo)
	if tipo=='05':
		json_data = nc_p(empresa, codigo)
	if tipo=='06':
		json_data = nd_p(empresa, codigo)
	if tipo=='11':
		json_data = fex_p(empresa, codigo)
	if tipo=='14':
		json_data = fse_p(empresa, codigo)

	ruta_archivo = os.path.join(settings.STATIC_DIR,'clientes', empresa, f'{codigo}.json')
	#messages(request, ruta_archivo)
	with open(ruta_archivo, 'w') as json_file:
		json.dump(json_data, json_file, indent=2, ensure_ascii=False)

	return codigo

def genQr(codigo, empresa):
	dato_empresa = get_object_or_404(Empresa, codigo=empresa)
	ambiente = dato_empresa.ambiente_id
	empresa = dato_empresa.codigo
	fecha = datetime.now().strftime('%Y-%m-%d')
	url = f'https://admin.factura.gob.sv/consultaPublica?ambiente={ambiente}&codGen={codigo}&fechaEmi={fecha}'
	qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
	qr.add_data(url)
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	qr_folder = os.path.join(settings.STATIC_DIR,'clientes', empresa)

	if not os.path.exists(qr_folder):
		os.makedirs(qr_folder)

	img_path = os.path.join(qr_folder, f'{codigo}.png')
	img.save(img_path)

	subirArchivo(empresa, f'{codigo}.png')

	return HttpResponse('ok')


def genPdf(codigo, tipo, empresa):
	config = Configuracion.objects.all().first()
	options = {
		'page-size': 'Letter',
		'page-height': "11in",
		'page-width': "8.5in",
		'margin-top': '0.5in',
		'margin-right': '0.5in',
		'margin-bottom': '0.5in',
		'margin-left': '0.5in',
		'encoding': "UTF-8"
	}

	template_path = ''
	emisor = Empresa.objects.get(codigo=empresa)
	codigo = codigo

	#dte = DTECliente.objects.get(codigoGeneracion = codigo)	
	#receptor = Cliente.objects.get(codigo = dte.receptor_id)
	
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
	
	logo = f'{config.blobUrl}{config.blobContenedor}/logos/{emisor.codigo}_logo.png'
	qr = f'{config.blobUrl}{config.blobContenedor}/{emisor.codigo}/{dte.codigoGeneracion}.png'
	
	context = {'dte':dte, 'emisor':emisor, 'receptor':receptor, 'dte_detalle':dte_detalle, 'letras':letras, 'logo':logo, 'qr':qr, 'fecha':fecha}
	template = get_template(template_name)
	html = template.render(context)

	config = pdfkit.configuration(wkhtmltopdf=wkhtml_to_pdf)

	pdf = pdfkit.from_string(html, False, configuration=config, options=options)

	pdf_nombre = codigo + '.pdf'
	
	pdf_path = os.path.join(settings.STATIC_DIR,'clientes', empresa, pdf_nombre)

	with open(pdf_path, 'wb') as pdf_file:
		pdf_file.write(pdf)

	# Generar respuesta para la descarga
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename="{pdf_nombre}"'

	# Leer el PDF desde el archivo y escribirlo en la respuesta
	with open(pdf_path, 'rb') as pdf_file:
		response.write(pdf_file.read())

	subirArchivo(empresa, f'{codigo}.pdf')

	if response.status_code==200:
		respuesta = 'PDF generado: ' + logo
	else:
		respuesta = response

	return respuesta


def firmar(codigo, tipo, cod_anulacion=None):
	if tipo in {'01','03','05','06','11'}:
		dte = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	elif tipo in {'07','14'}:
		dte = get_object_or_404(DTEProveedor, codigoGeneracion=codigo)
	elif tipo == 'anulacion':
		dte = get_object_or_404(DTEInvalidacion, codigoGeneracion=cod_anulacion)
	elif tipo == 'contingencia':
		dte = get_object_or_404(DTEContingencia, codigoGeneracion=codigo)
	
	emisor = Empresa.objects.get(codigo=dte.emisor_id)
	usuariomh = emisor.usuarioMH
	pwd = emisor.passwordPri

	if os.name == 'posix':
		archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{cod_anulacion if cod_anulacion else codigo}.json')
	else:
		archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{cod_anulacion if cod_anulacion else codigo}.json').replace('\\', '/')
	
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

	headers = {'content-Type': 'application/JSON'}
	response = requests.post(firma_url, json=data, headers=headers)

	if response.status_code == 200:
		response_data = json.loads(response.text)
		status_value = response_data.get("status", None)
		body_value = response_data.get("body", None)

		if tipo in {'01','03','04','05','06','08','09','11','15'}:
			guardar_firma = DTECliente.objects.get(codigoGeneracion=codigo)
			guardar_firma.docfirmado = body_value
			guardar_firma.save()
		elif tipo in {'07','14'}:
			guardar_firma = DTEProveedor.objects.get(codigoGeneracion=codigo)
			guardar_firma.docfirmado = body_value
			guardar_firma.save()
		elif tipo == 'anulacion':
			guardar_firma = DTEInvalidacion.objects.get(codigoGeneracion=cod_anulacion)
			guardar_firma.docfirmado = body_value
			guardar_firma.save()
		elif tipo == 'contingencia':
			guardar_firma = DTEContingencia.objects.get(codigoGeneracion=codigo)
			guardar_firma.docfirmado = body_value
			guardar_firma.save()

		with open(archivo, 'r') as json_file:
			data = json.load(json_file)

		try:
			with open(archivo, 'r') as json_file:
					contenido_actual = json.load(json_file)
		except FileNotFoundError:
			contenido_actual = {}

		contenido_actual['token'] = body_value

		#return redirect('dte:index')
		#return redirect('dte:actualizar', pk=codigo)
		return JsonResponse(response_data)
	else:
		return JsonResponse({'resp':data, 'codigo':response.status_code, 'url':firma_url})


def CantLetras(cantidad):
	letras = ''

	p_decimal, p_entero = math.modf(cantidad)
	p_decimal = int(round(p_decimal, 2) * 100)
	if len(str(p_decimal)) == 1:
		p_decimal = "0" + str(p_decimal)

	letras = (num2words(p_entero, lang='es') + " " + str(p_decimal) + u"/100 USD")

	return letras.upper()


def datosInicio(pk):
	empresa = get_object_or_404(Empresa, codigo=pk)
	# Obtener la fecha actual
	fecha_actual = datetime.now().date()
	primer_dia_mes = fecha_actual.replace(day=1)

	# Contar el número de registros con la fecha 'fecEmi' igual a la fecha actual
	num_registros_hoy = DTECliente.objects.filter(emisor=empresa, fecEmi__date=fecha_actual, ambiente=empresa.ambiente, estadoDte='002').count()

	# Sumar el campo 'subTotalVentas' de los registros que coincidan con la fecha actual
	subtotal_hoy = DTECliente.objects.filter(emisor=empresa, fecEmi__date=fecha_actual, ambiente=empresa.ambiente, estadoDte='002').aggregate(total_subtotal=models.Sum('subTotalVentas'))['total_subtotal']

	# Contar el número de registros con la fecha 'fecEmi' en el mes en curso
	num_registros_mes = DTECliente.objects.filter(emisor=empresa, fecEmi__month=fecha_actual.month, fecEmi__year=fecha_actual.year, ambiente=empresa.ambiente, estadoDte='002').count()

	# Sumar el campo 'subTotalVentas' de los registros con la fecha 'fecEmi' en el mes en curso
	subtotal_mes = DTECliente.objects.filter(emisor=empresa, fecEmi__gte=primer_dia_mes, ambiente=empresa.ambiente_id, estadoDte='002').aggregate(total_subtotal=models.Sum('subTotalVentas'))['total_subtotal']

	num_registros_hoy = num_registros_hoy or 0
	subtotal_hoy = subtotal_hoy or 0
	num_registros_mes = num_registros_mes or 0
	subtotal_mes = subtotal_mes or 0

	return num_registros_hoy, subtotal_hoy, num_registros_mes, subtotal_mes


def BitacoraDTE(request, usuario, dte, tipo, accion):
	tz = timezone(timedelta(hours=-6))
	fecha_actual = datetime.now(tz=tz)
	empresa = get_object_or_404(Empresa, codigo=request.session['empresa'])
	tipoDte = get_object_or_404(TipoDocumento, codigo=tipo)
	accionBitacora = get_object_or_404(TipoAccionUsuario, id=accion)
	
	bitacora = BitacoraAccionDte(
		empresa = empresa,
		usuario = usuario,
		dte = dte,
		tipoDte = tipoDte,
		fecha = datetime.now(),
		accion = accionBitacora
	)

	bitacora.save()

	return 'Guardado'