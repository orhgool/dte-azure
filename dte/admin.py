from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import *
from .forms import CustomUserChangeForm


class DtesEmpresaInline(admin.TabularInline):
	model = DtesEmpresa
	extra = 0

class EmpresaAdmin(admin.ModelAdmin):
	inlines = [DtesEmpresaInline]

class UserProfileAdmin(admin.StackedInline):
	model = UserProfile

class CustomUserAdmin(UserAdmin):
	form = CustomUserChangeForm
	inlines = (UserProfileAdmin,)

class TributoResumenAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre')

class TributoCuerpoAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre')	
		
class ImpuestoAdValoremAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre')	


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomUserAdmin)

admin.site.register(AmbienteDestino)
admin.site.register(Cliente)
admin.site.register(CondicionOperacion)
admin.site.register(ConfigSeg)
admin.site.register(ControlDocumento)
admin.site.register(Departamento)
admin.site.register(DomicilioFiscal)
admin.site.register(DtesEmpresa)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(EstadoDTE)
admin.site.register(FormaPago)
admin.site.register(ImpuestoAdValorem, ImpuestoAdValoremAdmin)
admin.site.register(Incoterm)
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