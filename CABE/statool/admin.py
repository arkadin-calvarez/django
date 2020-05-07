# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import Device, Service
from django.contrib import admin

# Register your models here.
admin.site.register(Device)
admin.site.register(Service)