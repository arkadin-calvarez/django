# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .models import Device, Service, Command
from napalm import get_network_driver
from django.contrib.auth.decorators import login_required
import requests
from subprocess import run, PIPE
from django.urls import reverse
from salt import client
import salt.client
import subprocess
import os
import yaml 
import io

# Page, with login to allow access the main/home page.
# when browsing to http://rasp:7777 URL
@login_required(login_url='/accounts/login/')
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html')


# Below is a redirectly to Statool APP http://cabe:7878/base
# in below example, some "context" can be given to be used with the template,
# allowing easy customization of messages in one page
# (remember the static blog posts from the video)
#@login_required(login_url='/accounts/login/')
def statool(request: HttpRequest) -> HttpResponse:
    devices = Device.objects.all()
    services = Service.objects.all()
    context = {
        'title' : 'Panaceia Statool',
        'owner' : 'Cabe',
        'devices' : devices,    #This is directly used in base.html (in FOR loops) to call/print devices
        'services' : services
    }
    return render(request, 'statool.html', context)

# Below scripts redirect us to the "scripts.html" and "saltindex" webpage
# when browsing to http://cabe:7878/scripts or http://cabe:7878/saltindex URL
# ============
# Display and redirecto to Webpage
def scripts(request: HttpRequest) -> HttpResponse:
    return render(request, 'scripts.html')

def salt(request: HttpRequest) -> HttpResponse:
    commands = Command.objects.all()
    devices = Device.objects.all()
    context = {
        'commands' : commands,
        'devices' : devices
    }
    return render(request, 'salt.html', context)

def saltapipage(request: HttpRequest) -> HttpResponse:
    return render(request, 'saltapipage.html')

# Runs the script itself, getting the information from the website
# and display it locally (scripts.html)
#def output(request):
#    data=requests.get("https://xkcd.com/1906/")
#    print(data.text)
#    data=data.text
#    return render(request, 'scripts.html' , {'data':data})


# Runs the script itself, getting the information from the website
# and display content in another HTML (output.html)
#def another(request):
#    info=requests.get("https://xkcd.com/1906/")
#    print(info.text)
#    info=info.text
#    return render(request, 'output.html' , {'data':info})


# Dropdown menu. After select the device, will redirect to the device.html
def run_script_ondevice(self):
#    results=Device.objects.all()
    return render(request, 'device.html',{'Device':results})

# Function to use NAPALM "Get facts" from devices.
# In this case, "get_interfaces" and "get_interfaces_ip" facts
def get_device_stats(request: HttpRequest, device_id) -> HttpResponse:
    device = Device.objects.get(pk=device_id)
    driver = get_network_driver(device.napalm_driver)
    with driver(device.host, device.username, device.password) as device_conn:
        interfaces = device_conn.get_interfaces()
        ipaddress = device_conn.get_interfaces_ip()
    context = {
        'device':device,
        'interfaces':interfaces,
        'ipaddress':ipaddress,
    }
    print(interfaces)
    print(ipaddress)
#    You can enable this when you want to see the debug on the terminal and read fields
    return render(request, 'device.html', context)
 
# SALT output page, when user click on "SALT Script" button, defined in scripts.html page.
# Remember that stdout and stderr w/ PIPE (imported) in Python3 the ways to allout the output 
# of the terminal output we want to see. "capture_output=True" was an old argument to allow 
# that in previous Python versions
def saltout(request):
    data = subprocess.run("sudo salt 'vsrx1' net.cli 'show bgp summary'", stdout=PIPE, stderr=PIPE, shell=True)
    return render(request, 'saltout.html' , {'data':data.stdout})
#    with open('saltout.txt', 'w') as saltout:
#        data = subprocess.run("sudo salt 'vsrx1' net.cli 'show bgp summary'", stdout=saltout, stderr=PIPE, shell=True)
#    with open("/home/outright/Django/CABE/saltout.txt") as out:
#        list = yaml.load(out, Loader=yaml.FullLoader)
#        return render(request, 'salt.html' , {'list':list})
#
#    data = (subprocess.Popen("sudo salt 'vsrx1' net.cli 'show bgp summary'", stdout=subprocess.PIPE, shell=True, universal_newlines=True).communicate()[0])
#    return render(request, 'salt.html' , {'data':data})

# Above, stdout is displays content in bites (that's the reason of the unsorted format). 
# We need to transform this to string. One method is decode() (Ex: return render(request, 
# 'salt.html' , {'data':data.stdout.decode()}))  Decode method worked partially, because 
# it removed the /n and /b letters from my text, but all output text remains in one long line



# Using the below def, it allows to get a minion host name entered by a user and 
# using subprocess module query the BGP summary of a JUNOS device using that value.
# "searchbox" is the name of the HTML form name, which is then stored in the "minion"
# variable to be used later as part of the SALTSTACK CLI command.
def showfrombox(request):
    minion = request.GET.get('searchbox')
    arguments = ['sudo', 'salt', minion, 'net.cli', "'show bgp summary'"]
#    with open('saltout.txt', 'w') as saltout:
    data = subprocess.run(arguments, stdout=PIPE, stderr=PIPE, timeout=15)
    context = {
    'data':data,
    }
    return render(request, 'showfrombox.html', context)
#    return render(request, 'bgp.html' , {'data':data.args})


# Entering minion name and executing static command
#def show_bgp_fromfile(request):
#    minion = request.GET.get('searchboxfile')
#    commands = ['sudo', 'salt', minion, 'net.cli', "'show bgp summary'"]
#    with open('saltout.txt', 'w') as saltout:
#        data = subprocess.run(commands, stdout=saltout, stderr=saltout, timeout=15)
#    f = open('//home//outright//Django//CABE//saltout.txt', 'r')
#    file_content = f.read()
#    f.close()
#    return HttpResponse(file_content, content_type="text/plain")
#    return render(request, 'bgp1.html', {'data':data.args})


# Entering minion name and selecting command from dropdown
def showfromdrop(request):
    minion = request.GET.get('device_id')
    command = request.GET.get('command_id')
#    show = request.GET.get('command_id')
    commands = ['sudo', 'salt', minion, 'net.cli', command]
    with open('saltout.txt', 'w') as saltout:
        data = subprocess.run(commands, stdout=saltout, stderr=saltout, timeout=15)
    f = open('//home//outright//Django//CABE//saltout.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")


# Using SALT API (Local.Client()), to get dictionary of information.
def saltapi(request):
    local = client.LocalClient()
    salida = local.cmd('vsrx1', 'net.cli', ['show version'], username='saltapi', password='saltapi', eauth='pam')
    context = {
    'salida':salida,
    }   
    return render(request, 'saltapipage.html', context)