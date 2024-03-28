import os, json, requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

def subir():
    # Define la cadena de conexión a tu cuenta de Azure Storage
    connect_str = "DefaultEndpointsProtocol=https;AccountName=almacendte;AccountKey=aoLLUo/S/fVFCTAwzVfroFTHaGUQDC4XwGCU19WIxu6ns/hLmJBLzkkoZPhYcYNSrShEaTHLKlAu+AStJOP26w==;EndpointSuffix=core.windows.net"

    # Crea el cliente del servicio de blobs
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Nombre del contenedor donde deseas guardar el archivo
    container_name = "clientes"

    # Nombre del archivo que deseas guardar
    file_name = "799B7357-74F8-4D43-B097-F0DD9A1C8489.png"
    empresa = 'A4BCBC83-4C59-4A3F-9C25-807D83AD0837'

    # Ruta local al archivo JSON que deseas cargar
    local_file_path = os.path.join(settings.STATIC_DIR,'clientes', empresa, file_name)

    # Crea un contenedor si no existe
    container_client = blob_service_client.get_container_client(container_name)
    #container_client.create_container()

    # Sube el archivo JSON al contenedor
    with open(local_file_path, "rb") as data:
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        blob_client.upload_blob(data, overwrite=True)

    blob_url = blob_client.url
    messages.info(requests, blob_url)

    #return JsonResponse({'respuesta': f'Archivo JSON cargado con éxito en Azure Blob Storage en el contenedor {container_name} como {file_name}'})
    return JsonResponse({'respuesta': f'Imagen PNG cargada con éxito en Azure Blob Storage. URL: {blob_url}'})
    #return HttpResponse('URL: ' + blob_url)