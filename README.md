# DJANGO Apps
============

Perform Network Monitoring via WEB, using Django applications and python scripts 

Goals Achieved
- Query Cisco and Juniper devices, using Netmiko libraries
- Display information on webpage
- Provide basic local authentication method before access the web page


Django Project Name:  NIO
====================
- App1:     statool
- App2:     accounts (disabled)


File/Site Structure
===================
centos:7878 --> home (authentication) --> statool--> devices output (AUTH not operational)
            --> home (no authentication) --> statool--> devices output
            --> home (no authentication) --> statool--> scripts --> output
            
