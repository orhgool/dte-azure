import os, json, uuid, math, pdfkit, qrcode, requests
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F, Q, Sum, ExpressionWrapper, DecimalField
from django.template.loader import render_to_string, get_template
from .models import *
from .jsons import fcf, ccf
from datetime import datetime, timedelta
from num2words import num2words

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

	return url.url


def genJson(codigo, tipo, empresa):
	dato_empresa = get_object_or_404(Empresa, codigo=empresa)
	archivo = {}
	if tipo=='01':
		json_data = fcf(codigo)
	elif tipo == '03':
		json_data = ccf(codigo)

	#qr_folder = os.path.join(settings.STATIC_DIR,'clientes', empresa, dato_empresa.codigo)
	ruta_archivo = os.path.join(settings.STATIC_DIR,'clientes', empresa, f'{codigo}.json')

	with open(ruta_archivo, 'w') as json_file:
		json.dump(json_data, json_file, indent=2, ensure_ascii=False)

	return ruta_archivo
	#return ruta_archivo


def gen_qr(codigo, empresa):
	dato_empresa = get_object_or_404(Empresa, codigo=empresa)
	ambiente = dato_empresa.ambiente_id
	empresa = dato_empresa.codigo
	fecha = datetime.now().strftime('%Y-%m-%d')
	url = f'https://admin.factura.gob.sv/consultaPublica?ambiente={ambiente}&codGen={codigo}&fechaEmi={fecha}'
	qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
	qr.add_data(url)
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	qr_folder = os.path.join(settings.STATIC_DIR,'clientes', empresa)

	if not os.path.exists(qr_folder):
		os.makedirs(qr_folder)

	img_path = os.path.join(qr_folder, f'{codigo}.png')
	img.save(img_path)

	return HttpResponse('ok')



def firmar(codigo, tipo):
	if tipo in {'01','03'}:
		dte = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	
	emisor = Empresa.objects.get(codigo=dte.emisor_id)
	usuariomh = emisor.usuarioMH
	pwd = emisor.passwordPri

	if os.name == 'posix':
		archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{codigo}.json')
	else:
		archivo = os.path.join(settings.STATIC_DIR,'clientes', emisor.codigo, f'{codigo}.json').replace('\\', '/')
	
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
	num_registros_hoy = DTECliente.objects.filter(emisor=empresa, fecEmi__date=fecha_actual).count()

	# Sumar el campo 'subTotalVentas' de los registros que coincidan con la fecha actual
	subtotal_hoy = DTECliente.objects.filter(emisor=empresa, fecEmi__date=fecha_actual).aggregate(total_subtotal=models.Sum('subTotalVentas'))['total_subtotal']

	# Contar el número de registros con la fecha 'fecEmi' en el mes en curso
	num_registros_mes = DTECliente.objects.filter(emisor=empresa, fecEmi__month=fecha_actual.month, fecEmi__year=fecha_actual.year).count()

	# Sumar el campo 'subTotalVentas' de los registros con la fecha 'fecEmi' en el mes en curso
	subtotal_mes = DTECliente.objects.filter(emisor=empresa, fecEmi__gte=primer_dia_mes).aggregate(total_subtotal=models.Sum('subTotalVentas'))['total_subtotal']

	dato1 = fecha_actual.month
	dato2 = 'fecha_actual.replace(day=1)'


	return num_registros_hoy, subtotal_hoy, num_registros_mes, subtotal_mes, dato1, dato2