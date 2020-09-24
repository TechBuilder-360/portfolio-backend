"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_BASE = os.path.abspath(os.path.join(PROJECT_DIR, '..'))
APP_DIR = os.path.abspath(os.path.join(PROJECT_BASE, 'apps'))
sys.path.append(PROJECT_DIR)
sys.path.append(PROJECT_BASE)
sys.path.append(APP_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_wsgi_application()
