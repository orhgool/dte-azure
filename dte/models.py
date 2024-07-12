import uuid
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class Departamento(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, default='001', null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column = 'Nombre', max_length = 200, default = 'N/A', blank=True, verbose_name='Nombre')

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Departamento'
		verbose_name_plural = 'Departamentos'
		ordering = ('nombre',)


class Municipio(models.Model):
	idMunicipio = models.CharField(db_column='Id', primary_key=True, default='001', null=False, max_length=50, verbose_name='Código')
	codigo = models.CharField(db_column='codigo', default='001', null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column = 'nombre', max_length = 200, default = 'N/A', blank=True, verbose_name='Nombre')
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, default=1)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Municipio'
		verbose_name_plural = 'Municipios'
		ordering = ('nombre',)


class Pais(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, default='001', null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column = 'Nombre', max_length = 200, default = 'N/A', blank=True, verbose_name='Nombre')

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'País'
		verbose_name_plural = 'Paises'
		ordering = ('nombre',)

class Actividadeconomica(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	descripcion = models.CharField(db_column = 'Descripcion', max_length = 200, default = 'N/A', blank=True, verbose_name='Descripción')
	
	def __str__(self):
		return "%s" % (self.descripcion)

	class Meta:
		verbose_name = 'Actividad económica'
		verbose_name_plural = 'Actividades económicas'
		ordering = ['descripcion',]


class TipoContribuyente(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, default='001', null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column = 'Nombre', max_length = 200, default = 'N/A', blank=True, verbose_name='Nombre')

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de contribuyente'
		verbose_name_plural = 'Tipos de contribuyente'
		ordering = ('codigo',)


class TipoDocumentoIdentificacion(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Numero', max_length=50, blank=True, null=True, verbose_name='Número de documento')

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		ordering = ('nombre',)

    
class AmbienteDestino(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Ambiente de destino'
		verbose_name_plural = "Ambientes de destino"
		ordering = ('nombre',)


class TipoPersona(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de persona'
		verbose_name_plural = "Tips de persona"
		ordering = ('nombre',)


class TipoEstablecimiento(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de establecimiento'
		verbose_name_plural = "Tipos de establecimiento"
		ordering = ('codigo',)


class Empresa(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	razonsocial = models.CharField(db_column='RazonSocial', max_length=100, blank=True, null=True, verbose_name='Razón social')
	nombreComercial = models.CharField(db_column='NombreComercial', max_length=50, blank=True, null=True, default='', verbose_name='Nombre comercial')
	nit = models.CharField(db_column='NIT', max_length=20, blank=True, null=True, verbose_name='NIT')
	nrc = models.CharField(db_column='NRC', max_length=10, blank=True, null=True, verbose_name='NRC')
	dui = models.CharField(db_column='DUI', max_length=10, blank=True, null=True, verbose_name='DUI')
	telefono = models.CharField(db_column='Telefono', max_length=50, blank=True, null=True, verbose_name='Teléfono')
	correo = models.EmailField(db_column='Correo', max_length=200, blank=True, null=True, verbose_name='Correo')
	actividadEconomica = models.ForeignKey(Actividadeconomica, on_delete=models.CASCADE, null=False, default='001', verbose_name='Actividad económica')
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=False, default='001', verbose_name='País')
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, default='001')
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=False, default='001')
	direccionComplemento = models.TextField(db_column='Direccion', max_length=200, blank=True, null=True, verbose_name='Dirección')
	ambiente = models.ForeignKey(AmbienteDestino, on_delete=models.CASCADE, null=False, default='001')
	tipoContribuyente = models.ForeignKey(TipoContribuyente, on_delete=models.CASCADE, null=False, default='001', verbose_name='Tipo de contribuyente')
	tipoPersona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE, null=False, default=1, verbose_name='Tipo de persona')
	tipoEstablecimiento = models.ForeignKey(TipoEstablecimiento, on_delete=models.CASCADE, null=False, default='02', verbose_name='Tipo de establecimiento')
	codigoEstablecimiento = models.CharField(db_column='codigoEstablecimiento', max_length=4, blank=True, null=True, default='0000', verbose_name='Código de establecimiento')
	codigoPuntoVenta = models.CharField(db_column='codigoPuntoVenta', max_length=4, blank=True, null=True, default='0000', verbose_name='Código de punto de venta')
	usuarioMH = models.CharField(db_column='UsuarioMH', null=False, max_length=50, default='', verbose_name='Usuario en Ministerio de Hacienda')
	passwordAPI = models.CharField(db_column='PasswordAPI', null=False, default='', max_length=50, verbose_name='Clave acceso API (generar token MH)')
	passwordPri = models.CharField(db_column='PasswordPri', null=False, default='', max_length=50, verbose_name='Clave privada')
	token = models.TextField(db_column='Token', null=False, default='', max_length=500, verbose_name='Token')
	fechaToken = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha y hora del token')
	logo = models.ImageField(upload_to='logos/', null=True, blank=True)
	correoPrivado = models.BooleanField(null=False, blank=True, default=False, verbose_name='Usar correo privado')
	correoUsuario = models.EmailField(null=True, blank=True, default='', max_length=50, verbose_name='Usuario de correo')
	correoClave = models.CharField(null=True, blank=True, default='', max_length=50, verbose_name='Clave de correo')
	correoServidorSmtp = models.CharField(null=True, blank=True, default='', max_length=50, verbose_name='Servidor SMTP')
	correoPuertoSmtp = models.IntegerField(null=True, blank=True, default=587, verbose_name='Puerto SMTP')
	correoEnableSsl = models.BooleanField(null=True, blank=True, default=True, verbose_name='Utiliza SSL')
	


	def __str__(self):
		return "%s" % (self.razonsocial.strip())

	class Meta:
		ordering = ('razonsocial',)


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')

	def __str__(self):
		return self.user.username

class Cliente(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	razonsocial = models.CharField(db_column='RazonSocial', max_length=100, blank=False, null=False, default='', verbose_name='Razón social')
	nombreComercial = models.CharField(db_column='NombreComercial', max_length=50, blank=True, null=True, default='', verbose_name='Nombre comercial')
	tipoDocumentoCliente = models.ForeignKey(TipoDocumentoIdentificacion, on_delete=models.CASCADE, null=False, default='001', verbose_name='Tipo de documento')
	numeroDocumento = models.CharField(db_column='numeroDocumento', max_length=50, blank=False, null=False, default='', verbose_name='Número de documento')
	nrc = models.CharField(db_column='NRC', max_length=10, blank=True, null=True, default='', verbose_name='NRC')
	telefono = models.CharField(db_column='Telefono', max_length=50, blank=False, null=False, default='', verbose_name='Teléfono') #, hint='Número de teléfono sin guines')
	correo = models.CharField(db_column='Correo', max_length=200, blank=False, null=False, default='', verbose_name='Correo 1')
	correo2 = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name='Correo 2')
	correo3 = models.CharField(max_length=200, blank=False, null=False, default='', verbose_name='Correo 3')
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	actividadEconomica = models.ForeignKey(Actividadeconomica, on_delete=models.CASCADE, null=False, default='001', verbose_name='Actividad económica')
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=False, default='001', verbose_name='País')
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True, default='001', verbose_name='Departamento')
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True, default='001', verbose_name='Municipio')
	direccionComplemento = models.CharField(db_column='Direccion', max_length=200, blank=True, default='', null=True, verbose_name='Dirección')
	tipoContribuyente = models.ForeignKey(TipoContribuyente, on_delete=models.CASCADE, null=False, default='001', verbose_name='Tipo de contribuyente')
	tipoPersona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE, null=False, default=1, verbose_name='Tipo de persona')
	agenteRetencion = models.BooleanField(null=True, blank=True, default=False, verbose_name='Cliente es agente de retención')
	diasCredito = models.IntegerField(null=True, blank=True, default=30, verbose_name='Días crédito')
	
	def __str__(self):
		return "%s" % (self.razonsocial.strip())

	class Meta:
		ordering = ('razonsocial',)

