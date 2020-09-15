#!/usr/bin/env python3

import argparse
import os,sys
sys.path.insert(0, os.path.abspath('modules/'))
import filelib as flib
import parsers as parse
import re
from shared_regex import *

parser = argparse.ArgumentParser(
  formatter_class = argparse.RawDescriptionHelpFormatter,
  epilog = ('''\
Parse network hosts configurations and print BIND style reverse zone files
for RFC1918 IP addresses based on the following address classes:

host: 10.0.0.0/8
link: 172.0.0.0/8 (due to misuse of addresses, the entire 172/8 is checked)
loop: 192.168.0.0/16
public: 185.37.220.0/22, 77.111.208.0/22, 192.206.95.0/24, 103.214.228.0/24

Network host configurations are parsed to obtain the IP address data so you must
provide a directory with a configuration file for each host you want to process.

The script checks for the location of configs in the following order:

1. A path provided the --dir argument
2. A path provided in a file named ~/.conf_dir
3. Default path is /var/lib/rancid/NETWORK/configs

The easiest is just to run the script while logged in to atlrancid01 and use the
default path.

However, if you want to keep a config repository somewhere besides
atlrancid01:

ababson@atlnetutil01:~$ cat .conf_dir
/home/ababson/configs/NETWORK/configs

Zone files will be written to the /tmp directory.

examples:
    dns_gen_records.py host
    dns_gen_records.py link
    dns_gen_records.py loop --verbose
    dns_gen_records.py public

    dns_gen_records.py loop --dir='/home/ababson/configs/NETWORK/configs'

      '''))
parser.add_argument(
  "ptr_class", help="Which class of addresses to process: host, link, or loop.")
parser.add_argument(
  "--dir", help="Alternate directory where network host configs are located.")
parser.add_argument("--verbose", help="Print to stdout.", action="store_true")

# this is the default SOA that will print at the beginning of each zone file
soa = """$TTL 4h
@ IN SOA pa2dns01.net.arkadin.lan. nio.arkadin.com. (
     1     ; Serial
     3h    ; Refresh after 3 hours
     1h    ; Retry after 1 hour
     1w    ; Expire after 1 week
     1h )  ; Negative caching TTL of 1 hour

@              IN NS     pa2dns01.net.arkadin.lan.
pa2dns01       IN A      10.124.23.53
; Do not change above this line unless you know what you're doing. :)
"""

# records to manually add to db.10
manual_db_10 = """
; Network servers - manually added
2.1.0          IN PTR    atl-bastion-01.net.arkadin.lan.
6.1.0          IN PTR    chi-bastion-01.net.arkadin.lan.
14.1.0         IN PTR    ld4-bastion-01.net.arkadin.lan.
18.1.0         IN PTR    mtp-bastion-01.net.arkadin.lan.
22.1.0         IN PTR    pa2-bastion-01.net.arkadin.lan.
38.1.0         IN PTR    atl-bastion-02.net.arkadin.lan.
20.19.100      IN PTR    atlrancid01.arkadin.lan.
21.19.100      IN PTR    atlnetutil01.arkadin.lan.
88.137.115     IN PTR    pa2-sltmst-01.net.arkadin.lan.
89.137.100     IN PTR    atl-sltprx-01.net.arkadin.lan.
89.137.250     IN PTR    ifc-sltprx-01.net.arkadin.lan.
89.137.115     IN PTR    pa2-sltprx-01.net.arkadin.lan.
90.90.250      IN PTR    netflow.arkadin.lan.
"""

# zone files will be written here
zone_dir = "/tmp/"

db_dict = {}
db_185_37 = {'zone': 'db.185.37'}
db_77_111 = {'zone': 'db.77.111'}
db_192_206_95 = {'zone': 'db.192.206.95'}
db_103_214_228 = {'zone': 'db.103.214.228'}
db_10 = {'zone': 'db.10'}
# yes I know should be 172.16/12 but we are misusing addresses
db_172 = {'zone': 'db.172'}
db_192_168 = {'zone': 'db.192.168'}

args = parser.parse_args()

domain = 'net.arkadin.lan.'

if args.dir:
    conf_dir = args.dir
else:
    # first check for a custom directory specified by ~/.conf_dir
    userhome = os.getenv('HOME')
    conf_dir_var = '/'.join([userhome, '.conf_dir'])
    if os.path.exists(conf_dir_var):
        with open(conf_dir_var, 'rt') as fh:
            conf_dir = fh.readlines()
        for line in conf_dir:
            if line.startswith('#'):
                continue
            else:
                conf_dir = line.rstrip()
    else:
        conf_dir = '/var/lib/rancid/NETWORK/configs'

