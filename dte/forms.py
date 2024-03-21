from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import UserProfile, DTECliente, DTEClienteDetalle, Cliente, Empresa, Producto
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .funciones import CodGeneracion

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'

    empresa = forms.CharField(max_length=100, required=False)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']

class DTEForm(forms.ModelForm):

	class Meta:
		model = DTECliente
		fields = ('emisor', 'codigoGeneracion', 'numeroControl', 'receptor', 'tipoDte', 'fecEmi', 'estadoPago')
		widgets = {
			'emisor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'codigoGeneracion': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'numeroControl': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'receptor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'tipoDte': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'fecEmi': forms.DateTimeInput(attrs={'class': 'datepicker','style': 'font-weight: bold;'}),
			'estadoPago': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'font-weight: bold; padding: 3px;'}),
		}


class DTEDetalleForm(forms.ModelForm):
	
	class Meta:
		model = DTEClienteDetalle
		fields = ('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'precioUni', 'montoDescu', 'ventaNoSuj', 
			'ventaExenta', 'ventaGravada')
		widgets = {
			'codigoDetalle': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center; width: 50px; padding: 3px;', 'readonly':'True'}),
			'tipoItem': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'cantidad': forms.NumberInput(attrs={'class': 'form-control','style': 'font-weight: bold; width: 80px; padding: 3px;','step':'1'}),
			'uniMedida': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'descripcion': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;'}),
			'precioUni': forms.NumberInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','step':'1.00'}),
			'montoDescu': forms.NumberInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 70px; padding: 3px;','step':'1'}),
			'ventaNoSuj': forms.NumberInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','step':'1'}),
			'ventaExenta': forms.NumberInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','step':'1'}),
			'ventaGravada': forms.NumberInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','step':'1'}),
		}

DTEClienteDetalleFormSet = inlineformset_factory(
	DTECliente,	DTEClienteDetalle, form=DTEDetalleForm,
	fields=('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'precioUni', 'montoDescu', 'ventaNoSuj', 
			'ventaExenta', 'ventaGravada'
			), extra=0, can_delete=False, can_delete_extra=True
)


class ClienteForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		initial_values = kwargs.get('initial', {})
		initial_values['valor_del_campo'] = 'prueba'
		kwargs['initial'] = initial_values
		super().__init__(*args, **kwargs)

	class Meta:
		model = Cliente
		fields = ('codigo','razonsocial','nombreComercial','tipoDocumentoCliente','numeroDocumento', 'nrc',
			'telefono', 'correo','actividadEconomica','pais','departamento','municipio','direccionComplemento',
			'tipoContribuyente','tipoPersona')
		widgets = {
			'codigo': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center', 'readonly':'True'}),
			'razonsocial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nombreComercial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'tipoDocumentoCliente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'numeroDocumento': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nrc': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'correo': forms.EmailInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'empresa': forms.HiddenInput(),
			'actividadEconomica': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'pais': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'departamento': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'municipio': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'direccionComplemento': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'tipoContribuyente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'tipoPersona': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
		}


class ProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = ('codigo','nombre','precio','existencia','unidadMedida','cantidadMinima')
		widgets = {
			'codigo': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center', 'readonly':'True'}),
			'nombre': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'precio': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right;', 'type': 'number', 'step':'any'}),
			'existencia': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right;', 'type': 'number', 'step':'any'}),
			'unidadMedida': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'cantidadMinima': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right;', 'type': 'number', 'step':'any'}),
		}

class EmpresaPerfilForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['codigoEstablecimiento'].help_text = 'Si no tiene código de establecimiento debe colocar "0000"'
		self.fields['codigoPuntoVenta'].help_text = 'Si no tiene código de punto de venta debe colocar "0000"'

	class Meta:
		model = Empresa
		fields = '__all__'
		widgets = {
			'codigo': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center', 'readonly':'True'}),
			'razonsocial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nombreComercial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nit': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nrc': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'dui': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'correo': forms.EmailInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'actividadEconomica': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'pais': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'departamento': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'municipio': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'direccionComplemento': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'ambiente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'tipoContribuyente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'tipoPersona': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'tipoEstablecimiento': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'codigoEstablecimiento': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'codigoPuntoVenta': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'usuarioMH': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'passwordAPI': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'passwordPri': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'token': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; align: center', 'readonly':'True'}),
		}