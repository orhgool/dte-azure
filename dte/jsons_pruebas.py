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

def fcf_p(empresa, codigo): # 01 - Factura
	emisor = get_object_or_404(Empresa, codigo=empresa)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	identificacion_data = {
			'version': 1,
			'ambiente': '00',
			'tipoDte': '01',
			'numeroControl': Correlativo(cod_tipo='01', cod_empresa=empresa),
			'codigoGeneracion': codigo,
			'tipoModelo': 1,
			'tipoOperacion': 1,
			'fecEmi': datetime.now().strftime("%Y-%m-%d"),
			'horEmi': datetime.now().strftime("%H:%M:%S"),
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

	receptor_data = {'tipoDocumento': '36',
				    'numDocumento': '03010205021015',
				    'nrc': None,
				    'nombre': 'Cliente 002 DECO',
				    'codActividad': '10005',
				    'descActividad': 'Otros',
				    'direccion': {
				      'departamento': '01',
				      'municipio': '03',
				      'complemento': 'Ferreteria La Industrial'
				    },
				    'telefono': '00000000',
				    'correo': 'cliente@cliente.com'
					}

	otrosDocumentos_data = None
	ventaTercero_data = None


	cuerpoDocumento_data = {
			'numItem': 1,
	      'tipoItem': 2,
	      'numeroDocumento': None,
	      'cantidad': 2,
	      'codigo': None,
	      'codTributo': None,
	      'uniMedida': 59,
	      'descripcion': 'Ventas varias para pruebaas',
	      'precioUni': 128.82,
	      'montoDescu': 0.0,
	      'ventaNoSuj': 0.0,
	      'ventaExenta': 0.0,
	      'ventaGravada': 257.64,
	      'noGravado': 0.0,
	      'tributos': None,
	      'psv': 0.0,
	      'ivaItem': 29.64
		},

	resumen_data = {
		'totalNoSuj': 0.0,
	    'totalExenta': 0.0,
	    'totalGravada': 257.64,
	    'subTotalVentas': 257.64,
	    'descuNoSuj': 0.0,
	    'descuExenta': 0.0,
	    'descuGravada': 0.0,
	    'porcentajeDescuento': 0.0,
	    'totalDescu': 0.0,
	    'tributos': None,
	    'subTotal': 257.64,
	    'ivaRete1': 0.0,
	    'reteRenta': 0.0,
	    'montoTotalOperacion': 257.64,
	    'totalNoGravado': 0.0,
	    'totalPagar': 257.64,
	    'totalLetras': 'DOSCIENTOS CINCUENTA Y SIETE 64/100 USD',
	    'totalIva': 29.64,
	    'saldoFavor': 0.0,
	    'condicionOperacion': 1,
	    'pagos': None,
	    'numPagoElectronico': None
	}

	extension_data = {
		'nombEntrega': 'ALFA CONSULTORES, S.A. DE C.V.',
	    'docuEntrega': '03070711201016',
	    'nombRecibe': 'Cliente 002 DECO',
	    'docuRecibe': '03010205021015',
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


def ccf_p(empresa, codigo): # 03 - CCF
	emisor = get_object_or_404(Empresa, codigo=empresa)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	identificacion_data = {
			'version': 3,
			'ambiente': '00',
			'tipoDte': '03',
			'numeroControl': Correlativo(cod_tipo='03', cod_empresa=empresa),
			'codigoGeneracion': codigo,
			'tipoModelo': 1,
			'tipoOperacion': 1,
			'fecEmi': datetime.now().strftime("%Y-%m-%d"),
			'horEmi': datetime.now().strftime("%H:%M:%S"),
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

	receptor_data = {"nit": "06142407620011",
				    "nrc": "4340",
				    "nombre": "ALMACENADORA CENTROAMERICANA, S.A. DE C.V.",
				    "codActividad": "52102",
				    "descActividad": "Alquiler de silos para conservacion y almacenamiento de granos",
				    "nombreComercial": "ALCASA",
				    "direccion": {
				      "departamento": "05",
				      "municipio": "11",
				      "complemento": "KM 9 y medio complejo corporativo SISCO"
				    },
				    "telefono": "22121270",
				    "correo": "alcasa@alcasa.com.sv"
					}

	otrosDocumentos_data = None
	ventaTercero_data = None


	cuerpoDocumento_data = {
		"numItem": 1,
      "tipoItem": 2,
      "numeroDocumento": None,
      "cantidad": 1.0,
      "codigo": None,
      "codTributo": None,
      "uniMedida": 59,
      "descripcion": "Pago 50% aplicacion control PLDA",
      "precioUni": 750.0,
      "montoDescu": 0.0,
      "ventaNoSuj": 0.0,
      "ventaExenta": 0.0,
      "ventaGravada": 750.0,
      "noGravado": 0.0,
      "tributos": [
        "20"
      ],
      "psv": 0.0
		},

	resumen_data = {
		"totalNoSuj": 0.0,
	    "totalExenta": 0.0,
	    "totalGravada": 750.0,
	    "subTotalVentas": 750.0,
	    "descuNoSuj": 0.0,
	    "descuExenta": 0.0,
	    "descuGravada": 0.0,
	    "porcentajeDescuento": 0.0,
	    "totalDescu": 0.0,
	    "tributos": [
	      {
	        "codigo": "20",
	        "descripcion": "Impuesto al Valor Agregado 13%",
	        "valor": 97.5
	      }
	    ],
	    "subTotal": 750.0,
	    "ivaPerci1": 0.0,
	    "ivaRete1": 0.0,
	    "reteRenta": 0.0,
	    "montoTotalOperacion": 847.5,
	    "totalNoGravado": 0.0,
	    "totalPagar": 847.5,
	    "totalLetras": "OCHOCIENTOS CUARENTA Y SIETE 50/100 USD",
	    "saldoFavor": 0.0,
	    "condicionOperacion": 1,
	    "pagos": None,
	    "numPagoElectronico": None
	}

	extension_data = {
		'nombEntrega': None,
	    'docuEntrega': None,
	    'nombRecibe': None,
	    'docuRecibe': None,
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


def nc_p(empresa, codigo): # 05 - NOTA DE CREDITO
	emisor = get_object_or_404(Empresa, codigo=empresa)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	identificacion_data = {
			'version': 3,
			'ambiente': '00',
			'tipoDte': '05',
			'numeroControl': Correlativo(cod_tipo='05', cod_empresa=empresa),
			'codigoGeneracion': codigo,
			'tipoModelo': 1,
			'tipoOperacion': 1,
			'fecEmi': datetime.now().strftime("%Y-%m-%d"),
			'horEmi': datetime.now().strftime("%H:%M:%S"),
			'tipoMoneda': 'USD',
			'tipoContingencia': None,
			'motivoContin': None
		}

	documentoRelacionado_data = {
      "tipoDocumento": "03",
      "tipoGeneracion": 1,
      "numeroDocumento": "9239",
      "fechaEmision": "2024-04-04"
    },

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

	receptor_data = {"nit": "06142407620011",
				    "nrc": "4340",
				    "nombre": "ALMACENADORA CENTROAMERICANA, S.A. DE C.V.",
				    "nombreComercial": "ALCASA",
				    "codActividad": "52102",
				    "descActividad": "Alquiler de silos para conservacion y almacenamiento de granos",
				    "direccion": {
				      "departamento": "05",
				      "municipio": "11",
				      "complemento": "KM 9 y medio complejo corporativo SISCO"
				    },
				    "telefono": "22121270",
				    "correo": "alcasa@alcasa.com.sv"
					}

	otrosDocumentos_data = None
	ventaTercero_data = None


	cuerpoDocumento_data = {
		"numItem": 1,
	      "tipoItem": 1,
	      "numeroDocumento": "9239",
	      "cantidad": 1.0,
	      "codigo": None,
	      "codTributo": None,
	      "uniMedida": 59,
	      "descripcion": "Correccion",
	      "precioUni": 20.0,
	      "montoDescu": 0.0,
	      "ventaNoSuj": 0.0,
	      "ventaExenta": 0.0,
	      "ventaGravada": 20.0,
	      "tributos": [
	        "20"
	      ]
			},

	resumen_data = {
		"totalNoSuj": 0.0,
	    "totalExenta": 0.0,
	    "totalGravada": 20.0,
	    "subTotalVentas": 20.0,
	    "descuNoSuj": 0.0,
	    "descuExenta": 0.0,
	    "descuGravada": 0.0,
	    "totalDescu": 0.0,
	    "tributos": [
	      {
	        "codigo": "20",
	        "descripcion": "Impuesto al Valor Agregado 13%",
	        "valor": 2.6
	      }
	    ],
	    "subTotal": 20.0,
	    "ivaPerci1": 0.0,
	    "ivaRete1": 0.0,
	    "reteRenta": 0.0,
	    "montoTotalOperacion": 22.6,
	    "totalLetras": "VEINTIDOS 60/100 USD",
	    "condicionOperacion": 1
	}

	extension_data = {
		'nombEntrega': None,
	    'docuEntrega': None,
	    'nombRecibe': None,
	    'docuRecibe': None,
	    'observaciones': None
	}

	apendice_data = None

	json_data = {
			'identificacion': identificacion_data,
			'documentoRelacionado' : documentoRelacionado_data,
			'ventaTercero': ventaTercero_data,
			'emisor': emisor_data,
			'receptor': receptor_data,
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


def nd_p(empresa, codigo): # 06 - NOTA DE DEBITO
	emisor = get_object_or_404(Empresa, codigo=empresa)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	identificacion_data = {
			'version': 3,
			'ambiente': '00',
			'tipoDte': '06',
			'numeroControl': Correlativo(cod_tipo='06', cod_empresa=empresa),
			'codigoGeneracion': codigo,
			'tipoModelo': 1,
			'tipoOperacion': 1,
			'fecEmi': datetime.now().strftime("%Y-%m-%d"),
			'horEmi': datetime.now().strftime("%H:%M:%S"),
			'tipoMoneda': 'USD',
			'tipoContingencia': None,
			'motivoContin': None
		}

	documentoRelacionado_data = {
      "tipoDocumento": "03",
      "tipoGeneracion": 1,
      "numeroDocumento": "5623",
      "fechaEmision": "2024-04-01"
    },

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

	receptor_data = {"nit": "06142407620011",
				    "nrc": "4340",
				    "nombre": "ALMACENADORA CENTROAMERICANA, S.A. DE C.V.",
				    "nombreComercial": "ALCASA",
				    "codActividad": "52102",
				    "descActividad": "Alquiler de silos para conservacion y almacenamiento de granos",
				    "direccion": {
				      "departamento": "05",
				      "municipio": "11",
				      "complemento": "KM 9 y medio complejo corporativo SISCO"
				    },
				    "telefono": "22121270",
				    "correo": "alcasa@alcasa.com.sv"
					}

	otrosDocumentos_data = None
	ventaTercero_data = None


	cuerpoDocumento_data = {
	      "numItem": 1,
	      "tipoItem": 1,
	      "numeroDocumento": "5623",
	      "cantidad": 1.0,
	      "codigo": None,
	      "codTributo": None,
	      "uniMedida": 59,
	      "descripcion": 'Debito',
	      "precioUni": 20.0,
	      "montoDescu": 0.0,
	      "ventaNoSuj": 0.0,
	      "ventaExenta": 0.0,
	      "ventaGravada": 20.0,
	      "tributos": [
	        "20"
	      ]
	    },

	resumen_data = {
		"totalNoSuj": 0.0,
    "totalExenta": 0.0,
    "totalGravada": 20.0,
    "subTotalVentas": 20.0,
    "descuNoSuj": 0.0,
    "descuExenta": 0.0,
    "descuGravada": 0.0,
    "totalDescu": 0.0,
    "tributos": [
      {
        "codigo": "20",
        "descripcion": "Impuesto al Valor Agregado 13%",
        "valor": 2.6
      }
    ],
    "subTotal": 20.0,
    "ivaPerci1": 0.0,
    "ivaRete1": 0.0,
    "reteRenta": 0.0,
    "montoTotalOperacion": 22.6,
    "totalLetras": "VEINTIDOS 60/100 USD",
    "condicionOperacion": 1,
    "numPagoElectronico": None
	}

	extension_data = {
		'nombEntrega': None,
	    'docuEntrega': None,
	    'nombRecibe': None,
	    'docuRecibe': None,
	    'observaciones': None
	}

	apendice_data = None

	json_data = {
			'identificacion': identificacion_data,
			'documentoRelacionado': documentoRelacionado_data,
			'ventaTercero': ventaTercero_data,
			'emisor': emisor_data,
			'receptor': receptor_data,
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


def fex_p(empresa, codigo): # 11 - FACTURA DE EXPORTACION
	emisor = get_object_or_404(Empresa, codigo=empresa)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	identificacion_data = {
			'version': 1,
			'ambiente': '00',
			'tipoDte': '11',
			'numeroControl': Correlativo(cod_tipo='11', cod_empresa=empresa),
			'codigoGeneracion': codigo,
			'tipoModelo': 1,
			'tipoOperacion': 1,
			'fecEmi': datetime.now().strftime("%Y-%m-%d"),
			'horEmi': datetime.now().strftime("%H:%M:%S"),
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
					"codEstableMH": None,
				    "codEstable": None,
				    "codPuntoVentaMH": None,
				    "codPuntoVenta": None,
				    "tipoItemExpor": 1,
				    "recintoFiscal": "02",
				    "regimen": "EX-1.1040.000"
					}

	receptor_data = {"tipoDocumento": "36",
				    "numDocumento": "06142407620011",
				    "nombre": "ALMACENADORA CENTROAMERICANA, S.A. DE C.V.",
				    "nombreComercial": None,
				    "descActividad": "Alquiler de silos para conservacion y almacenamiento de granos",
				    "complemento": "KM 9 y medio complejo corporativo SISCO",
				    "codPais": "9300",
				    "nombrePais": "EL SALVADOR",
				    "tipoPersona": 2,
				    "telefono": "22121270",
				    "correo": "alcasa@alcasa.com.sv"
					}

	otrosDocumentos_data = None
	ventaTercero_data = None


	cuerpoDocumento_data = {
	      "numItem": 1,
	      "cantidad": 1.0,
	      "codigo": None,
	      "uniMedida": 59,
	      "descripcion": "producto",
	      "precioUni": 300.0,
	      "montoDescu": 0.0,
	      "ventaGravada": 300.0,
	      "tributos": [
	        "20"
	      ],
	      "noGravado": 0.0
	    },

	resumen_data = {
		"totalGravada": 300.0,
	    "descuento": 0.0,
	    "porcentajeDescuento": 0.0,
	    "totalDescu": 0.0,
	    "seguro": 0,
	    "flete": 0,
	    "montoTotalOperacion": 300.0,
	    "totalNoGravado": 0.0,
	    "totalPagar": 300.0,
	    "totalLetras": "TRESCIENTOS 00/100 USD",
	    "condicionOperacion": 1,
	    "pagos": None,
	    "numPagoElectronico": None,
	    "codIncoterms": "04",
	    "descIncoterms": "CIP-Transporte y seguro pagado hasta",
	    "observaciones": None
	}

	extension_data = {
		'nombEntrega': None,
	    'docuEntrega': None,
	    'nombRecibe': None,
	    'docuRecibe': None,
	    'observaciones': None
	}

	apendice_data = None

	json_data = {
		'identificacion': identificacion_data,
		'otrosDocumentos': otrosDocumentos_data,
		'ventaTercero': ventaTercero_data,
		'emisor': emisor_data,
		'receptor': receptor_data,
		'cuerpoDocumento': cuerpoDocumento_data,
		'resumen': resumen_data,
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


def fse_p(empresa, codigo): # 14 - Factura de sujeto excluido
	emisor = get_object_or_404(Empresa, codigo=empresa)
	from .funciones import CantLetras, CodGeneracion, Correlativo
	json_data = {}
	datos_emisor = {}
	datos_receptor = {}
	datos_detalle = []
	documento_relacionado = []
	tributos_consolidados = {}
	tributos_consolidados_lista = []

	identificacion_data = {
			'version': 1,
			'ambiente': '00',
			'tipoDte': '14',
			'numeroControl': Correlativo(cod_tipo='14', cod_empresa=empresa),
			'codigoGeneracion': codigo,
			'tipoModelo': 1,
			'tipoOperacion': 1,
			'fecEmi': datetime.now().strftime("%Y-%m-%d"),
			'horEmi': datetime.now().strftime("%H:%M:%S"),
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

	receptor_data = {'tipoDocumento': '36',
				    'numDocumento': '016312457',
				    'nombre': 'Proveedor de servicios',
				    'codActividad': '10005',
				    'descActividad': 'Otros',
				    'direccion': {
				      'departamento': '01',
				      'municipio': '03',
				      'complemento': 'Ferreteria La Industrial'
				    },
				    'telefono': '00000000',
				    'correo': 'cliente@cliente.com'
					}

	otrosDocumentos_data = None
	ventaTercero_data = None


	cuerpoDocumento_data = {
		"numItem": 1,
      "tipoItem": 1,
      "cantidad": 1.0,
      "codigo": None,
      "uniMedida": 99,
      "descripcion": "servicios",
      "precioUni": 1000.0,
      "montoDescu": 0.0,
      "compra": 1000.0
		},

	resumen_data = {
		"totalCompra": 1000.0,
	    "descu": 0.0,
	    "totalDescu": 0.0,
	    "subTotal": 1000.0,
	    "ivaRete1": 0.0,
	    "reteRenta": 100.0,
	    "totalPagar": 900.0,
	    "totalLetras": "NOVECIENTOS 00/100 USD",
	    "condicionOperacion": 1,
	    "pagos": None,
	    "observaciones": None
	}

	extension_data = None

	apendice_data = None

	json_data = {
			'identificacion': identificacion_data,
			'emisor': emisor_data,
			'sujetoExcluido': receptor_data,
			'cuerpoDocumento': cuerpoDocumento_data,
			'resumen': resumen_data,
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