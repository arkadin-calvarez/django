from django.conf.urls import url
#from django.contrib import admin
from django.urls import path, include
from . import views, minion_form
from django.contrib.auth.views import LoginView

from . import views
from accounts.views import login_view, register_view, logout_view

urlpatterns = [
# Below line ('') will show default page for http://localhost:7777 requests
# The following paths (routes) like "statool/" and "scripts/" were created to
# forward request based on what was configured in "views.py" file, adding the 
# ".statool" or ".scripts" name

    path('', views.home, name='network-tools-home'),
    path('statool/', views.statool, name='statool-home'),
    path('scripts/', views.scripts, name='scripts'),
    path('salt/', views.salt, name='salt'),
    path('output/', views.output, name='scriptdone'),
    path('another/', views.another, name='scriptfinal'),
    path('external/', views.external, name='external'),
    path('saltout/', views.saltout, name='saltout'),
    path('bgp/', views.show_bgp_summ, name='show_bgp_summ'),
    path('bgp1/', views.show_bgp_fromfile, name='show_bgp_fromfile'),
    path('salt/devices/vsrx1', views.show, name='show'),
    path('statool/devices/<int:device_id>', views.get_device_stats, name="device"), # With ABSOLUTE URL (see models.py)
    path('services/<int:service_id>', views.get_device_stats, name="service"),
]
