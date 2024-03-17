from django.contrib.auth.models import User
from .models import UserProfile

def user_empresa_context(request):
    empresa_value = None  # Valor por defecto si el campo no está configurado

    if request.user.is_authenticated:
        try:
            empresa_value = request.user.userprofile.empresa.nombreComercial
        except UserProfile.DoesNotExist:
            pass
    
    return {'empresa_value': empresa_value}

def username_context(request):
    username_value = None

    if request.user.is_authenticated:
        username_value = "%s %s" % (request.user.first_name, request.user.last_name)


    return {'username_value': username_value}

"""Ahora, puedes acceder al campo personalizado a través del perfil del usuario.
Por ejemplo, para obtener el campo custom_field del perfil de un usuario:
user = User.objects.get(username='username')
custom_field_value = user.userprofile.custom_field"""