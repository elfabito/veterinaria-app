import os
from django.core.wsgi import get_wsgi_application

# Establecer la configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "veterinaria.settings")

# Define el app para Vercel
app = get_wsgi_application()
