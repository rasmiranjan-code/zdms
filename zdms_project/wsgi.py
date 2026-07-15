# zdms_project/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zdms_project.settings.development')

application = get_wsgi_application()