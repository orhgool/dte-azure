from django.urls import path
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static

from .views import *

app_name = 'dte'

handler404 = 'dte.views.custom_page_not_found'

urlpatterns = [
	path('', index, name='index'),
	path('lista_dte/<str:tipo>', lista_dte, name='lista_dte'),
    path('lista_dte_filtrar/<str:tipo>', lista_dte_filtrar, name='lista_dte_filtrar'),
	path('autenticar/', autenticar, name='autenticar'),
	path('loginMH/', loginMH, name='loginMH'),
	path('vista_previa/<str:tipo>/<str:codigo>/', vista_previa_pdf_dte, name='vista_previa'),
	path('vista_previa_correo/<str:tipo>/<str:codigo>/', vista_previa_correo, name='vista_previa_correo'),
	path('firmardte/<str:tipo>/<str:codigo>', firmarDte, name='firmardte'),
	path('enviar_mh/<str:tipo>/<str:codigo>', EnviarDTEView.as_view(), name='enviar_mh'),
	path('enviar_mh_anulacion/<str:tipo>/<str:cod_anulacion>', EnviarDTEView.as_view(), name='enviar_mh_anulacion'),
	path('enviar_mh_prueba/<str:tipo>/<str:codigo>/<str:doc>/', EnviarDTEView_prueba.as_view(), name='enviar_mh_prueba'),
	path('nuevo/<str:tipo>', DTECreate.as_view(), name='nuevo'),
	path('actualizar/<str:tipo>/<str:pk>', DTEUpdate.as_view(), name='actualizar'),
	path('eliminar/<str:tipo>/<str:pk>', eliminar_detalle, name='eliminar_detalle'),
	path('clientes/', lista_cliente, name='cliente_list'),
	path('proveedores/', lista_proveedor, name='proveedor_list'),
	path('productos/', lista_producto, name='lista_producto'),
	path('producto_nuevo/', producto, name='producto_nuevo'),
	path('producto/<str:pk>', producto, name='producto_detalle'),
    path('guardar_cliente_modal/', guardar_cliente_modal, name='guardar_cliente_modal'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<str:pk>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<str:pk>/eliminar/', cliente_delete, name='cliente_delete'),
    path('proveedores/nuevo/', proveedor_create, name='proveedor_create'),
    path('proveedores/<str:pk>/editar/', proveedor_update, name='proveedor_update'),
    path('proveedores/<str:pk>/eliminar/', proveedor_delete, name='proveedor_delete'),
    path('perfil_empresa/', perfil_empresa, name='perfil_empresa'),
    path('perfil_usuario/', perfil_usuario, name='perfil_usuario'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('autocompletar-producto/', autocompletar_producto, name='autocompletar_producto'),
    path('direcciones/', direcciones, name='direcciones'),
    path('cdn/', cdn, name='cdn'),
    path('ver_correo/<str:tipo>/<str:codigo>', verCorreo, name='verCorreo'),
    path('correo/<str:tipo>/<str:codigo>/<str:reenvio>', correoACliente, name='correo'),
    path('pruebas/', pruebas, name='prueba'),
    path('enviar_prueba/<str:tipo>', enviarPrueba, name='enviar_prueba'),
    path('invalidar_dte/<str:tipo>/<str:codigo>', invalidarDte, name='invalidarDte'),
    path('registro_de_cliente/<str:cod_empresa>', cliente_auto_registro, name='cliente_auto_registro'),
    path('<str:cod_empresa>/gracias', registro_de_cliente_gracias, name='registro_de_cliente_gracias'),
    path('bitacoraDte/<str:codigo>', bitacoraDte, name='bitacoraDte'),
    path('seleccionar_json/', seleccionar_json, name='seleccionar_json'),
    path('upload_json/', upload_json, name='upload_json'),
    path('guardar_json_data/', guardar_json_data, name='guardar_json_data'),
    path('exportDtes/', exportDtes, name='exportDtes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)