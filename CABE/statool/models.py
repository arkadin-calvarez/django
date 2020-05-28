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

    # To show the DC device name instead "Object ID" in the /admin page
    def __str__(self) -> str:
        return self.name
    
    @property
    def napalm_driver(self) -> str:
        return NAPALM_MAPPING[self.platform]

    # Instance method used by Dynamic URLs to avoid static data
    def get_absolute_url(self):
        return f"devices/{self.name}"
    
    def get_absolute_url2(self):
        return f"{self.name}"


# Services DC
class Service(models.Model):
    name = models.CharField(max_length=100)
    devices = models.ForeignKey(Device, null=True, blank=True, on_delete= models.SET_NULL)

    # To show the DC device name instead "Object ID" in the /admin page
    def __str__(self) -> str:
        return self.name


# Show command
class Command(models.Model):
    name = models.CharField(max_length=100)
    command = models.CharField(max_length=100)
    platform = models.CharField(
        max_length=30, default='Firewall',
        choices=(('cisco', 'ios'), ('juniper', 'junos'))
    )
    # To show the DC device name instead "Object ID" in the /admin page
    def __str__(self) -> str:
        return self.name

    # Instance method used by Dynamic URLs to avoid static data
    def get_absolute_command(self):
        return f"commands/{self.id}"