# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
#from django.contrib.auth.models import Device

NAPALM_MAPPING = {
    'cisco': 'ios',
    'juniper':'junos',
}

# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=70, default='000000')
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=70)
    device_type = models.CharField(
        max_length=30, default='000000',
        choices=(('router', 'Router'), ('switch', 'Switch'), ('firewall', 'Firewall'))
    )
    platform = models.CharField(
        max_length=30, default='Firewall',
        choices=(('cisco', 'ios'), ('juniper', 'junos'))
    )

    def __str__(self) -> str:
        return self.name
    
    @property
    def napalm_driver(self) -> str:
        return NAPALM_MAPPING[self.platform]

# Services DC
class Service(models.Model):
    name = models.CharField(max_length=100)
    devices = models.ForeignKey(Device, null=True, blank=True, on_delete= models.SET_NULL)

    def __str__(self) -> str:
        return self.name