class Proveedor(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	razonsocial = models.CharField(db_column='RazonSocial', max_length=100, blank=True, null=True, verbose_name='Razón social')
	nombreComercial = models.CharField(db_column='NombreComercial', max_length=50, blank=True, null=True, default='', verbose_name='Nombre comercial')
	tipoDocumentoProveedor = models.ForeignKey(TipoDocumentoIdentificacion, on_delete=models.CASCADE, null=False, default='001', verbose_name='Tipo de documento')
	numeroDocumento = models.CharField(db_column='numeroDocumento', max_length=50, blank=True, null=True, verbose_name='Número de documento')
	nrc = models.CharField(db_column='NRC', max_length=10, blank=True, null=True, default='', verbose_name='NRC')
	telefono = models.CharField(db_column='Telefono', max_length=50, blank=True, null=True, verbose_name='Teléfono')
	correo = models.CharField(db_column='Correo', max_length=200, blank=True, null=True, verbose_name='Correo')
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	actividadEconomica = models.ForeignKey(Actividadeconomica, on_delete=models.CASCADE, null=False, default='001', verbose_name='Actividad económica')
	pais = models.ForeignKey(Pais, on_delete=models.CASCADE, null=False, default='001')
	departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, default='001')
	municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=False, default='001')
	direccionComplemento = models.CharField(db_column='Direccion', max_length=200, blank=True, null=True, verbose_name='Dirección')
	tipoContribuyente = models.ForeignKey(TipoContribuyente, on_delete=models.CASCADE, null=False, default='001', verbose_name='Tipo de contribuyente')
	tipoPersona = models.ForeignKey(TipoPersona, on_delete=models.CASCADE, null=False, default=1, verbose_name='Tipo de persona')


	def __str__(self):
		return "%s" % (self.razonsocial.strip())

	class Meta:
		ordering = ('razonsocial',)


class UnidadMedida(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Unidad de medida'
		verbose_name_plural = "Unidades de medida"
		ordering = ('nombre',)


class Producto(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, max_length=50, default='')
	nombre = models.CharField(db_column='Nombre', max_length=200, blank=True, null=True)
	precio = models.DecimalField(db_column='Precio', max_digits=18, decimal_places=2, blank=True, default=0, null=True, verbose_name='Precio')
	unidadMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, default=59, verbose_name='Unidad de medida')
	existencia = models.DecimalField(db_column='Existencia', max_digits=18, decimal_places=2, blank=True, default=0, null=True, verbose_name='Existencia')
	cantidadMinima = models.DecimalField(db_column='CantidadMinima', max_digits=18, decimal_places=2, blank=True, default=0, null=True, verbose_name='Cantidad mínima')
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		ordering = ('nombre',)


