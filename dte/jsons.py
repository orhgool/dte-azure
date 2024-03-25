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

def fcf(codigo):
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}

	dte = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	emisor = get_object_or_404(Empresa, codigo=dte.emisor_id)
	receptor = get_object_or_404(Cliente, codigo=dte.receptor_id)
	datos_identificacion = {'codigoGeneracion':codigo, 'tipo':dte.tipoDte, 'version':dte.version}
	

	identificacion_data = {
			'version': dte.version,
			'ambiente': dte.ambiente.codigo,
			'tipoDte': dte.tipoDte.codigo,
			'numeroControl': dte.numeroControl,
			'codigoGeneracion': dte.codigoGeneracion,
			'tipoModelo': int(dte.tipoModelo_id),
			'tipoOperacion': int(dte.tipoTransmision_id),
			'fecEmi': dte.fecEmi.strftime("%Y-%m-%d"),
			'horEmi': dte.fecEmi.strftime("%H:%M:%S"),
			'tipoMoneda': 'USD',
			'tipoContingencia': None,
			'motivoContin': None
		}

	documentoRelacionado_data = None

	emisor_data = {'nit': emisor.nit.replace('-',''),
					'nrc': emisor.nrc.replace('-',''),
					'nombre': emisor.razonsocial,
					'codActividad': emisor.actividadEconomica_id, 
					'descActividad': emisor.actividadEconomica.descripcion,
					'nombreComercial': emisor.nombreComercial,
					'tipoEstablecimiento': emisor.tipoEstablecimiento.codigo,
					'direccion': {'departamento':emisor.departamento_id,
									'municipio':emisor.municipio.codigo,
									'complemento':emisor.direccionComplemento},
					'telefono': emisor.telefono,
					'correo': emisor.correo,
					'codEstableMH': None,
					'codEstable': None,
					'codPuntoVentaMH': None,
					'codPuntoVenta': None
					}

	receptor_data = {'tipoDocumento': receptor.tipoDocumentoCliente_id,
						'numDocumento': receptor.numeroDocumento.replace('-',''),
						'nrc': None if receptor.nrc == '' or receptor.nrc == None else receptor.nrc.replace('-',''),
						'nombre': receptor.razonsocial,
						'codActividad': receptor.actividadEconomica_id,
						'descActividad': receptor.actividadEconomica.descripcion,
						'direccion': {'departamento':receptor.departamento_id,
									'municipio':receptor.municipio.codigo,
									'complemento':receptor.direccionComplemento},
						'telefono': receptor.telefono,
						'correo': receptor.correo
					}

	otrosDocumentos_data = None
	ventaTercero_data = None

	for index, detalle in enumerate(detalleDTECliente):
		datos_detalle.append({
			'numItem': index + 1,
			'tipoItem': int(detalle.tipoItem.codigo),
			'numeroDocumento': None,
			'cantidad': round(float(detalle.cantidad), 3),
			'codigo': None,
			'codTributo': None,
			'uniMedida': int(detalle.uniMedida.codigo),
			'descripcion': detalle.descripcion,
			'precioUni': round((float(detalle.precioUni) * float(1.13)),2),
			'montoDescu': float(detalle.montoDescu),
			'ventaNoSuj': float(detalle.ventaNoSuj),
			'ventaExenta': float(detalle.ventaExenta),
			'ventaGravada': round((float(detalle.ventaGravada) * float(1.13)),2),
			'noGravado': float(detalle.noGravado),
			'tributos': None, #[str(ctributo.codigo.codigo) for ctributo in DTEDetalleTributo.objects.filter(codigoDetalle=detalle.codigoDetalle)],
			'psv': 0.0,
			'ivaItem': round((float(detalle.ventaGravada) * float(0.13)), 2)
		})

	cuerpoDocumento_data = datos_detalle

	resumen_data = {
		'totalNoSuj': 0.0,
		'totalExenta': 0.0,
		'totalGravada': float(dte.subTotal) + float(dte.ivaPerci1),
		'subTotalVentas': float(dte.subTotal) + float(dte.ivaPerci1),
		'descuNoSuj': float(dte.descuNoSuj),
		'descuExenta': float(dte.descuExenta),
		'descuGravada': float(dte.descuGravada),
		'porcentajeDescuento': float(dte.porcentajeDescuento),
		'totalDescu': float(dte.totalDescu),
		'tributos': None, #tributos_consolidados_lista,
		'subTotal': float(dte.montoTotalOperacion),
		'ivaRete1': 0.0,
		'reteRenta': 0.0,
	    'montoTotalOperacion': float(dte.montoTotalOperacion),
	    'totalNoGravado': 0.0,
	    'totalPagar': float(dte.totalPagar),
	    'totalLetras': CantLetras(float(dte.totalPagar)),
	    'totalIva': float(dte.ivaPerci1),
	    'saldoFavor': 0.0,
	    'condicionOperacion': 1,
	    'pagos': None,
	    'numPagoElectronico': None
	}

	extension_data = {
		'nombEntrega': emisor.razonsocial,
		'docuEntrega': emisor.nit.replace('-',''),
		'nombRecibe': receptor.razonsocial,
		'docuRecibe': receptor.numeroDocumento.replace('-',''),
		'placaVehiculo': None,
		'observaciones': None
	}

	apendice_data = None

	json_data = {
			'identificacion': identificacion_data,
			'documentoRelacionado' : documentoRelacionado_data,
			'emisor': emisor_data,
			'receptor': receptor_data,
			'otrosDocumentos': otrosDocumentos_data,
			'ventaTercero': ventaTercero_data,
			'cuerpoDocumento': cuerpoDocumento_data,
			'resumen': resumen_data,
			'extension': extension_data,
			'apendice': apendice_data,
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


def ccf(codigo):
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}

	dte = get_object_or_404(DTECliente, codigoGeneracion=codigo)
	emisor = get_object_or_404(Empresa, codigo=dte.emisor_id)
	receptor = get_object_or_404(Cliente, codigo=dte.receptor_id)
	datos_identificacion = {'codigoGeneracion':codigo, 'tipo':dte.tipoDte, 'version':dte.version}
	

	identificacion_data = {
			'version': dte.version,
			'ambiente': dte.ambiente.codigo,
			'tipoDte': dte.tipoDte.codigo,
			'numeroControl': dte.numeroControl,
			'codigoGeneracion': dte.codigoGeneracion,
			'tipoModelo': int(dte.tipoModelo_id),
			'tipoOperacion': int(dte.tipoTransmision_id),
			'fecEmi': dte.fecEmi.strftime("%Y-%m-%d"),
			'horEmi': dte.fecEmi.strftime("%H:%M:%S"),
			'tipoMoneda': 'USD',
			'tipoContingencia': None,
			'motivoContin': None
		}

	documentoRelacionado_data = None

	emisor_data = {'nit': emisor.nit.replace('-',''),
					'nrc': emisor.nrc.replace('-',''),
					'nombre': emisor.razonsocial,
					'codActividad': emisor.actividadEconomica_id, 
					'descActividad': emisor.actividadEconomica.descripcion,
					'nombreComercial': emisor.nombreComercial,
					'tipoEstablecimiento': emisor.tipoEstablecimiento.codigo,
					'direccion': {'departamento':emisor.departamento_id,
									'municipio':emisor.municipio.codigo,
									'complemento':emisor.direccionComplemento},
					'telefono': emisor.telefono,
					'correo': emisor.correo,
					'codEstableMH': None,
					'codEstable': None,
					'codPuntoVentaMH': None,
					'codPuntoVenta': None
					}

	receptor_data = {'nit': receptor.numeroDocumento.replace('-',''),
						'nrc': None if receptor.nrc == '' or receptor.nrc == None else receptor.nrc.replace('-',''),
						'nombre': receptor.razonsocial,
						'codActividad': receptor.actividadEconomica_id,
						'descActividad': receptor.actividadEconomica.descripcion,
						'nombreComercial': receptor.nombreComercial,
						'direccion': {'departamento':receptor.departamento_id,
									'municipio':receptor.municipio.codigo,
									'complemento':receptor.direccionComplemento},
						'telefono': receptor.telefono,
						'correo': receptor.correo
					}

	otrosDocumentos_data = None
	ventaTercero_data = None

	for detalle in detalleDTECliente:
		totales_IVA = round(float(0), 2)
		current = round(float(0), 2)
		
		restributos = DTEClienteDetalleTributo.objects.filter(codigoDetalle=detalle.codigoDetalle)
		tributos_detalle = []
		for tributo in restributos:
			if tributo.codigo.codigo in tributos_consolidados:
				totales_IVA += float(tributo.valor)
				current = tributos_consolidados[tributo.codigo.codigo]["valor"] 
				current += round(float(tributo.valor), 2)
				tributos_consolidados[tributo.codigo.codigo]["valor"] = round(float(current), 2)
			else:
				totales_IVA = float(tributo.valor)
				tributos_consolidados[tributo.codigo.codigo] = {
					"codigo": tributo.codigo.codigo,
					"descripcion": tributo.descripcion,
					"valor": round(totales_IVA, 2)
				}
		tributos_consolidados_lista = list(tributos_consolidados.values())

	for index, detalle in enumerate(detalleDTECliente):
		datos_detalle.append({
			'numItem': index + 1,
			'tipoItem': int(detalle.tipoItem.codigo),
			'numeroDocumento': None,
			'cantidad': round(float(detalle.cantidad), 3),
			'codigo': None,
			'codTributo': None,
			'uniMedida': int(detalle.uniMedida.codigo),
			'descripcion': detalle.descripcion,
			'precioUni': float(detalle.precioUni),
			'montoDescu': float(detalle.montoDescu),
			'ventaNoSuj': float(detalle.ventaNoSuj),
			'ventaExenta': float(detalle.ventaExenta),
			'ventaGravada': float(detalle.ventaGravada),
			'noGravado': float(detalle.noGravado),
			'tributos': [str(ctributo.codigo.codigo) for ctributo in DTEClienteDetalleTributo.objects.filter(codigoDetalle=detalle.codigoDetalle)],
			'psv': 0.0,
			'noGravado': round((float(detalle.noGravado) * float(0.13)), 2)
		})

	cuerpoDocumento_data = datos_detalle

	resumen_data = {
		'totalNoSuj': 0.0,
		'totalExenta': 0.0,
		'totalGravada': float(dte.subTotal),
		'subTotalVentas': float(dte.subTotalVentas),
		'descuNoSuj': float(dte.descuNoSuj),
		'descuExenta': float(dte.descuExenta),
		'descuGravada': float(dte.descuGravada),
		'porcentajeDescuento': float(dte.porcentajeDescuento),
		'totalDescu': float(dte.totalDescu),
		'tributos': tributos_consolidados_lista,
		'subTotal': float(dte.subTotal),
		'ivaPerci1': float(dte.ivaPerci1),
		'ivaRete1': 0.0,
		'reteRenta': 0.0,
	    'montoTotalOperacion': float(dte.montoTotalOperacion),
	    'totalNoGravado': 0.0,
	    'totalPagar': float(dte.totalPagar),
	    'totalLetras': CantLetras(float(dte.totalPagar)),
	    'saldoFavor': 0.0,
	    'condicionOperacion': 1,
	    'pagos': None,
	    'numPagoElectronico': None
	}

	extension_data = {
		'nombEntrega': emisor.razonsocial,
		'docuEntrega': emisor.nit.replace('-',''),
		'nombRecibe': receptor.razonsocial,
		'docuRecibe': receptor.numeroDocumento.replace('-',''),
		'placaVehiculo': None,
		'observaciones': None
	}

	apendice_data = None

	json_data = {
			'identificacion': identificacion_data,
			'documentoRelacionado' : documentoRelacionado_data,
			'emisor': emisor_data,
			'receptor': receptor_data,
			'otrosDocumentos': otrosDocumentos_data,
			'ventaTercero': ventaTercero_data,
			'cuerpoDocumento': cuerpoDocumento_data,
			'resumen': resumen_data,
			'extension': extension_data,
			'apendice': apendice_data,
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