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
from .models import DTECliente, Empresa, Cliente

def enviar_correo(request, tipo, codigo, destino):
    template = ''
    if tipo in {'01','03','05'}:
        template = 'dte:actualizar'
        tabla = get_object_or_404(DTECliente, codigoGeneracion=codigo)
        emisor = get_object_or_404(Empresa, codigoGeneracion=codigo)
        cliente = Cliente.objects.get(codigo=tabla.receptor_id)
        correos = [cliente_email.email for cliente_email in ClienteEmail.objects.filter(cliente=cliente)]
        sello = tabla.selloRecepcion
    elif tipo in {'07'}:
        pass
        #template = 'sitria:actualizar_dte_proveedor'
        #tabla = get_object_or_404(DTEProveedor, codigoGeneracion=codigo)
        #proveedor = Proveedor.objects.get(codigo=tabla.receptor_id)
        #correos = proveedor.correo
        #sello = tabla.selloRecepcion

    correos = ['alfaconsultores.sv@gmail.com',]

    tabTipo = TipoDocumento.objects.get(codigo=tipo)

    # Datos de conexión
    servidor_smtp = 'smtp-mail.outlook.com'
    puerto_smtp = 587
    cuenta_correo = 'facturacion.electronica.sv'
    contraseña = 'Ammh0909$'

    # Destinatario y contenido del correo
    destinatario = ', '.join(correos) #'alfaconsultores.sv@gmail.com'
    asunto = f'{tabTipo} cod.: {codigo}'
    context = {'codigo':codigo, 'tipoDocumento':tabTipo.nombre, 'numeroControl': tabla.numeroControl, 'selloRecepcion': tabla.selloRecepcion, 'fecEmi': tabla.fecEmi.strftime("%Y-%m-%d"), 'fecha': tabla.fecEmi.strftime("%d-%m-%Y")}
    cuerpo_html = render_to_string('sitria/correo.html', context)

    # Configurar el correo
    mensaje = MIMEMultipart()
    mensaje['From'] = 'ALCASA'
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo_html, 'html'))

    # Adjuntar archivo JSON
    json_filename = f'{codigo}.json'
    json_path = os.path.join(settings.STATIC_DIR, 'json/', json_filename)
    json_attachment = MIMEApplication(open(json_path, 'rb').read())
    json_attachment.add_header('Content-Disposition', 'attachment', filename=json_filename)
    mensaje.attach(json_attachment)

    # Adjuntar archivo PDF
    pdf_filename = f'{codigo}.pdf'
    pdf_path = os.path.join(settings.STATIC_DIR, 'pdf/', pdf_filename)
    pdf_attachment = MIMEApplication(open(pdf_path, 'rb').read())
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
    mensaje.attach(pdf_attachment)

    try:
        # Configurar la conexión con el servidor SMTP
        conexion_smtp = smtplib.SMTP(servidor_smtp, puerto_smtp)
        conexion_smtp.starttls()
        conexion_smtp.login(cuenta_correo, contraseña)

        # Enviar el correo
        conexion_smtp.sendmail(cuenta_correo, destinatario, mensaje.as_string())
        conexion_smtp.quit()

        mensaje_respuesta = 'Correo enviado con éxito.'
        
    except Exception as e:
        mensaje_respuesta = f'Error al enviar el correo: {str(e)}'

    return HttpResponse(mensaje_respuesta)