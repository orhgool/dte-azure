import os, smtplib, requests
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import DTECliente, Empresa, Cliente, Configuracion, TipoDocumento

def enviarCorreo(request, tipo, codigo):
    config = Configuracion.objects.all().first()
    template = ''
    if tipo in {'01','03','05','06','11','14'}:
        template = 'dte:actualizar'
        tabla = get_object_or_404(DTECliente, codigoGeneracion=codigo)
        emisor = get_object_or_404(Empresa, codigo=request.session['empresa'])
        cliente = Cliente.objects.get(codigo=tabla.receptor_id)
        correo = cliente.correo
        sello = tabla.selloRecepcion
    elif tipo in {'07'}:
        pass
        #template = 'sitria:actualizar_dte_proveedor'
        #tabla = get_object_or_404(DTEProveedor, codigoGeneracion=codigo)
        #proveedor = Proveedor.objects.get(codigo=tabla.receptor_id)
        #correos = proveedor.correo
        #sello = tabla.selloRecepcion

    correo = 'alfaconsultores.sv@gmail.com'

    tablaTipo = TipoDocumento.objects.get(codigo=tipo)

    # Datos de conexión
    servidor_smtp = config.servidorSmtp
    puerto_smtp = config.puertoSmtp
    cuenta_correo = config.usuarioCorreo
    contraseña = config.claveCorreo

    # Destinatario y contenido del correo
    destinatario = correo
    asunto = f'{tabla.emisor.nombreComercial}, {tablaTipo.nombre_corto} cod.: {codigo}'
    datos = get_object_or_404(DTECliente, codigoGeneracion=codigo)
    empresa = get_object_or_404(Empresa, codigo=datos.emisor.codigo)
    logo = request.session['logo']
    enlace = f'https://admin.factura.gob.sv/consultaPublica?ambiente={empresa.ambiente.codigo}&codGen={datos.codigoGeneracion}&fechaEmi={datos.fecEmi.strftime("%Y-%m-%d")}'
    context={'datos':datos, 'logo':logo, 'enlace':enlace}
    cuerpo_html = render_to_string('plantillas/correo_receptor.html', context)

    # Configurar el correo
    mensaje = MIMEMultipart()
    mensaje['From'] = 'Facturación electrónica'
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo_html, 'html'))

    try:
        # Adjuntar archivo JSON
        json_filename = f'{codigo}.json'
        json_path = os.path.join(settings.STATIC_DIR, f'clientes/{tabla.emisor_id}/', json_filename)
        json_attachment = MIMEApplication(open(json_path, 'rb').read())
        json_attachment.add_header('Content-Disposition', 'attachment', filename=json_filename)
        mensaje.attach(json_attachment)

        # Adjuntar archivo PDF
        pdf_filename = f'{codigo}.pdf'
        pdf_path = os.path.join(settings.STATIC_DIR, f'clientes/{tabla.emisor_id}/', pdf_filename)
        pdf_attachment = MIMEApplication(open(pdf_path, 'rb').read())
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
        mensaje.attach(pdf_attachment)


        # Configurar la conexión con el servidor SMTP
        conexion_smtp = smtplib.SMTP(servidor_smtp, puerto_smtp)
        conexion_smtp.starttls()
        conexion_smtp.login(cuenta_correo, contraseña)

        # Enviar el correo
        conexion_smtp.sendmail(cuenta_correo, destinatario, mensaje.as_string())
        conexion_smtp.quit()

        mensaje_respuesta = 'Correo enviado'
        
    except Exception as e:
        mensaje_respuesta = f'Error al enviar el correo: {str(e)}'
        messages.info(request, mensaje_respuesta)

    return HttpResponse(mensaje_respuesta)