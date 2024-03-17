from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import *
from datetime import datetime

def replace_in_dict(obj, find, replace):
	if isinstance(obj, str):
		return obj.replace(find, replace)
	elif isinstance(obj, dict):
		return {key: replace_in_dict(value, find, replace) for key, value in obj.items()}
	elif isinstance(obj, list):
		return [replace_in_dict(item, find, replace) for item in obj]
	else:
		return obj

def fcf(codigo, ambiente):
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}

	dte = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	emisor = Empresa.objects.get(codigo=dte.emisor_id)
	datos_identificacion = {'codigoGeneracion':codigo, 'tipo':dte.tipoDte, 'version':dte.version}
	

	identificacion_data = {
			'version': dte.version,
			'ambiente': dte.ambiente,
			'tipoDte': dte.tipoDte.codigo,
			'numeroControl': dte.numeroControl,
			'codigoGeneracion': dte.codigoGeneracion,
			'tipoModelo': int(dte.tipoModelo_id),
			'tipoOperacion': int(dte.tipoTransmision_id),
			'tipoContingencia': None,
			'motivoContin': None,
			'fecEmi': dte.fecEmi.strftime("%Y-%m-%d"),
			'horEmi': dte.fecEmi.strftime("%H:%M:%S"),
			'tipoMoneda': 'USD'
		}

	emisor_data = {'nit': emisor.nit, 'nrc': emisor.nrc,
					'nombre': emisor.razonsocial,
					'codActividad': emisor.actividadeconomica_id, 
					'descActividad': emisor.actividadeconomica.descripcion,
					'nombreComercial': emisor.nombrecorto,
					'tipoEstablecimiento': emisor.tipoEstablecimiento,
					'direccion': {'departamento':emisor.departamento_id, 'municipio':emisor.municipio.codigo, 'complemento':emisor.direccion},

					'telefono': emisor.telefono,
					'correo': emisor.correo,
					'codEstableMH': emisor.codEstableMH,
					'codEstable': emidor.codEstable,
					'codPuntoVentaMH': None,
					'codPuntoVenta': None
					}

	json_data = {
			'identificacion': identificacion_data,
			'emisor': emisor_data,
		}

	json_data = replace_in_dict(json_data, 'á', 'a')
	json_data = replace_in_dict(json_data, 'é', 'e')
	json_data = replace_in_dict(json_data, 'í', 'i')
	json_data = replace_in_dict(json_data, 'ó', 'o')
	json_data = replace_in_dict(json_data, 'ú', 'u')
	json_data = replace_in_dict(json_data, 'ñ', 'n')
	json_data = replace_in_dict(json_data, 'Á', 'A')
	json_data = replace_in_dict(json_data, 'É', 'E')
	json_data = replace_in_dict(json_data, 'Í', 'I')
	json_data = replace_in_dict(json_data, 'Ó', 'O')
	json_data = replace_in_dict(json_data, 'Ú', 'U')
	json_data = replace_in_dict(json_data, 'Ñ', 'N')


	return json_data