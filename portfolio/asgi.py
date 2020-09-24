"""
ASGI config for portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os, sys

from django.core.asgi import get_asgi_application

filedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(filedir, 'apps'))
sys.path.append(os.path.join(filedir, 'portfolio'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_asgi_application()