class Configuracion(models.Model):
	usuarioCorreo = models.EmailField(null=False, default='none@usuario.com', max_length=50, verbose_name='Usuario de correo')
	claveCorreo = models.CharField(null=False, default='', max_length=50, verbose_name='Clave de correo')
	servidorSmtp = models.CharField(null=False, default='', max_length=50, verbose_name='Servidor SMTP')
	puertoSmtp = models.IntegerField(null=False, default=587, verbose_name='Puerto SMTP')
	enableSsl = models.BooleanField(null=False, default=True, verbose_name='Utiliza SSL')
	blobUrl = models.CharField(null=False, default='', max_length=100, verbose_name='Blob url')
	blobContenedor = models.CharField(null=False, default='', max_length=50, verbose_name='Blob contenedor')
	blobCadenaConexion = models.TextField(null=False, default='', max_length=500, verbose_name='Blob cadena de conexión')
	
	def __str__(self):
		return 'Configuración'

	class Meta:
		verbose_name = 'Configuración'
		verbose_name_plural = 'Configuración'

class UrlSistema(models.Model):
	tipo = models.CharField(db_column='tipo', max_length=20, null=False, blank=False, default='', verbose_name='Tipo')
	url = models.URLField(db_column='URLFirmado', null=False, max_length=100, default='', verbose_name='Url para firmar DTE')
	ambiente = models.ForeignKey(AmbienteDestino, on_delete=models.CASCADE, default='00', verbose_name='Ambiente')
	
	def __str__(self):
		return '%s %s (%s)' % (self.tipo, self.ambiente, self.url)

	class Meta:
		verbose_name = 'URL del sistema'
		verbose_name_plural = 'URLs del sistema'


