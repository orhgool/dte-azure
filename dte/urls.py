from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

app_name = 'dte'

urlpatterns = [
	path('', index, name='index'),
	path('lista_dte/<str:tipo>', lista_dte, name='lista_dte'),
	path('autenticar/', autenticar, name='autenticar'),
	path('loginMH/', loginMH, name='loginMH'),
	path('vista_previa/<str:tipo>/<str:codigo>/', vista_previa_pdf_dte, name='vista_previa'),
	path('firmardte/<str:tipo>/<str:codigo>', firmarDte, name='firmardte'),
	path('enviar_mh/<str:tipo>/<str:codigo>', EnviarDTEView.as_view(), name='enviar_mh'),
	path('nuevo/<str:pk>', DTECreate.as_view(), name='nuevo'),
	path('actualizar/<str:pk>', DTEUpdate.as_view(), name='actualizar'),
	path('eliminar/<str:pk>', eliminar_detalle, name='eliminar_detalle'),
	path('clientes/', lista_cliente, name='cliente_list'),
	path('productos/', lista_producto, name='lista_producto'),
	path('producto_nuevo/', producto, name='producto_nuevo'),
	path('producto/<str:pk>', producto, name='producto_detalle'),
    path('guardar_cliente_modal/', guardar_cliente_modal, name='guardar_cliente_modal'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<str:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<str:pk>/eliminar/', cliente_delete, name='cliente_delete'),
    path('perfil_empresa/', perfil_empresa, name='perfil_empresa'),
    path('perfil_usuario/', perfil_usuario, name='perfil_usuario'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('autocompletar-producto/', autocompletar_producto, name='autocompletar_producto'),
    path('direcciones/', direcciones, name='direcciones'),
    path('cdn/', cdn, name='cdn'),
    path('correo/<str:tipo>/<str:codigo>', correoACliente, name='correo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)