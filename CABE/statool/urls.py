from django.conf.urls import url
#from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView

from . import views
#from accounts.views import login_view, register_view, logout_view

urlpatterns = [
# Below line ('') will show default page for http://localhost:7777 requests
# The following paths (routes) like "statool/" and "scripts/" were created to
# forward request based on what was configured in "views.py" file, adding the 
# ".statool" or ".scripts" name

    path('', views.home, name='network-tools-home'),
    path('statool/', views.statool, name='statool-home'),
    path('scripts/', views.scripts, name='scripts'),
    path('output/', views.output, name='scriptdone'),
    path('another/', views.another, name='scriptfinal'),
    path('external/', views.external, name='external'),
#    path('devices/<int:device_id>', views.devices_cat),
    path('salt/', views.salt, name='salt'),
    path('devices/<int:device_id>', views.get_device_stats, name="device"),
    path('services/<int:service_id>', views.get_device_stats, name="service"),
#    path('services/', views.ccasp, name="ccasp"),
    path('/devices/2', views.get_device_stats, name="device")
]