class TipoDocumento(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)
	nombre_corto = models.CharField(db_column='NombreCorto', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de documento'
		verbose_name_plural = "Tipos de documento"
		ordering = ('codigo',)


class ModeloFacturacion(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Modelo de facturación'
		verbose_name_plural = "Modelos de facturación"
		ordering = ('nombre',)


class TipoTransmision(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de transmisión'
		verbose_name_plural = "Tipos de transmisión"
		ordering = ('nombre',)


class TipoContingencia(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de contingencia'
		verbose_name_plural = "Tipos de contingencia"
		ordering = ('nombre',)


class RetencionIVAMH(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Retención IVA MH'
		verbose_name_plural = "Retenciones IVA MH"
		ordering = ('nombre',)


class TipoGeneracionDocumento(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de generación del documento'
		verbose_name_plural = "Tipos de generación de los documentos"
		ordering = ('nombre',)


class TipoServicioMedico(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de servicio médico'
		verbose_name_plural = "Tipos de servicios médicos"
		ordering = ('nombre',)


class TipoItem(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de ítem'
		verbose_name_plural = "Tipos de ítem"
		ordering = ('codigo',)


class TributoResumen(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tributo resumen'
		verbose_name_plural = 'Tributos resumen'
		ordering = ('nombre',)



class TributoCuerpo(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tributo cuerpo'
		verbose_name_plural = "Tributos cuerpo"
		ordering = ('nombre',)

class ImpuestoAdValorem(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Impuesto AD Valorem'
		verbose_name_plural = "Impuestos AD Valorem"
		ordering = ('nombre',)


class CondicionOperacion(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Condición de la operación'
		verbose_name_plural = "Condiciones de la operaciones"
		ordering = ('nombre',)


class FormaPago(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Forma de pago'
		verbose_name_plural = "Formas de pago"
		ordering = ('nombre',)


class Plazo(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Plazo'
		verbose_name_plural = "Plazos"
		ordering = ('nombre',)


class OtroDocumentoAsociado(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Otro documento asociado'
		verbose_name_plural = "Otros documentos asociados"
		ordering = ('nombre',)


class TipoDocumentoContingencia(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de documento en contingencia'
		verbose_name_plural = "Tipos de documento en contingencia"
		ordering = ('nombre',)

class TipoInvalidacion(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de invalidación'
		verbose_name_plural = "Tipos de invalidación"
		ordering = ('codigo',)


class TituloRemision(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Título a que se remiten los bienes'
		verbose_name_plural = "Títulos a que se remiten los bienes"
		ordering = ('codigo',)


class TipoDonacion(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de donación'
		verbose_name_plural = "Tipos de donación"
		ordering = ('codigo',)


class RecintoFiscal(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Recinto fiscal'
		verbose_name_plural = "Recintos fiscales"
		ordering = ('nombre',)


class Regimen(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 300, default = 'N/A', blank=True)

	def __str__(self):
		return "%s %s" % (self.codigo, self.nombre)

	class Meta:
		verbose_name = 'Régimen'
		verbose_name_plural = "Regimenes"
		ordering = ('nombre',)


class Transporte(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Tipo de transporte'
		verbose_name_plural = "Tipos de transporte"
		ordering = ('codigo',)


class Incoterms(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Incoterms'
		verbose_name_plural = "Incoterms"
		ordering = ('nombre',)


class DomicilioFiscal(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Domicilio fiscal'
		verbose_name_plural = "Domicilios fiscales"
		ordering = ('nombre',)


class Moneda(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)
	prefijo = models.CharField(db_column='Prefijo', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Moneda'
		verbose_name_plural = "Monedas"
		ordering = ('nombre',)


class EstadoDTE(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Estado DTE'
		verbose_name_plural = "Estados de DTE"
		ordering = ('codigo',)


class EstadoPago(models.Model):
	codigo = models.CharField(db_column='Codigo', primary_key=True, null=False, max_length=50, verbose_name='Código')
	nombre = models.CharField(db_column='Nombre', max_length = 100, default = 'N/A', blank=True)

	def __str__(self):
		return "%s" % (self.nombre)

	class Meta:
		verbose_name = 'Estado de pago'
		verbose_name_plural = "Estados de pago"
		ordering = ('codigo',)


class ControlDocumento(models.Model):
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
	numeroactual = models.IntegerField(db_column='NumeroActual', default=0, verbose_name='Número actual')

	def __str__(self):
		return "%s - %s - %s" % (self.empresa, self.tipo, self.numeroactual)

	class Meta:
		verbose_name = 'Control documento'
		verbose_name_plural = "Control documentos"
		ordering = ('empresa',)


class DTECliente(models.Model):
	emisor = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	receptor = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
	selloRecepcion = models.CharField(db_column = 'SelloRecepcion', max_length = 100, default = '', null=True, blank=True, verbose_name='Sello de recepción')
	version = models.IntegerField(db_column = 'Version', verbose_name='Versión JSON', default=3)
	ambiente = models.ForeignKey(AmbienteDestino, on_delete=models.CASCADE, default='00', verbose_name='Ambiente de trabajo')
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE,default='', verbose_name='Tipo DTE')
	numeroControl = models.CharField(max_length=31, default='', null=True, blank=True, verbose_name='Número de control')
	codigoGeneracion = models.CharField(primary_key=True, default='', max_length=36, verbose_name='Código de generación')
	tipoModelo = models.ForeignKey(ModeloFacturacion, on_delete=models.CASCADE, db_column = 'TipoModelo', default='1', verbose_name='Tipo de modelo')
	tipoTransmision = models.ForeignKey(TipoTransmision, on_delete=models.CASCADE, db_column = 'TipoTransmision', default='1', verbose_name='Tipo de transmisión')
	tipoContingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, blank=True,db_column = 'TipoContingencia', max_length=10, null=True, verbose_name='Tipo de contingencia')
	motivoContin = models.CharField(max_length=255, blank=True, null=True, default='', verbose_name='Motivo de contingencia')
	fecEmi = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de emisión')
	tipoMoneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, default = '001')
	totalNoSuj = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total no sujetas')
	totalExenta = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total exentas')
	totalGravada = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Total gravadas')
	subTotalVentas = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Sub-total ventas')
	descuNoSuj = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Descuento no sujetas')
	descuExenta = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Descuento exentas')
	descuGravada = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Descuento gravadas')
	porcentajeDescuento = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Porcentaje descuento')
	totalDescu = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total descuento')
	subTotal = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Sub total')
	totalCompra = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total compra')
	ivaPerci1 = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='IVA percibido')
	ivaRete1 = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='IVA retenido')
	reteRenta = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Retención de renta')
	montoTotalOperacion = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Monto total de operación')
	totalNoGravado = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total no gravado')
	totalPagar = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total a pagar')
	totalLetras = models.CharField(max_length=200, blank=True, null=True, default='' , verbose_name='Total en letras')
	saldoFavor = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Saldo a favor')
	condicionOperacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, db_column = 'CondicionOperacion', default='2', verbose_name='Condición de la operación')
	pagos = models.IntegerField(blank=True, default=1)
	numPagoElectronico = models.IntegerField(null=True, blank=True, verbose_name='Número de pago electrónico')
	observaciones = models.CharField(max_length=3000, null=True, blank=True, default='', verbose_name='Observaciones')
	placaVehiculo = models.CharField(max_length=10, blank=True, null=True, verbose_name='Placa del vehículo')
	estadoDte = models.ForeignKey(EstadoDTE, on_delete=models.CASCADE, null=False, blank=True, default='001', verbose_name='Estado del DTE')
	estadoPago = models.BooleanField(null=False, blank=True, default=True, verbose_name='Pagado')
	docfirmado = models.TextField(null=True, blank=True, verbose_name='Documento firmado')
	fechaPago = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de pago')
	tipoItemExpor = models.ForeignKey(TipoItem, on_delete=models.CASCADE, null=True, blank=True, default=2, verbose_name='Tipo ítem de exportación')
	recintoFiscal = models.ForeignKey(RecintoFiscal, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name='Recinto fiscal')
	regimen = models.ForeignKey(Regimen, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name='Regimen')
	incoterms = models.ForeignKey(Incoterms, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name='Incoterms')
	diasCredito = models.IntegerField(null=True, blank=True, default=30, verbose_name='Días crédito')
	tituloRemision = models.ForeignKey(TituloRemision, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Título remisión')
		
	def __str__(self):
		return "%s" % (self.numeroControl)

	def rz(self):
		return "%s" % (self.razonsocial)

	def save(self, *args, **kwargs):
		from .funciones import Correlativo
		if not self.numeroControl and self.tipoDte_id:
			self.numeroControl = Correlativo(self.emisor, self.tipoDte_id)

		super().save(*args, **kwargs)

	class Meta:
		verbose_name = 'DTE de cliente'
		verbose_name_plural = "DTE's de clientes"
		ordering = ('-fecEmi',)		


class DTEClienteDetalle(models.Model):
	codigoDetalle = models.CharField(db_column='CodigoDetalle', primary_key=True, blank=True, max_length=36)
	dte = models.ForeignKey(DTECliente, on_delete=models.CASCADE, blank=True, default='', related_name='detalles')
	tipoItem = models.ForeignKey(TipoItem, on_delete=models.CASCADE, db_column='tipoItem_id', default=2, verbose_name='Tipo de ítem')
	tipoDoc = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, default='01', verbose_name='Tipo de documento')
	tipoGeneracion = models.ForeignKey(TipoGeneracionDocumento, on_delete=models.CASCADE, default=2, verbose_name='Tipo de generación')
	numeroDocumento = models.CharField(db_column='numeroDocumento', max_length=36, blank=True, null=True, default='', verbose_name='Número de documento')
	fechaEmision = models.DateTimeField(db_column = 'FechaEmision', default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de emisión')
	cantidad = models.DecimalField(db_column='Cantidad', max_digits=11, decimal_places=3, blank=True, default=1, verbose_name='Cantidad')
	codigo = models.CharField(db_column='Codigo', max_length=25, blank=True, default='', verbose_name='Codigo')
	uniMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, db_column='uniMedida_id', default='59', verbose_name='Unidad de medida')
	descripcion = models.CharField(db_column='Descripcion', max_length=1000, default='', verbose_name='Descripción')
	precioUni = models.DecimalField(db_column='PrecioUnitario', max_digits=11, decimal_places=4, default=0, verbose_name='Precio unitario')
	montoDescu = models.DecimalField(db_column='MontoDescuento', max_digits=11, decimal_places=2, default=0, verbose_name='Monto de descuento')
	ventaNoSuj = models.DecimalField(db_column='VentaNoSujeta', max_digits=11, decimal_places=2, default=0, verbose_name='Venta no sujeta')
	ventaExenta = models.DecimalField(db_column='VentaExenta', max_digits=11, decimal_places=2, default=0, verbose_name='Venta exenta')
	ventaGravada = models.DecimalField(db_column='VentaGravada', max_digits=11, decimal_places=4, default=0, verbose_name='Venta gravada')
	exportaciones = models.DecimalField(db_column='Exportaciones', max_digits=11, decimal_places=2, default=0)
	compra = models.DecimalField(db_column='Compra', max_digits=11, decimal_places=2, default=0)
	tributos = models.ForeignKey(TributoResumen, on_delete=models.CASCADE, db_column='tributos_id', blank=True, default='20')
	psv = models.DecimalField(db_column='PSV', max_digits=11, decimal_places=2, default=0, verbose_name='Precio sugerido de venta')
	noGravado = models.DecimalField(db_column='NoGravado', max_digits=11, decimal_places=2, default=0, verbose_name='No gravado')
	ivaItem = models.DecimalField(db_column='IVAItem', max_digits=11, decimal_places=2, default=0, verbose_name='IVA item')
	montoSujetoGrav = models.DecimalField(db_column='MontoSujetoGravado', max_digits=11, decimal_places=2, default=0, verbose_name='Monto sujeto gravado')
	codigoRetencionMH = models.DecimalField(db_column='CodigoRetencionMH', max_digits=11, decimal_places=2, default=0, verbose_name='Código retención MH')
	ivaRetenido = models.DecimalField(db_column='IVARetenido', max_digits=11, decimal_places=4, default=0, verbose_name='IVA retenido')
	periodoLiquidacionFechaInicio = models.DateTimeField(db_column='PeriodoLiquidacionFechaInicio', default=datetime.now, verbose_name='Inicio período liquidación')
	periodoLiquidacionFechaFin = models.DateTimeField(db_column='PeriodoLiquidacionFechaFin', default=datetime.now, verbose_name='Fin período liquidación')
	codLiquidacion = models.CharField(db_column='CodigoLiquidacion', max_length=30, default='', verbose_name='Código de liquidación')
	cantidadDoc = models.IntegerField(db_column='CantidadDocumentos', default=0, verbose_name='Cantidad documentos')
	valorOperaciones = models.DecimalField(db_column='ValorOperaciones', max_digits=11, decimal_places=2, default=0, verbose_name='Valor operaciones')
	montoSinPercepcion = models.DecimalField(db_column='MontoSinPercepcion', max_digits=11, decimal_places=2, default=0, verbose_name='Monto sin percepción')
	descripcionPercepcion = models.CharField(db_column='DescripcionPercepcion', max_length=100, default='', verbose_name='Descripción percepción')
	obsitem = models.CharField(db_column = 'ObsItem', max_length=3000, null=True, default='', verbose_name='Observaciones')
	observaciones = models.CharField(db_column = 'Observaciones', max_length=200, null=True, default='', verbose_name='Observaciones')
	complemento1 = models.CharField(db_column = 'Complemento1', max_length=3000, null=True, blank=True, default='', verbose_name='Complemento 1')
	complemento2 = models.CharField(db_column = 'Complemento2', max_length=3000, null=True, blank=True, default='', verbose_name='Complemento 2')
	subTotal = models.DecimalField(db_column='SubTotal', max_digits=11, decimal_places=2, default=0, verbose_name='Sub-total')
	iva = models.DecimalField(db_column='IVA', max_digits=11, decimal_places=4, default=0)
	montoSujetoPercepcion = models.DecimalField(db_column='MontoSujetoPercepcion', max_digits=11, decimal_places=2, default=0, verbose_name='Monto sujeto percepción')
	ivaPercibido = models.DecimalField(db_column='IVAPercibido', max_digits=11, decimal_places=4, default=0, verbose_name='IVA Percibido')
	comision = models.DecimalField(db_column='Comision', max_digits=11, decimal_places=2, default=0, verbose_name='Comisión')
	porcentComision = models.DecimalField(db_column='PorcentajeComision', max_digits=11, decimal_places=2, default=0, verbose_name='Porcentaje comisión')
	IVAComision = models.DecimalField(db_column='IVAComision', max_digits=11, decimal_places=2, default=0, verbose_name='IVA comisión')
	liquidoApagar = models.DecimalField(db_column='LiquidoAPagar', max_digits=11, decimal_places=2, default=0, verbose_name='Líquido a pagar')
	totalLetras = models.CharField(db_column='TotalLetras', max_length=200, default='', verbose_name='Total en letras')
	

	def __str__(self):
		return "%s" % (self.codigoDetalle)

	def save(self, *args, **kwargs):
		if not self.codigoDetalle:
			self.codigoDetalle = str(uuid.uuid4())
		super().save(*args, **kwargs)

	class Meta:
		verbose_name = 'DTE cliente detalle'
		verbose_name_plural = "DTE's cliente detalles"

class DTEClienteDetalleTributo(models.Model):
	codigoDetalle = models.ForeignKey(DTEClienteDetalle, on_delete=models.CASCADE)
	codigo = models.ForeignKey(TributoResumen, on_delete=models.CASCADE)
	descripcion = models.CharField(db_column='Descripcion', max_length=100, blank=True, default='', verbose_name='Descripción del tributo')
	valor = models.DecimalField(db_column='Valor', max_digits=11, decimal_places=2, default=0)

	def __str__(self):
		return "%s - %s" % (self.codigoDetalle, self.codigo)

	class Meta:
		verbose_name = 'DTE Cliente Detalle tributo'
		verbose_name_plural = "DTE Cliente Detalle tributos"


class DTEProveedor(models.Model):
	emisor = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	receptor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	version = models.IntegerField(verbose_name='Versión JSON', default=3)
	ambiente = models.ForeignKey(AmbienteDestino, on_delete=models.CASCADE, default='00', verbose_name='Ambiente de trabajo')
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, default='', verbose_name='Tipo DTE')
	numeroControl = models.CharField(max_length=31, default='', blank=True, verbose_name='Número de control')
	codigoGeneracion = models.CharField(primary_key=True, default='', max_length=36, verbose_name='Código de generación')
	selloRecepcion = models.CharField(max_length = 100, default = '', blank=True, verbose_name='Sello de recepción')
	tipoModelo = models.ForeignKey(ModeloFacturacion, on_delete=models.CASCADE, default='1', verbose_name='Tipo de modelo')
	tipoTransmision = models.ForeignKey(TipoTransmision, on_delete=models.CASCADE, default='1', verbose_name='Tipo de transmisión')
	tipoContingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, blank=True,db_column = 'TipoContingencia', max_length=10, null=True, verbose_name='Tipo de contingencia')
	motivoContin = models.CharField(max_length=255, blank=True, null=True, default='', verbose_name='Motivo de contingencia')
	fecEmi = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de emisión')
	tipoMoneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, default = '001', verbose_name='Tipo moneda')
	totalCompra = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total compra')
	descu = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Descuento')
	totalDescu = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total descuento')
	subTotal = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Sub total')
	totalSujetoRetencion = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total sujeto retención')
	ivaRete1 = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='IVA retenido')
	reteRenta = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Retención de renta')
	totalPagar = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total a pagar')
	totalIVARetenido = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total IVA Retenido')
	condicionOperacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, db_column = 'CondicionOperacion', default='2', verbose_name='Condición de la operación')
	pagos = models.IntegerField(blank=True, default=1, verbose_name='Pagos')
	observaciones = models.CharField(max_length=3000, null=True, blank=True, default='', verbose_name='Observaciones')
	estadoPago = models.BooleanField(null=False, blank=True, default=True, verbose_name='Pagado')
	estadoDte = models.ForeignKey(EstadoDTE, on_delete=models.CASCADE, null=False, blank=True, default='001', verbose_name='Estado del DTE')
	docfirmado = models.TextField(null=True, blank=True, verbose_name='Documento firmado')
		
	def __str__(self):
		return "%s" % (self.numeroControl)

	def save(self, *args, **kwargs):
		from .funciones import Correlativo
		if not self.numeroControl and self.tipoDte_id:
			self.numeroControl = Correlativo(self.emisor, self.tipoDte_id)

		super().save(*args, **kwargs)

	class Meta:
		verbose_name = 'DTE de proveedor'
		verbose_name_plural = "DTE's de proveedor"
		ordering = ('-fecEmi',)


class DTEProveedorDetalle(models.Model):
	codigoDetalle = models.CharField(primary_key=True, blank=False, max_length=36, default='')
	dte = models.ForeignKey(DTEProveedor, on_delete = models.CASCADE, blank=True, default='', related_name='detalles')
	tipoItem = models.ForeignKey(TipoItem, on_delete=models.CASCADE, db_column='tipoItem_id', default=1, verbose_name='Tipo de ítem')
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, default='03', verbose_name='Tipo DTE')
	tipoGeneracion = models.ForeignKey(TipoGeneracionDocumento, on_delete=models.CASCADE, default=2, verbose_name='Tipo de generación')
	numeroDocumento = models.CharField(max_length=50, blank=True, default='', verbose_name='Número de documento')
	fechaEmision = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de emisión')
	cantidad = models.DecimalField(max_digits=11, decimal_places=3, blank=True, default=1, verbose_name='Cantidad')
	codigo = models.CharField(max_length=25, blank=True, default='', verbose_name='Código')
	uniMedida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, db_column='uniMedida_id', default='59', verbose_name='Unidad de medida')
	descripcion = models.CharField(max_length=1000, default='', verbose_name='Descripción')
	complemento1 = models.CharField(db_column = 'Complemento1', max_length=3000, null=True, blank=True, default='', verbose_name='Complemento 1')
	precioUni = models.DecimalField(max_digits=11, decimal_places=2, default=0, verbose_name='Precio unitario')
	montoDescu = models.DecimalField(max_digits=11, decimal_places=2, default=0, verbose_name='Monto de descuento')
	compra = models.DecimalField(max_digits=11, decimal_places=2, default=0, verbose_name='Compra')
	montoSujetoGrav = models.DecimalField(max_digits=11, decimal_places=2, default=0, verbose_name='Monto sujeto gravado')
	codigoRetencionMH = models.ForeignKey(RetencionIVAMH, on_delete=models.CASCADE, default='C4', verbose_name='Código retención MH')
	ivaRetenido = models.DecimalField(max_digits=11, decimal_places=2, default=0, verbose_name='IVA retenido')
	

	def __str__(self):
		return "%s" % (self.codigoDetalle)

	def save(self, *args, **kwargs):
		if not self.codigoDetalle:
			self.codigoDetalle = str(uuid.uuid4())
		super().save(*args, **kwargs)

	class Meta:
		verbose_name = 'DTE proveedor detalle'
		verbose_name_plural = "DTE's proveedor detalles"


class DTEProveedorDetalleTributo(models.Model):
	codigoDetalle = models.ForeignKey(DTEProveedorDetalle, on_delete=models.CASCADE)
	codigo = models.ForeignKey(TributoResumen, on_delete=models.CASCADE)
	descripcion = models.CharField(max_length=100, blank=True, default='', verbose_name='Descripción del tributo')
	valor = models.DecimalField(max_digits=11, decimal_places=2, default=0)

	def __str__(self):
		return "%s - %s" % (self.codigoDetalle, self.codigo)

	class Meta:
		verbose_name = 'DTE Proveedor Detalle tributo'
		verbose_name_plural = "DTE Proveedor Detalle tributos"		


class DTEInvalidacion(models.Model):
	codigoGeneracion = models.CharField(primary_key=True, default='', max_length=36, verbose_name='Código de generación')
	numeroDocumento = models.CharField(max_length=50, blank=True, null=True, default=None, verbose_name='Número de documento')
	emisor = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	receptor = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
	receptor_tmp = models.CharField(max_length=36, blank=True, null=True, default='')
	codigoDte = models.CharField(default='', max_length=36, verbose_name='Código DTE a anular')
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, db_column = 'TipoDTE', default='', verbose_name='Tipo DTE')
	fechaEmision = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de emisión')
	tipoInvalidacion = models.ForeignKey(TipoInvalidacion, on_delete=models.CASCADE, default=2, verbose_name='Tipo de anulación')
	docfirmado = models.TextField(db_column='DocFirmado', null=True, blank=True, verbose_name='Documento firmado')
	selloRecepcion = models.CharField(default='', max_length=50, verbose_name='Sello de recepción')
	

	def __str__(self):
		return self.codigoGeneracion

	class Meta:
		verbose_name = 'Invalidación DTE'
		verbose_name_plural = "Invalidaciones de DTE's"



class DTEContingencia(models.Model):
	codigoGeneracion = models.CharField(primary_key=True, default='', max_length=36, verbose_name='Código de generación')
	numeroControl = models.CharField(max_length=31, default='', null=True, blank=True, verbose_name='Número de control')
	version = models.IntegerField(verbose_name='Versión JSON', default=3)
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, default='03', verbose_name='Tipo DTE')
	ambiente = models.ForeignKey(AmbienteDestino, on_delete=models.CASCADE, db_column = 'Ambiente', default='00', verbose_name='Ambiente de trabajo')
	emisor = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	fTransmision = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de transmisión')
	tipoContingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, default=1, verbose_name='Tipo de contingencia')
	fInicio = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha inicio de contingencia')
	fFinal = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha fin de contingencia')
	docfirmado = models.TextField(null=True, blank=True, verbose_name='Documento firmado')
	selloRecepcion = models.CharField(default='', max_length=50, verbose_name='Sello de recepción')
	

	def __str__(self):
		return self.codigoGeneracion

	class Meta:
		ordering = ('-fTransmision',)
		verbose_name = 'DTE de contingencia'
		verbose_name_plural = "DTE's de contingencia"

class DTEContingenciaDetalle(models.Model):
	dteContingencia = models.ForeignKey(DTEContingencia, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Dte')
	tipoDte = models.ForeignKey(TipoDocumentoContingencia, on_delete=models.CASCADE, default='', verbose_name='Tipo DTE')
	codigoGeneracionDTE = models.CharField(default='', max_length=36, null=True, blank=True, verbose_name='Codigo DTE a reportar')
	
	def __str__(self):
		return 'DTE %s - detalle %s' % (self.dteContingencia, self. codigoGeneracionDTE)

	class Meta:
		verbose_name = 'Detalle contingencia DTE'
		verbose_name_plural = "Detalles contingencia de DTE's"



class DTECompra(models.Model):
	codigoGeneracion = models.CharField(primary_key=True, default='', max_length=36, verbose_name='Código de generación')
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='A4BCBC83-4C59-4A3F-9C25-807D83AD0837')
	proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, null=True, blank=True)
	selloRecepcion = models.CharField(db_column = 'SelloRecepcion', max_length = 100, default = '', null=True, blank=True, verbose_name='Sello de recepción')
	version = models.IntegerField(db_column = 'Version', verbose_name='Versión JSON', default=3)
	ambiente = models.ForeignKey(AmbienteDestino, on_delete=models.CASCADE, default='00', verbose_name='Ambiente de trabajo')
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE,default='', verbose_name='Tipo DTE')
	numeroControl = models.CharField(max_length=31, default='', null=True, blank=True, verbose_name='Número de control')
	tipoModelo = models.ForeignKey(ModeloFacturacion, on_delete=models.CASCADE, db_column = 'TipoModelo', default='1', verbose_name='Tipo de modelo')
	tipoTransmision = models.ForeignKey(TipoTransmision, on_delete=models.CASCADE, db_column = 'TipoTransmision', default='1', verbose_name='Tipo de transmisión')
	tipoContingencia = models.ForeignKey(TipoContingencia, on_delete=models.CASCADE, blank=True,db_column = 'TipoContingencia', max_length=10, null=True, verbose_name='Tipo de contingencia')
	motivoContin = models.CharField(max_length=255, blank=True, null=True, default='', verbose_name='Motivo de contingencia')
	fecEmi = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de emisión')
	tipoMoneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, default = '001')
	totalNoSuj = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total no sujetas')
	totalExenta = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total exentas')
	totalGravada = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Total gravadas')
	subTotalVentas = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Sub-total ventas')
	descuNoSuj = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Descuento no sujetas')
	descuExenta = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Descuento exentas')
	descuGravada = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Descuento gravadas')
	porcentajeDescuento = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Porcentaje descuento')
	totalDescu = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total descuento')
	subTotal = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Sub total')
	totalCompra = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total compra')
	ivaPerci1 = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='IVA percibido')
	ivaRete1 = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='IVA retenido')
	reteRenta = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Retención de renta')
	montoTotalOperacion = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True, default=0.0 , verbose_name='Monto total de operación')
	totalNoGravado = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total no gravado')
	totalPagar = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Total a pagar')
	totalLetras = models.CharField(max_length=200, blank=True, null=True, default='' , verbose_name='Total en letras')
	saldoFavor = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, default=0.0 , verbose_name='Saldo a favor')
	condicionOperacion = models.ForeignKey(CondicionOperacion, on_delete=models.CASCADE, db_column = 'CondicionOperacion', default='2', verbose_name='Condición de la operación')
	pagos = models.IntegerField(blank=True, default=1)
	numPagoElectronico = models.IntegerField(null=True, blank=True, verbose_name='Número de pago electrónico')
	observaciones = models.CharField(max_length=3000, null=True, blank=True, default='', verbose_name='Observaciones')
	placaVehiculo = models.CharField(max_length=10, blank=True, null=True, verbose_name='Placa del vehículo')
	estadoPago = models.BooleanField(null=False, blank=True, default=True, verbose_name='Pagado')
	docfirmado = models.TextField(null=True, blank=True, verbose_name='Documento firmado')
	fechaPago = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha de pago')
		
	def __str__(self):
		return "%s" % (self.numeroControl)

	def rz(self):
		return "%s" % (self.razonsocial)

	class Meta:
		verbose_name = 'DTE de compra'
		verbose_name_plural = "DTE's de compras"
		ordering = ('-fecEmi',)	


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default='001')
	tipoEstablecimiento = models.ForeignKey(TipoEstablecimiento, on_delete=models.CASCADE, null=False, default='02', verbose_name='Tipo de establecimiento')
	codigoEstablecimiento = models.CharField(db_column='codigoEstablecimiento', max_length=4, blank=True, null=True, default='0000', verbose_name='Código de establecimiento')
	codigoPuntoVenta = models.CharField(db_column='codigoPuntoVenta', max_length=4, blank=True, null=True, default='0000', verbose_name='Código de punto de venta')
	

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Perfil'
		verbose_name_plural = 'Perfiles'


class DtesEmpresa(models.Model):
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Empresa')
	dte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, null=False, blank=False, verbose_name='Tipo de documento autorizado')

	def __str__(self):
		return '%s' % (self.dte)

	class Meta:
		verbose_name = 'Dte autorizado por empresa'
		verbose_name_plural = "Dte's autorizados por empresa"
		ordering = ('empresa',)

