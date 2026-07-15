# zdms_project/asgi.py

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zdms_project.settings.development')

application = get_asgi_application()