import requests
from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory, ModelForm
from .models import (UserProfile, DTECliente, DTEClienteDetalle, DTEProveedor, DTEProveedorDetalle, 
	Cliente, Proveedor, Empresa, Producto, TipoDocumento, DTEContingencia, DTEContingenciaDetalle)
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

class DTEClienteForm(forms.ModelForm):
	def __init__(self, *args, request=None, empresa=None, tipo=None, **kwargs):
		super(DTEClienteForm, self).__init__(*args, **kwargs)

		self.fields['estadoPago'].label = '. Pagado'

		if empresa:
			self.fields['receptor'].queryset = Cliente.objects.filter(empresa_id=empresa)

	class Meta:
		model = DTECliente
		fields = ('emisor', 'codigoGeneracion', 'numeroControl','receptor', 'tipoDte', 'fecEmi', 'version', 'reteRenta',
			'observaciones','condicionOperacion', 'estadoPago', 'tipoItemExpor','recintoFiscal','regimen','incoterms')
		widgets = {
			'emisor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'codigoGeneracion': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'numeroControl': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'ambiente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'receptor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'tipoDte': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'condicionOperacion': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'version': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'fecEmi': forms.DateTimeInput(attrs={'class': 'datepicker','style': 'font-weight: bold;'}),
			'observaciones': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;', 'rows':'3'}),
			'estadoPago': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'font-weight: bold; padding: 3px;'}),
			'reteRenta': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; padding: 3px;','type': 'number', 'step':'any'}),
			'tipoItemExpor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'recintoFiscal': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'regimen': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'incoterms': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
		}
			

class DTEProveedorForm(forms.ModelForm):
	def __init__(self, *args, request=None, empresa=None, tipo=None, **kwargs):
		super(DTEProveedorForm, self).__init__(*args, **kwargs)

		self.fields['estadoPago'].label = '.  Pagado'

		if empresa:
			self.fields['receptor'].queryset = Proveedor.objects.filter(empresa_id=empresa)

	class Meta:
		model = DTEProveedor
		fields = ('emisor', 'codigoGeneracion', 'numeroControl','receptor', 'tipoDte', 'version', 'fecEmi', 'version',
			'observaciones','condicionOperacion', 'estadoPago')
		widgets = {
			'emisor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'codigoGeneracion': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'numeroControl': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'ambiente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'receptor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'tipoDte': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'condicionOperacion': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
			'version': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'fecEmi': forms.DateTimeInput(attrs={'class': 'datepicker','style': 'font-weight: bold;'}),
			'observaciones': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;', 'rows':'3'}),
			'estadoPago': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'font-weight: bold; padding: 3px;'}),
		}