class TipoAccionUsuario(models.Model):
	nombre = models.CharField(max_length=50, blank=True, null=True, default='', verbose_name='Nombre')

	def __str__(self):
		return '%s' % (self.nombre)

	class Meta:
		ordering = ('id',)

class BitacoraAccionDte(models.Model):
	empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=False, blank=False, default='', verbose_name='Empresa')
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
	dte = models.CharField(max_length=36, null=True, blank=True, default='', verbose_name='´DTE')
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, blank=True, default='', verbose_name='Tipo DTE')
	fecha = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha')
	accion = models.ForeignKey(TipoAccionUsuario, on_delete=models.CASCADE, blank=True, default='', verbose_name='Acción')

	def __str__(self):
		return '%s - %s' % (self.usuario, self.dte)

class BitacoraAccionDteP(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
	dte = models.ForeignKey(DTEProveedor, on_delete=models.CASCADE, blank=True, default='', verbose_name='DTE')
	tipoDte = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, blank=True, default='', verbose_name='Tipo DTE')
	fecha = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False, verbose_name='Fecha')
	accion = models.ForeignKey(TipoAccionUsuario, on_delete=models.CASCADE, blank=True, default='', verbose_name='Acción')

	def __str__(self):
		return '%s - %s' % (self.usuario, self.dte)