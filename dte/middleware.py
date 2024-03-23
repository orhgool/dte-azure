# middleware.py

from django.contrib import messages

class MessagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Aquí puedes agregar cualquier lógica necesaria para agregar mensajes
        messages.add_message(request, messages.INFO, 'Este es un mensaje de prueba')

        response = self.get_response(request)
        return response