class FCCFDetalleForm(forms.ModelForm):
	
	class Meta:
		model = DTEClienteDetalle
		fields = ('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'complemento1', 'precioUni', 'montoDescu', 'ventaNoSuj', 
			'ventaExenta', 'ventaGravada')
		widgets = {
			'codigoDetalle': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center; width: 50px; padding: 3px;', 'readonly':'True'}),
			'tipoItem': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 100px; padding: 3px;'}),
			'cantidad': forms.TextInput(attrs={'class': 'form-control cantidad','style': 'font-weight: bold; width: 80px; padding: 3px;','type': 'number','step':'any', 'oninput':'calcularTotal(this)'}),
			'uniMedida': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'complemento1': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'precioUni': forms.TextInput(attrs={'class': 'form-control precioUni','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any', 'oninput':'calcularTotal(this)'}),
			'montoDescu': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 70px; padding: 3px;','type': 'number', 'step':'any'}),
			'ventaNoSuj': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
			'ventaExenta': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
			'ventaGravada': forms.TextInput(attrs={'class': 'form-control ventaGravada','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
		}


class NCDDetalleForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(NCDDetalleForm, self).__init__(*args, **kwargs)
		self.fields['tipoDoc'].queryset = TipoDocumento.objects.filter(codigo__in=['01','03'])

	class Meta:
		model = DTEClienteDetalle
		fields = ('codigoDetalle', 'tipoItem', 'tipoDoc', 'tipoGeneracion', 'numeroDocumento', 
		'fechaEmision', 'cantidad', 'uniMedida', 'descripcion', 'complemento1',	'precioUni', 'montoDescu', 
		'ventaNoSuj', 'ventaExenta', 'ventaGravada')
		widgets = {
			'codigoDetalle': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center; width: 50px; padding: 3px;', 'readonly':'True'}),
			'tipoItem': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'tipoDoc': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'tipoGeneracion': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'numeroDocumento': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;'}),
			'fechaEmision': forms.DateTimeInput(attrs={'class': 'datepicker','style': 'font-weight: bold;'}),
			'cantidad': forms.TextInput(attrs={'class': 'form-control cantidad','style': 'font-weight: bold; width: 80px; padding: 3px;','type': 'number','step':'any', 'oninput':'calcularTotal(this)'}),
			'uniMedida': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'complemento1': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'precioUni': forms.TextInput(attrs={'class': 'form-control precioUni','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any', 'oninput':'calcularTotal(this)'}),
			'montoDescu': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 70px; padding: 3px;','type': 'number', 'step':'any'}),
			'ventaNoSuj': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
			'ventaExenta': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
			'ventaGravada': forms.TextInput(attrs={'class': 'form-control ventaGravada','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
		}


class FEXDetalleForm(forms.ModelForm):
	
	class Meta:
		model = DTEClienteDetalle
		fields = ('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'complemento1', 'precioUni', 'montoDescu', 'noGravado', 'ventaGravada')
		widgets = {
			'codigoDetalle': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center; width: 50px; padding: 3px;', 'readonly':'True'}),
			'tipoItem': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'cantidad': forms.TextInput(attrs={'class': 'form-control cantidad','style': 'font-weight: bold; width: 80px; padding: 3px;','type': 'number','step':'any', 'oninput':'calcularTotal(this)'}),
			'uniMedida': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'complemento1': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'precioUni': forms.TextInput(attrs={'class': 'form-control precioUni','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any', 'oninput':'calcularTotal(this)'}),
			'montoDescu': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 70px; padding: 3px;','type': 'number', 'step':'any'}),
			'noGravado': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
			'ventaGravada': forms.TextInput(attrs={'class': 'form-control ventaGravada','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
		}



class FSEDetalleForm(forms.ModelForm):
	
	class Meta:
		model = DTEProveedorDetalle
		fields = ('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'complemento1', 'precioUni', 'montoDescu', 'compra')
		widgets = {
			'codigoDetalle': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center; width: 50px; padding: 3px;', 'readonly':'True'}),
			'tipoItem': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'cantidad': forms.TextInput(attrs={'class': 'form-control cantidad','style': 'font-weight: bold; width: 80px; padding: 3px;','type': 'number','step':'any', 'oninput':'calcularTotal(this)'}),
			'uniMedida': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 150px; padding: 3px;'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'complemento1': forms.Textarea(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;', 'rows':'3'}),
			'precioUni': forms.TextInput(attrs={'class': 'form-control precioUni','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any', 'oninput':'calcularTotal(this)'}),
			'montoDescu': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; text-align: right; width: 70px; padding: 3px;','type': 'number', 'step':'any'}),
			'compra': forms.TextInput(attrs={'class': 'form-control ventaGravada','style': 'font-weight: bold; text-align: right; width: 100px; padding: 3px;','type': 'number', 'step':'any'}),
		}


FCCFDetalleFormSet = inlineformset_factory(
	DTECliente,	DTEClienteDetalle, form=FCCFDetalleForm,
	fields=('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'complemento1', 'precioUni', 'montoDescu', 'ventaNoSuj', 
			'ventaExenta', 'ventaGravada'
			), extra=0, can_delete=False, can_delete_extra=True
)

NCDDetalleFormSet = inlineformset_factory(
	DTECliente,	DTEClienteDetalle, form=NCDDetalleForm,
	fields=('tipoItem', 'tipoDoc', 'tipoGeneracion', 'numeroDocumento', 'fechaEmision', 'cantidad', 
		'uniMedida', 'descripcion', 'complemento1',	'precioUni', 'montoDescu', 'ventaNoSuj', 'ventaExenta', 'ventaGravada'
			), extra=0, can_delete=False, can_delete_extra=True
)

FEXDetalleFormSet = inlineformset_factory(
	DTECliente,	DTEClienteDetalle, form=FEXDetalleForm,
	fields=('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'complemento1', 'precioUni', 'montoDescu', 'noGravado', 'ventaGravada'
			), extra=0, can_delete=False, can_delete_extra=True
)


FSEDetalleFormSet = inlineformset_factory(
	DTEProveedor,	DTEProveedorDetalle, form=FSEDetalleForm,
	fields=('tipoItem', 'cantidad', 'uniMedida', 'descripcion', 'complemento1', 'precioUni', 'montoDescu', 'compra'
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
			'telefono', 'correo', 'actividadEconomica','pais','departamento','municipio','direccionComplemento',
			'tipoContribuyente','tipoPersona', 'diasCredito')
		widgets = {
			'codigo': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center', 'readonly':'True'}),
			'razonsocial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nombreComercial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'tipoDocumentoCliente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'numeroDocumento': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nrc': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'correo': forms.EmailInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'correo2': forms.EmailInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'correo3': forms.EmailInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'empresa': forms.HiddenInput(),
			'actividadEconomica': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'pais': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'departamento': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'municipio': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'direccionComplemento': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'tipoContribuyente': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'tipoPersona': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
			'agenteRetencion': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'font-weight: bold; padding: 3px;'}),
			'diasCredito': forms.TextInput(attrs={'class': 'form-control cantidad','style': 'font-weight: bold; width: 80px; padding: 3px;','type': 'number','step':'1'}),
		}


class ProveedorForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		initial_values = kwargs.get('initial', {})
		initial_values['valor_del_campo'] = 'prueba'
		kwargs['initial'] = initial_values
		super().__init__(*args, **kwargs)

	class Meta:
		model = Proveedor
		fields = ('codigo','razonsocial','nombreComercial','tipoDocumentoProveedor','numeroDocumento', 'nrc',
			'telefono', 'correo','actividadEconomica','pais','departamento','municipio','direccionComplemento',
			'tipoContribuyente','tipoPersona')
		widgets = {
			'codigo': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center', 'readonly':'True'}),
			'razonsocial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'nombreComercial': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; align: center'}),
			'tipoDocumentoProveedor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold'}),
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


class DTEContingenciaForm(forms.ModelForm):
	def __init__(self, *args, request=None, empresa=None, tipo=None, **kwargs):
		super(DTEContingenciaForm, self).__init__(*args, **kwargs)
		if empresa:
			pass

	class Meta:
		model = DTEContingencia
		fields = ('emisor', 'codigoGeneracion', 'tipoDte', 'version', 'fTransmision', 'tipoContingencia',
			'fInicio','fFinal')
		widgets = {
			#'emisor': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'codigoGeneracion': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'version': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;','readonly': 'True'}),
			'fTransmision': forms.DateTimeInput(attrs={'class': 'datepicker','style': 'font-weight: bold;'}),
			'fInicio': forms.DateTimeInput(attrs={'class': 'datepicker','style': 'font-weight: bold;'}),
			'fFinal': forms.DateTimeInput(attrs={'class': 'datepicker','style': 'font-weight: bold;'}),
			'tipoContingencia': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
		}
			

class ContingenciaDetalleForm(forms.ModelForm):	
	class Meta:
		model = DTEContingenciaDetalle
		fields = ('tipoDte', 'codigoGeneracionDTE')
		widgets = {
			'tipoDte': forms.Select(attrs={'class': 'form-control','style': 'font-weight: bold; width: 250px; padding: 3px;'}),
			'codigoGeneracionDTE': forms.TextInput(attrs={'class': 'form-control','style': 'font-weight: bold; padding: 3px;'}),
		}


ContingenciaDetalleFormSet = inlineformset_factory(
	DTEContingencia, DTEContingenciaDetalle, form=ContingenciaDetalleForm,
	fields=('tipoDte', 'codigoGeneracionDTE'
			), extra=0, can_delete=False, can_delete_extra=True
)