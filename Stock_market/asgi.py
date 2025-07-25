"""
ASGI config for Stock_market project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from whitenoise import ASGIStaticFilesWrapper
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Stock_market.settings')

application = get_asgi_application()
# application = ASGIStaticFilesWrapper(application)