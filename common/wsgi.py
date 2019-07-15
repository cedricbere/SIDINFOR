#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
WSGI config for sidinfor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "common.settings"

application = get_wsgi_application()
