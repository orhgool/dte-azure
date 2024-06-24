from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import *
from .forms import CustomUserChangeForm


class ActividadeconomicaAdmin(admin.ModelAdmin):
	search_fields = ['descripcion',]

class DtesEmpresaInline(admin.TabularInline):
	model = DtesEmpresa
	extra = 0

class EmpresaAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'razonsocial',)
	inlines = [DtesEmpresaInline]

class UserProfileAdmin(admin.StackedInline):
	model = UserProfile

class ControlDocumentoAdmin(admin.ModelAdmin):
	search_fields = ['empresa__razonsocial',]

class CustomUserAdmin(UserAdmin):
	form = CustomUserChangeForm
	inlines = (UserProfileAdmin,)

class DtesEmpresaAdmin(admin.ModelAdmin):
	search_fields = ['empresa',]
	list_display = ('empresa_razonsocial','dte')

	def empresa_razonsocial(self, obj):
		return obj.empresa.nombreComercial

class DteClienteAdmin(admin.ModelAdmin):
	search_fields = ['codigoGeneracion',]
	list_display = ('codigoGeneracion', 'numeroControl', 'emisor_razonsocial', 'formatted_fecEmi')

	def emisor_razonsocial(self, obj):
		return obj.emisor.razonsocial

	def formatted_fecEmi(self, obj):
		return obj.fecEmi.strftime('%d/%m/%Y')

class DteProveedorAdmin(admin.ModelAdmin):
	search_fields = ['codigoGeneracion',]
	list_display = ('codigoGeneracion', 'numeroControl', 'emisor_razonsocial')

	def emisor_razonsocial(self, obj):
		return obj.emisor.razonsocial

class DteContingenciaAdmin(admin.ModelAdmin):
	search_fields = ['codigoGeneracion',]
	list_display = ('codigoGeneracion', 'fTransmision', 'emisor_razonsocial')

	def emisor_razonsocial(self, obj):
		return obj.emisor.razonsocial

class TributoResumenAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre')

class TributoCuerpoAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre')	
		
class ImpuestoAdValoremAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre')

class ClienteAdmin(admin.ModelAdmin):
	search_fields = ['empresa__razonsocial', 'razonsocial', 'nombreComercial',]
	list_display = ('razonsocial', 'nombreComercial', 'empresa__razonsocial')

	def empresa__razonsocial(self, obj):
		return obj.empresa.razonsocial


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)

admin.site.register(Actividadeconomica, ActividadeconomicaAdmin)
admin.site.register(TipoAccionUsuario)
admin.site.register(BitacoraAccionDte)
admin.site.register(AmbienteDestino)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(CondicionOperacion)
admin.site.register(Configuracion)
admin.site.register(ControlDocumento, ControlDocumentoAdmin)
admin.site.register(Departamento)
admin.site.register(DTECliente, DteClienteAdmin)
admin.site.register(DTEContingencia, DteContingenciaAdmin)
admin.site.register(DTEProveedor, DteProveedorAdmin)
admin.site.register(DomicilioFiscal)
admin.site.register(DtesEmpresa, DtesEmpresaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(EstadoDTE)
admin.site.register(FormaPago)
admin.site.register(ImpuestoAdValorem, ImpuestoAdValoremAdmin)
admin.site.register(Incoterms)
admin.site.register(ModeloFacturacion)
admin.site.register(Moneda)
admin.site.register(Municipio)
admin.site.register(OtroDocumentoAsociado)
admin.site.register(Pais)
admin.site.register(Plazo)
admin.site.register(Proveedor)
admin.site.register(RecintoFiscal)
admin.site.register(Regimen)
admin.site.register(RetencionIVAMH)
admin.site.register(TipoContingencia)
admin.site.register(TipoContribuyente)
admin.site.register(TipoDocumentoContingencia)
admin.site.register(TipoDocumentoIdentificacion)
admin.site.register(TipoDocumento)
admin.site.register(TipoDonacion)
admin.site.register(TipoEstablecimiento)
admin.site.register(TipoGeneracionDocumento)
admin.site.register(TipoInvalidacion)
admin.site.register(TipoItem)
admin.site.register(TipoPersona)
admin.site.register(TipoServicioMedico)
admin.site.register(TipoTransmision)
admin.site.register(Transporte)
admin.site.register(TituloRemision)
admin.site.register(TributoCuerpo, TributoCuerpoAdmin)
admin.site.register(TributoResumen, TributoResumenAdmin)
admin.site.register(UnidadMedida)
admin.site.register(UrlSistema)