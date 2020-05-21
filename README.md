# DJANGO Apps
============

Perform Network Monitoring via WEB, using Django applications and python scripts 

Goals Achieved
- Query Cisco and Juniper devices, using Netmiko libraries
- Display information on webpage
- Provide basic local authentication method before access the web page


Django Project Name:  CABE (Django/CABE/statool)
====================
- App1:     statool
- App2:     accounts (disabled)


File/Site Structure
===================
centos:7878 
            --> home (no authentication) --> Panaceia Statool--> local devices, dropdown and query using Django Views defs
            --> home (no authentication) --> Python Scripts --> using python to query devices
            --> home (no authentication) --> SALT Queries --> using SALTSTACK to query devices
