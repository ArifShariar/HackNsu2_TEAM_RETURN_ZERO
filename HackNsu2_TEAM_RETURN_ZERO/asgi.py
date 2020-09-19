"""
ASGI config for HackNsu2_TEAM_RETURN_ZERO project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackNsu2_TEAM_RETURN_ZERO.settings')

application = get_asgi_application()
