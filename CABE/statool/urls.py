from django.conf.urls import url
#from django.contrib import admin
from django.urls import path, include
from . import views, minion_form
from django.contrib.auth.views import LoginView

from . import views
from accounts.views import login_view, register_view, logout_view

urlpatterns = [
# "path('', views.home" will show default page for http://localhost:7878 requests
# The following paths (routes) like "statool/" and "scripts/" were created to
# forward request based on what was configured in "views.py" file, adding the 
# ".statool" or ".scripts" name

# Go to MAIN webpages
    path('', views.home, name='network-tools-home'),
    path('statool/', views.statool, name='statool-home'),
    path('scripts/', views.scripts, name='scripts'),
    path('salt/', views.salt, name='salt'),
    path('saltv2/', views.saltv2, name='saltv2'),
    path('findpattern/', views.findpattern, name='findpattern'),

# Go to RESULTS webpages
# "Panaceia" website results
    path('services/<int:service_id>', views.get_device_stats, name="service"),
    path('statool/devices/<int:device_id>', views.get_device_stats, name="device"), # With ABSOLUTE URL (see models.py)

# "Scripts" website results
    path('saltapiexternal/', views.saltapiexternal, name='saltapiexternal'),
    path('saltout/', views.saltout, name='saltout'),
    path('saltapipage/', views.saltapi, name='saltapi'),

# "Findpattern" website
#    path('findpattern/', views.findpattern, name='findpattern'),

# "SALT Scripts" website results
    path('showstandalone/', views.showstandalone, name='showstandalone'),
    path('showbgpstatus/', views.showbgpstatus, name='showbgpstatus'),
    path('showstandpepper/', views.showstandpepper, name='showstandpepper'),
#    path('showstandpepper1/', views.showstandpepper1, name='showstandpepper1'),
    path('showfromdrop/', views.showfromdrop, name='showfromdrop'),
#    path('salt/devices/*', views.showfromdrop, name='showfromdrop'),
    path('showfrombox/', views.showfrombox, name='showfrombox'),

# Scripts website - Disabled
#    path('output/', views.output, name='scriptdone'),
#    path('another/', views.another, name='scriptfinal'),
#    path('bgp1/', views.show_bgp_fromfile, name='show_bgp_fromfile'),
]
