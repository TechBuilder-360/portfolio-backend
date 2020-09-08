"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

filedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(filedir, 'apps'))
sys.path.append(os.path.join(filedir, 'portfolio'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_wsgi_application()
