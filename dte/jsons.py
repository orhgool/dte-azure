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

def fcf(codigo): # 01 - Factura
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

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
			'precioUni': float(detalle.precioUni),
			'montoDescu': float(detalle.montoDescu),
			'ventaNoSuj': float(detalle.ventaNoSuj),
			'ventaExenta': float(detalle.ventaExenta),
			'ventaGravada': float(detalle.ventaGravada),
			'noGravado': float(detalle.noGravado),
			'tributos': None, #[str(ctributo.codigo.codigo) for ctributo in DTEDetalleTributo.objects.filter(codigoDetalle=detalle.codigoDetalle)],
			'psv': 0.0,
			'ivaItem': round((float(detalle.ventaGravada) - (float(detalle.ventaGravada) / float(1.13))), 2)
		})

	cuerpoDocumento_data = datos_detalle

	resumen_data = {
		'totalNoSuj': float(dte.totalNoSuj),
		'totalExenta': float(dte.totalExenta),
		'totalGravada': float(dte.totalGravada),
		'subTotalVentas': float(dte.subTotalVentas),
		'descuNoSuj': float(dte.descuNoSuj),
		'descuExenta': float(dte.descuExenta),
		'descuGravada': float(dte.descuGravada),
		'porcentajeDescuento': float(dte.porcentajeDescuento),
		'totalDescu': float(dte.totalDescu),
		'tributos': None, #tributos_consolidados_lista,
		'subTotal': float(dte.montoTotalOperacion),
		'ivaRete1': float(dte.ivaRete1),
		'reteRenta': float(dte.reteRenta),
	    'montoTotalOperacion': float(dte.montoTotalOperacion),
	    'totalNoGravado': float(dte.totalNoGravado),
	    'totalPagar': float(dte.totalPagar),
	    'totalLetras': CantLetras(float(dte.totalPagar)),
	    'totalIva': round((float(dte.totalGravada) - (float(dte.totalGravada) / float(1.13))),2),
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


def ccf(codigo): # 03 - Crédito fiscal
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

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
		'totalNoSuj': float(dte.totalNoSuj),
		'totalExenta': float(dte.totalExenta),
		'totalGravada': float(dte.totalGravada),
		'subTotalVentas': float(dte.subTotalVentas),
		'descuNoSuj': float(dte.descuNoSuj),
		'descuExenta': float(dte.descuExenta),
		'descuGravada': float(dte.descuGravada),
		'porcentajeDescuento': float(dte.porcentajeDescuento),
		'totalDescu': float(dte.totalDescu),
		'tributos': tributos_consolidados_lista if tributos_consolidados_lista else None,
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


def nc(codigo): # 05 - Nota de crédito
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	docrelacionado_detalle = []
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

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
			'tipoContingencia': None,
			'motivoContin': None,
			'fecEmi': dte.fecEmi.strftime("%Y-%m-%d"),
			'horEmi': dte.fecEmi.strftime("%H:%M:%S"),
			'tipoMoneda': 'USD'
		}

	
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
					'correo': emisor.correo
					}

	receptor_data = {'nit': receptor.numeroDocumento.replace('-',''),
						'nrc': None if receptor.nrc == '' or receptor.nrc == None else receptor.nrc.replace('-',''),
						'nombre': receptor.razonsocial,
						'nombreComercial': None,
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
		docrelacionado_detalle.append({
			'tipoDocumento': detalle.tipoDoc.codigo,
			'tipoGeneracion': int(detalle.tipoGeneracion.codigo),
			'numeroDocumento': detalle.numeroDocumento,
			'fechaEmision': detalle.fechaEmision.strftime("%Y-%m-%d")
			})
		datos_detalle.append({
			'numItem': index + 1,
			'tipoItem': int(detalle.tipoItem.codigo),
			'numeroDocumento': detalle.numeroDocumento,
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
			'tributos': [str(ctributo.codigo.codigo) for ctributo in DTEClienteDetalleTributo.objects.filter(codigoDetalle=detalle.codigoDetalle)],
		})

	documentoRelacionado_data = docrelacionado_detalle
	cuerpoDocumento_data = datos_detalle

	resumen_data = {
		'totalNoSuj': float(dte.totalNoSuj),
		'totalExenta': float(dte.totalExenta),
		'totalGravada': float(dte.totalGravada),
		'subTotalVentas': float(dte.subTotalVentas),
		'descuNoSuj': float(dte.descuNoSuj),
		'descuExenta': float(dte.descuExenta),
		'descuGravada': float(dte.descuGravada),
		'totalDescu': float(dte.totalDescu),
		'tributos': tributos_consolidados_lista,
		'subTotal': float(dte.subTotal),
		'ivaPerci1': float(dte.ivaPerci1),
		'ivaRete1': float(dte.ivaRete1),
		'reteRenta': float(dte.reteRenta),
	    'montoTotalOperacion': float(dte.montoTotalOperacion),
	    'totalLetras': CantLetras(float(dte.totalPagar)),
	    'condicionOperacion': 1
	}

	extension_data = {
		'nombEntrega': emisor.razonsocial,
		'docuEntrega': emisor.nit.replace('-',''),
		'nombRecibe': receptor.razonsocial,
		'docuRecibe': receptor.numeroDocumento.replace('-',''),
		'observaciones': None
	}

	apendice_data = None

	json_data = {
			'identificacion': identificacion_data,
			'documentoRelacionado' : documentoRelacionado_data,
			'ventaTercero': ventaTercero_data,
			'emisor': emisor_data,
			'receptor': receptor_data,
			#'otrosDocumentos': otrosDocumentos_data,
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


def nd(codigo): # 06 - Nota de débito
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	docrelacionado_detalle = []
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

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
			'tipoContingencia': None,
			'motivoContin': None,
			'fecEmi': dte.fecEmi.strftime("%Y-%m-%d"),
			'horEmi': dte.fecEmi.strftime("%H:%M:%S"),
			'tipoMoneda': 'USD'
		}

	
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
					'correo': emisor.correo
					}

	receptor_data = {'nit': receptor.numeroDocumento.replace('-',''),
						'nrc': None if receptor.nrc == '' or receptor.nrc == None else receptor.nrc.replace('-',''),
						'nombre': receptor.razonsocial,
						'nombreComercial': None,
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
		docrelacionado_detalle.append({
			'tipoDocumento': detalle.tipoDoc.codigo,
			'tipoGeneracion': int(detalle.tipoGeneracion.codigo),
			'numeroDocumento': detalle.numeroDocumento,
			'fechaEmision': detalle.fechaEmision.strftime("%Y-%m-%d")
			})
		datos_detalle.append({
			'numItem': index + 1,
			'tipoItem': int(detalle.tipoItem.codigo),
			'numeroDocumento': detalle.numeroDocumento,
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
			'tributos': [str(ctributo.codigo.codigo) for ctributo in DTEClienteDetalleTributo.objects.filter(codigoDetalle=detalle.codigoDetalle)],
		})

	documentoRelacionado_data = docrelacionado_detalle
	cuerpoDocumento_data = datos_detalle

	resumen_data = {
		'totalNoSuj': float(dte.totalNoSuj),
		'totalExenta': float(dte.totalExenta),
		'totalGravada': float(dte.totalGravada),
		'subTotalVentas': float(dte.subTotalVentas),
		'descuNoSuj': float(dte.descuNoSuj),
		'descuExenta': float(dte.descuExenta),
		'descuGravada': float(dte.descuGravada),
		'totalDescu': float(dte.totalDescu),
		'tributos': tributos_consolidados_lista,
		'subTotal': float(dte.subTotal),
		'ivaPerci1': float(dte.ivaPerci1),
		'ivaRete1': float(dte.ivaRete1),
		'reteRenta': float(dte.reteRenta),
	    'montoTotalOperacion': float(dte.montoTotalOperacion),
	    'totalLetras': CantLetras(float(dte.totalPagar)),
	    'condicionOperacion': 1,
	    'numPagoElectronico': None
	}

	extension_data = {
		'nombEntrega': emisor.razonsocial,
		'docuEntrega': emisor.nit.replace('-',''),
		'nombRecibe': receptor.razonsocial,
		'docuRecibe': receptor.numeroDocumento.replace('-',''),
		'observaciones': None
	}

	apendice_data = None

	json_data = {
			'identificacion': identificacion_data,
			'documentoRelacionado' : documentoRelacionado_data,
			'ventaTercero': ventaTercero_data,
			'emisor': emisor_data,
			'receptor': receptor_data,
			#'otrosDocumentos': otrosDocumentos_data,
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


def fex(codigo): # 11 - Factura de exportación
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

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
			'motivoContigencia': None
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
					'codPuntoVenta': None,
					'tipoItemExpor': int(dte.tipoItemExpor_id),
					'recintoFiscal': dte.recintoFiscal_id,
					'regimen': dte.regimen_id
					}

	receptor_data = {'tipoDocumento': receptor.tipoDocumentoCliente_id,
						'numDocumento': receptor.numeroDocumento.replace('-',''),
						'nombre': receptor.razonsocial,
						#'codActividad': receptor.actividadEconomica_id,
						'nombreComercial': None,
						'descActividad': receptor.actividadEconomica.descripcion,
						'complemento':receptor.direccionComplemento,
						'codPais': receptor.pais_id,
						'nombrePais': str(receptor.pais),
						'tipoPersona': int(receptor.tipoPersona_id),
						'telefono': receptor.telefono,
						'correo': receptor.correo
					}

	otrosDocumentos_data = None
	ventaTercero_data = None

	for index, detalle in enumerate(detalleDTECliente):
		datos_detalle.append({
			'numItem': index + 1,
			'cantidad': round(float(detalle.cantidad), 3),
			'codigo': None,
			'uniMedida': int(detalle.uniMedida.codigo),
			'descripcion': detalle.descripcion,
			'precioUni': float(detalle.precioUni),
			'montoDescu': float(detalle.montoDescu),
			'ventaGravada': float(detalle.ventaGravada),
			'tributos': [str(ctributo.codigo.codigo) for ctributo in DTEClienteDetalleTributo.objects.filter(codigoDetalle=detalle.codigoDetalle)],
			'noGravado': float(detalle.noGravado),
		})

	cuerpoDocumento_data = datos_detalle

	resumen_data = {
		'totalGravada': float(dte.totalGravada),
		'descuento': float(dte.descuGravada),
		'porcentajeDescuento': float(dte.porcentajeDescuento),
		'totalDescu': float(dte.totalDescu),
		'seguro': 0, #tributos_consolidados_lista,
		'flete': 0,
		'montoTotalOperacion': float(dte.montoTotalOperacion),
	    'totalNoGravado': 0.0,
	    'totalPagar': float(dte.totalPagar),
	    'totalLetras': CantLetras(float(dte.totalPagar)),
	    'condicionOperacion': 1,
	    'pagos': None,
	    'numPagoElectronico': None,
	    'codIncoterms': dte.incoterms_id,
	    'descIncoterms': str(dte.incoterms),
	    'observaciones': dte.observaciones
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
			#'documentoRelacionado' : documentoRelacionado_data,
			'emisor': emisor_data,
			'receptor': receptor_data,
			'otrosDocumentos': otrosDocumentos_data,
			'ventaTercero': ventaTercero_data,
			'cuerpoDocumento': cuerpoDocumento_data,
			'resumen': resumen_data,
			#'extension': extension_data,
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


def fse(codigo): # 14 - Factura de sujeto excluido
	detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

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
			'tipoContingencia': None,
			'motivoContin': None,
			'fecEmi': dte.fecEmi.strftime("%Y-%m-%d"),
			'horEmi': dte.fecEmi.strftime("%H:%M:%S"),
			'tipoMoneda': 'USD'
		}

	documentoRelacionado_data = None

	emisor_data = {'nit': emisor.nit.replace('-',''),
					'nrc': emisor.nrc.replace('-',''),
					'nombre': emisor.razonsocial,
					'codActividad': emisor.actividadEconomica_id, 
					'descActividad': emisor.actividadEconomica.descripcion,
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
			'cantidad': round(float(detalle.cantidad), 3),
			'codigo': None,
			'uniMedida': int(detalle.uniMedida.codigo),
			'descripcion': detalle.descripcion,
			'precioUni': float(detalle.precioUni),
			'montoDescu': float(detalle.montoDescu),
			'compra': float(detalle.compra)
		})

	cuerpoDocumento_data = datos_detalle

	resumen_data = {
		'totalCompra': float(dte.totalCompra),
		'descu': float(dte.totalDescu),
		'totalDescu': float(dte.totalDescu),
		'subTotal': float(dte.subTotal),
		'ivaRete1': float(dte.ivaRete1),
		'reteRenta': float(dte.reteRenta),
	    'totalPagar': float(dte.totalPagar),
	    'totalLetras': CantLetras(float(dte.totalPagar)),
	    'condicionOperacion': 1,
	    'pagos': None,
	    'observaciones': None
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
			#'documentoRelacionado' : documentoRelacionado_data,
			'emisor': emisor_data,
			'sujetoExcluido': receptor_data,
			#'otrosDocumentos': otrosDocumentos_data,
			#'ventaTercero': ventaTercero_data,
			'cuerpoDocumento': cuerpoDocumento_data,
			'resumen': resumen_data,
			#'extension': extension_data,
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


def anulacion(codAnulacion, codigoDte): # Anulacion
	#detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	#from .funciones import CodGeneracion
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	dte = get_object_or_404(DTECliente, codigoGeneracion=codigoDte)
	emisor = get_object_or_404(Empresa, codigo=dte.emisor_id)
	receptor = get_object_or_404(Cliente, codigo=dte.receptor_id)
	#datos_identificacion = {'codigoGeneracion':codigo, 'tipo':dte.tipoDte, 'version':dte.version}
	

	identificacion_data = {
			'version': 2,
			'ambiente': dte.ambiente.codigo,
			'codigoGeneracion': codAnulacion,
			'fecAnula': datetime.now().strftime("%Y-%m-%d"),
			'horAnula': datetime.now().strftime("%H:%M:%S")
		}

	documentoRelacionado_data = None

	emisor_data = {
		'nit': emisor.nit.replace('-',''),
		'nombre': emisor.razonsocial,
		'nomEstablecimiento': emisor.nombreComercial,
		'tipoEstablecimiento': emisor.tipoEstablecimiento.codigo,
		'telefono': emisor.telefono,
		'correo': emisor.correo,
		'codEstable': None,
		'codPuntoVenta': None,
		'codEstableMH': None,
		'codPuntoVentaMH': None
	}

	documento_data = {
		'tipoDte': dte.tipoDte_id,
	    'codigoGeneracion': dte.codigoGeneracion,
	    'selloRecibido': dte.selloRecepcion,
	    'numeroControl': dte.numeroControl,
	    'fecEmi': dte.fecEmi.strftime("%Y-%m-%d"),
	    'montoIva': float(dte.montoTotalOperacion),
	    'codigoGeneracionR': None,
	    'tipoDocumento': '36',
	    'numDocumento': dte.receptor.numeroDocumento.replace('-',''),
	    'nombre': dte.receptor.razonsocial,
	    'telefono': dte.receptor.telefono,
	    'correo': dte.receptor.correo,
	}

	motivo_data = {
	    'tipoAnulacion': 2,
	    'motivoAnulacion': 'Rescindir de la operacion realizada',
	    'nombreResponsable': dte.emisor.razonsocial,
	    'tipDocResponsable': '36',
	    'numDocResponsable': dte.emisor.nit.replace('-','') if dte.emisor.nit.replace('-','') else dte.emisor.dui.replace('-',''),
	    'nombreSolicita': dte.receptor.razonsocial,
	    'tipDocSolicita': '36',
	    'numDocSolicita': dte.receptor.numeroDocumento.replace('-','')
  	}


	json_data = {
		'identificacion': identificacion_data,
		'emisor': emisor_data,
		'documento': documento_data,
		'motivo': motivo_data
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


def contingencia(codContingencia, codigoDte): # Contingencia
	#detalleDTECliente = DTEClienteDetalle.objects.filter(dte=codigo)
	#from .funciones import CodGeneracion
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	dte = get_object_or_404(DTEContingencia, codigoGeneracion=codigoDte)
	emisor = get_object_or_404(Empresa, codigo=dte.emisor_id)
	
	identificacion_data = {
			'version': 3,
			'ambiente': dte.ambiente.codigo,
			'codigoGeneracion': codContingencia,
			'fTransmision': datetime.now().strftime("%Y-%m-%d"),
			'hTransmision': datetime.now().strftime("%H:%M:%S")
		}

	emisor_data = {
		'nit': emisor.nit.replace('-',''),
		'nombre': emisor.razonsocial,
		'nombreResponsable': emisor.nombreComercial,
		'tipoDocResponsable': '36',
		'numeroDocResponsalble'
		'tipoEstablecimiento': emisor.tipoEstablecimiento.codigo,
		'telefono': emisor.telefono,
		'correo': emisor.correo,
		'codPuntoVenta': None,
		'codEstableMH': None
	}

	for index, detalle in enumerate(detalleDTECliente):
		datos_detalle.append({
			'noItem': index + 1,
			'tipoDoc': int(detalle.tipoDte.codigo),
			'codigoGeneracion': detalle.codigoGeneracionDTE
		})

	detalleDTE_data = datos_detalle

	motivo_data = {
	    'fInicio': dte.fInicio.strftime("%Y-%m-%d"),
	    'fFin': dte.fFinal.strftime("%Y-%m-%d"),
	    'hInicio': dte.fInicio.strftime("%H:%M:%S"),
	    'hFin': dte.fFinal.strftime("%H:%M:%S"),
	    'tipoContingencia': dte.tipoContingencia.codigo,
	    'motivoContingencia': dte.tipoContingencia
  	}


	json_data = {
		'identificacion': identificacion_data,
		'emisor': emisor_data,
		'detalleDTE': detalleDTE_data,
		'motivo': motivo_data
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