def gen_reverse_zone(db_dict):
    zone = db_dict.pop('zone')
    with open(zone_dir + zone, 'wt') as fh:
        fh.write('{0}'.format(soa))
        # all servers are currently in 10/8 address space
        if zone == 'db.10':
            fh.write('{0}'.format(manual_db_10))
        fh.write('\n; Auto-generated section - NETWORK\n')
        for ip_addr, records in sorted(db_dict.items()):
            octet1, octet2, octet3, octet4 = ip_addr.split('.')
            for record in records:
                # don't print netscreen -2 standby unless it's mgmt
                if not 'mgmt' in record:
                    match_pri = re.search(r'(\w+fw0\d)-1(.*)', record)
                    if match_pri:
                        record = match_pri.group(1) + match_pri.group(2)
                    elif re.search(r'fw0\d-2', record):
                        continue
                if re.search(r'^(10|172)\.', ip_addr):
                    ptr = '.'.join([octet4, octet3, octet2])
                elif re.search(r'^(192\.168|185\.37|77\.111)\.', ip_addr):
                    ptr = '.'.join([octet4, octet3])
                elif re.search(r'^(192\.206\.95|103\.214\.228)\.', ip_addr):
                    ptr = octet4
                host = '.'.join([record, domain])
                if args.verbose:
                    print('{0:<15}IN PTR    {1}'.format(ptr, host.lower()))
                fh.write('{0:<15}IN PTR    {1}\n'.format(ptr, host.lower()))

configs = flib.get_configs(conf_dir)

ip_dict = {}

# db_dict is just a reference to the specific db dicts to make the code shorter
db_dict = {}

for (hostname, platform), config_lines in configs.items():
    host_ip_dict = {hostname: {}}
    E = enumerate(config_lines)
    parse.parse_any(hostname, platform, E, host_ip_dict) 
    ip_dict.update(host_ip_dict)

for hostname, intfs in ip_dict.items():
    for intf, ip_addrs in intfs.items():
        if len(ip_addrs) < 1:
            continue
        for (ip_addr, ip_mask) in ip_addrs:
            private_match = re.search(r'^((10)|(172)|(192\.168))\.', ip_addr)
            ripe1_match = re_arkad_ripe1_v4.search(ip_addr)
            ripe2_match = re_arkad_ripe2_v4.search(ip_addr)
            arin1_match = re_arkad_arin1_v4.search(ip_addr)
            apnic1_match = re_arkad_apnic1_v4.search(ip_addr)
            if private_match:
                ip_range = private_match.group(1)
                if ip_range == '10':
                    db_dict = db_10
                elif ip_range == '172':
                    db_dict = db_172
                elif ip_range == '192.168':
                    db_dict = db_192_168
            elif ripe1_match:
                ip_range = ripe1_match.group(1)
                db_dict = db_185_37
            elif ripe2_match:
                ip_range = ripe2_match.group(1)
                db_dict = db_77_111
            elif arin1_match:
                ip_range = arin1_match.group(1)
                db_dict = db_192_206_95
            elif apnic1_match:
                ip_range = apnic1_match.group(1)
                db_dict = db_103_214_228
            else:
                # not what we're looking for
                continue
            record = '-'.join([hostname, intf])
            record = re.sub('[./]', '-', record)
            if ip_mask == 'hsrp':
                record += '-hsrp'
            if ip_mask == 'vrrp':
                record += '-vrrp'
            try:
                db_dict[ip_addr].append(record)
            except KeyError as e:
                db_dict.update({ip_addr: [record]})

if args.ptr_class == 'host':
    print('# db.10')
    gen_reverse_zone(db_10)
elif args.ptr_class == 'link':
    print('# db.172')
    gen_reverse_zone(db_172)
elif args.ptr_class == 'loop':
    print('# db.192.168')
    gen_reverse_zone(db_192_168)
elif args.ptr_class == 'public':
    print('# db.185.37')
    gen_reverse_zone(db_185_37)
    print('# db.77.111')
    gen_reverse_zone(db_77_111)
    print('# db.192.206.95')
    gen_reverse_zone(db_192_206_95)
    print('# db.103.214.228')
    gen_reverse_zone(db_103_214_228)
elif args.ptr_class == 'all':
    print('# db.10')
    gen_reverse_zone(db_10)
    print('# db.172')
    gen_reverse_zone(db_172)
    print('# db.192.168')
    gen_reverse_zone(db_192_168)
    print('# db.185.37')
    gen_reverse_zone(db_185_37)
    print('# db.77.111')
    gen_reverse_zone(db_77_111)
    print('# db.192.206.95')
    gen_reverse_zone(db_192_206_95)
    print('# db.103.214.228')
    gen_reverse_zone(db_103_214_228)
# hidden option - provide hostname and get a dump of IP info
elif ip_dict.get(args.ptr_class):
    print(ip_dict[args.ptr_class])
else:
    print('Sorry, try again.')

