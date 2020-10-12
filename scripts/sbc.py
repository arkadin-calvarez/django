from pathlib import Path
import re
import json
import pandas as pd

output_table1 = []
output_table3 = []
output_table4 = []
output_table5 = []

#f = open('/home/c.alvarez/scripts/sbc_apac.txt', 'r')
f = open('//Users//outright//Downloads//VOICE//ifcsbc01p', 'r')
read_file = f.read()

#regex1 = re.compile(r'rancid\s(\w{3}sbc01p)')
#match_reg1 = regex1.finditer(read_file)

#if match_reg1:
#    for match1 in match_reg1:
#        output_table1.append(match1.group(1))

#print ('\n'.join(map(str, output_table1)))

regex3 = re.compile(r'name\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s([M|m].*)')
match_reg3 = regex3.finditer(read_file)

regex4 = re.compile(r'ip-address\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.)')
match_reg4 = regex4.finditer(read_file)

regex5 = re.compile(r'sub-port-id\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s(.*)')
match_reg5 = regex5.finditer(read_file)

#regex6 = re.compile(r'netmask\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d[0-24])')
#match_reg6 = regex6.finditer(read_file)

if match_reg3:
    for match3 in match_reg3:
        output_table3.append(match3.group(1))

if match_reg4:
    for match4 in match_reg4:
        output_table4.append(match4.group(1))

if match_reg5:
    for match5 in match_reg5:
        output_table5.append(match5.group(1))

#if match_reg6:
#    for match6 in match_reg6:
#        output_table6.append(match6.group(1))

dic = {'Interface':output_table3, 'IP address':output_table4,'VLAN ID':output_table5}
df = pd.DataFrame(dic)
print (df)
#print ('\n'.join(map(str, output_table3)))
#print ('\n'.join(map(str, output_table4)))
