from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import user_login

app_name = 'manager'

urlpatterns = [
    path('', user_login, name='login')
]