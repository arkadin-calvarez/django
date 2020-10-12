# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import Device, Service, Command
from napalm import get_network_driver
from django.contrib.auth.decorators import login_required
import requests

from subprocess import run, PIPE
from django.urls import reverse

import logging
import subprocess
import os
import yaml 
import sys
import io
import json
import re
import string

############################ WEBPAGES START ############################

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

# Salt - LocalClient webpage
def salt(request: HttpRequest) -> HttpResponse:
    commands = Command.objects.all()
    devices = Device.objects.all()
    context = {
        'commands' : commands,
        'devices' : devices
    }
    return render(request, 'salt.html', context)

# Salt - Salt-pepper webpage
def saltv2(request: HttpRequest) -> HttpResponse:
    commands = Command.objects.all()
    devices = Device.objects.all()
    context = {
        'commands' : commands,
        'devices' : devices
    }
    return render(request, 'saltv2.html', context)

# Find pattern webpage
def findpattern(request: HttpRequest) -> HttpResponse:
    return render(request, 'findpattern.html')
    
############################ WEBPAGES END ############################




############################ SCRIPT SECTION START ############################

def saltapiexternal(request):
#    out = run([sys.executable,'//home//outright//Django//CABE//minion_showversion.py'],shell=False, stdout=PIPE)
#    return render(request, 'saltapiexternal.html', {'out':out.stdout})
    with open('saltapiexternal.txt', 'w') as saltapiexternal:
        out = run([sys.executable,'//home//outright//Django//CABE//minion_showversion.py'],shell=False, stdout=saltapiexternal)
    f = open('//home//outright//Django//CABE//saltapiexternal.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")


def saltapi(request: HttpRequest) -> HttpResponse:
    return render(request, 'saltapipage.html')

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

############################ SCRIPT SECTION END ############################




############################ SALT SECTION START ############################

# Using the below def, it allows to get a minion host name entered by a user and 
# using subprocess module query the BGP summary of a JUNOS device using that value.
# "searchbox" is the name of the HTML form name, which is then stored in the "minion"
# variable to be used later as part of the SALTSTACK CLI command.
def showfrombox(request):
    minion = request.GET.get('searchbox')
    arguments = ['sudo', 'salt', minion, 'net.cli', "'show bgp summary'"]
    data = subprocess.run(arguments, stdout=PIPE, stderr=PIPE, timeout=15)
#    encoded = base64.b64encode(data)
#    context = {
#    'encoded':encoded,
#    }
    context = {
    'data':data,
    }
    return render(request, 'showfrombox.html', context)
#    return render(request, 'showfrombox.html' , {'data':data.stdout})
#    return render(request, 'showfrombox.html' , {'encoded':encoded})

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
    commands = ['sudo', 'salt', minion, 'net.cli', command, '--output=json']
    
    with open('saltout.txt', 'w') as saltout:
        data = subprocess.run(commands, stdout=saltout, stderr=saltout, timeout=15)
    f = open('//home//outright//Django//CABE//saltout.txt', 'r')
    file_content = f.read()
    f.close()
#    return HttpResponse(file_content, content_type="text/plain")
    return render(request, 'showfromdrop.html', {'data': data})


# Using SALT API (Local.Client()), to get dictionary of information. (DROPDOWN only)
def showstandalone(request):
    import salt.client

    output_table1 = [] # BGP Status
    output_table2 = [] # BGP IP
    output_table3 = [] # Display Command
    output = {}

    minion = request.GET.get('device_id')
    command = request.GET.get('command_id')
    local = salt.client.LocalClient()

    # Salt-API dict output
    output = local.cmd(minion, 'net.cli', [command], username='saltapi', password='saltapi', eauth='pam')

    # Before saving the dictionary, Json.dumps must convert all to str (even a dictionary)
    str1 = json.dumps(output)

    # Saving variable 'str' content into a file
    f = open("saltapi.json","w")
    f.write(str1)
    f.close()

    # Reading file and using REGEX to ID values
    f = open('//home//outright//Django//CABE//saltapi.json', 'r')
    read_file = f.read()

    regex1 = re.compile(r'\s\sState: Idle|\s\sState: Active|\s\sState: Connect')
    match_reg1 = regex1.finditer(read_file)

    regex2 = re.compile(r'Peer:\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
#    Peer:\s\d+\.\d+\.\d+\.\d+
    match_reg2 = regex2.finditer(read_file)

    regex3 = re.compile(r'show\s\w+\s\w+')
    match_reg3 = regex3.finditer(read_file)
    

    if match_reg1:
        for match1 in match_reg1:
            output_table1.append(match1.group(0))
    
    if match_reg2:
        for match2 in match_reg2:
            output_table2.append(match2.group(0))

    if match_reg3:
        for match3 in match_reg3:
            output_table3.append(match3.group(0))

    # For logging in console
#    return str1
    return render(request, 'showstandalone.html', {'output': output, 
                                                'output_table1': output_table1, 
                                                'output_table2': output_table2,
                                                'output_table3': output_table3})


# Using SALT API (Local.Client()), to get dictionary of information. (TEXTBOX and DROPDOWN)
def showbgpstatus(request):
    import salt.client

    output_table1 = []
    output_table2 = []
    output_table3 = []

    neighbor_ip = request.GET.get('searchbox1')
    minion1 = request.GET.get('device_id')
    command = 'show bgp neighbor ' + neighbor_ip
    local1 = salt.client.LocalClient()

    # Salt-API dict output
    outputx = local1.cmd(minion1, 'net.cli', [command], username='saltapi', password='saltapi', eauth='pam')

    # Before saving the dictionary, Json.dumps must convert all to str (even a dictionary)
    str1 = json.dumps(outputx)

    # Saving variable 'str' content into a file
    f = open("saltapi2.json","w")
    f.write(str1)
    f.close()

    # Reading file and using REGEX to ID values
    f = open('//home//outright//Django//CABE//saltapi2.json', 'r')
    read_file = f.read()

    regex1 = re.compile(r'\s\sState: Idle|\s\sState: Active|\s\sState: Connect')
    match_reg1 = regex1.finditer(read_file)

    regex2 = re.compile(r'Peer:\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    match_reg2 = regex2.finditer(read_file)

    regex3 = re.compile(r'show\s\w+|show\s\w+')
    match_reg3 = regex3.finditer(read_file)
    

    if match_reg1:
        for match1 in match_reg1:
            output_table1.append(match1.group(0))
    
    if match_reg2:
        for match2 in match_reg2:
            output_table2.append(match2.group(0))

    if match_reg3:
        for match3 in match_reg3:
            output_table3.append(match3.group(0))

    # For logging in console
#    return str1

    return render(request, 'showfromapi2.html', {'outputx': outputx, 
                                                'output_table1': output_table1, 
                                                'output_table2': output_table2,
                                                'output_table3': output_table3})



# Using SALT API (Salt-pepper from DJANGO server), to get dictionary of information. (DROPDOWN only)
def showstandpepper(request):
    minion = request.GET.get('device_id1')
    command = request.GET.get('command_id1')
    arguments = ['pepper', minion, 'net.cli', command]

    output_table1 = []
    output_table2 = []
    output_table3 = []
    output_table4 = []
    
    with open('saltstandpepper.txt', 'w') as saltpepper:
        data = subprocess.run(arguments, stdout=saltpepper, stderr=saltpepper, timeout=25)

     # Before saving the dictionary, Json.dumps must convert all to str (even a dictionary)
    #str1 = json.dumps(data)

    # Reading file and REPLACE new line character with blank space:
    f = open('//home//outright//Django//CABE//saltstandpepper.txt', 'r')
    content = f.read()
    replaced_contents = content.replace('\\n', ' ')

    # Save new file, now with blank spaces
    f = open('//home//outright//Django//CABE//saltstandpepperfinal.txt',"w")
    f.write(replaced_contents)
    f.close()

    # Open file and read it to work with REGEX
    f = open('//home//outright//Django//CABE//saltstandpepperfinal.txt', 'r')
    file = f.read()

    # SHOW VERSION REGEX
    regex1 = re.compile(r'Hostname:\s(.*\d)\s')
    match_reg1 = regex1.finditer(file)

    if match_reg1:
        for match1 in match_reg1:
            output_table1.append(match1.group(1))

    regex2 = re.compile(r'Model:\s(.*)[^\s]')
    match_reg2 = regex2.finditer(file)

    if match_reg2:
        for match2 in match_reg2:
            output_table2.append(match2.group(1))

    # Gathering context before rendering
    context = {
    'output_table1': output_table1,
    'output_table2': output_table2,
    }

    #===========================================================================

    #regex3 = re.compile(r'\s\sState: Idle|\s\sState: Active|\s\sState: Connect')
    #match_reg3 = regex3.finditer(read_file)

    #regex4 = re.compile(r'Peer:\s\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    #match_reg4 = regex4.finditer(read_file)


    #if match_reg3:
    #    for match3 in match_reg3:
    #        output_table3.append(match3.group(1))
    
    #if match_reg4:
    #    for match4 in match_reg4:
    #        output_table4.append(match4.group(1))

    #context = {
    #'output_table3': output_table3,
    #'output_table4': output_table4,
    #}

    # For logging in console
    # return str1
    #if match_reg1:
    return render(request, 'showstandpepper.html', context)

    #if match_reg3:
    #    return render(request, 'showstandpepper1.html', context)

    
############################ SALT SECTION END ############################


########################### FIND PATTERN SECTION STARTS ############################

# Scripts: Patternfinder

import os.path
import re
from tabulate import tabulate

def showfindpattern(request):

    pattern = request.GET.get('pattern')
#    print(" ")
#    pattern = input("Please insert what look for: ")
#    print(" ")
#    print("Entered word is: " pattern)
#    print(" ")

    list = []
    output1 = []
    headers = ['Index', 'Network Device','Full Line']

    for filename in os.listdir('//home//outright//Django//rancid//backups//NETWORK//'):
        if re.match('.*', filename):
            try:
                filepath = '//home//outright//Django//rancid//backups//NETWORK//'+filename
                fileh = open(filepath, "r")

                for line in fileh.readlines():
                    for word in line.split():
                        if re.match(pattern, word):
                            list = [filename, line]
                            output1.append(list)
            except:
                pass

    context = {
        'output1': output1,
    }
#    print(tabulate(output1, headers=headers, tablefmt='plain', showindex="always"))
    return render(request, 'showfindpattern.html', context)
########################### FIND PATTERN SECTION ENDS ############################