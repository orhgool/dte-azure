import os, json, requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

def subirArchivo(empresa, archivo):
    # Define la cadena de conexión a tu cuenta de Azure Storage
    connect_str = "DefaultEndpointsProtocol=https;AccountName=almacendte;AccountKey=aoLLUo/S/fVFCTAwzVfroFTHaGUQDC4XwGCU19WIxu6ns/hLmJBLzkkoZPhYcYNSrShEaTHLKlAu+AStJOP26w==;EndpointSuffix=core.windows.net"

    # Crea el cliente del servicio de blobs
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Nombre del contenedor donde deseas guardar el archivo
    contenedor = "empresas"

    # Ruta dentro del contenedor donde deseas guardar el archivo (carpeta 'codigo_empresa')
    blob_path = f"{empresa}/{archivo}"
    
    # Ruta local al archivo JSON que deseas cargar
    local_file_path = os.path.join(settings.STATIC_DIR,'clientes', empresa, archivo)

    # Crea un contenedor si no existe
    container_client = blob_service_client.get_container_client(contenedor)
    #container_client.create_container()  ## No crear el contenedor

    # Sube el archivo JSON al contenedor
    with open(local_file_path, "rb") as data:
        blob_client = blob_service_client.get_blob_client(container=contenedor, blob=blob_path)
        blob_client.upload_blob(data, overwrite=True)

    blob_url = blob_client.url
    #messages.info(requests, blob_url)

    #return JsonResponse({'respuesta': f'Archivo JSON cargado con éxito en Azure Blob Storage en el contenedor {contenedor} como {nombre_archivo}'})
    return JsonResponse({'respuesta': f'Archivo cargado con éxito en Azure Blob Storage. URL: {blob_url}'})
    #return HttpResponse('URL: ' + blob_url)