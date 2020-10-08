from pathlib import Path
import re
import json
import pandas as pd
import os

output_table1 = []
output_table3 = []
output_table4 = []
output_table5 = []

for filename in os.listdir('/var/lib/rancid/VOICE/configs'):
    if re.match('^.*$', filename):
        try:
            if not filename == 'CVS' and not filename == '.cvsignore' and not filename.endswith('.new'):
                filepath = '/var/lib/rancid/VOICE/configs/'+filename
                read_file = open(filepath, "r")

                for line in read_file.readlines():


                    regex3 = re.compile(r'name\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s([M|m].*)')
                    match_reg3 = regex3.finditer(read_file)

                    regex4 = re.compile(r'ip-address\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.)')
                    match_reg4 = regex4.finditer(read_file)

                    regex5 = re.compile(r'sub-port-id\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s\s(.*)')
                    match_reg5 = regex5.finditer(read_file)


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

                    dic = {'Interface':output_table3,'VLAN':output_table5,'IPs':output_table4}
                    df = pd.DataFrame(dic)
                    print (df)
        
        except IOError:
			print "I/O error {}".format(filepath)
#print ('\n'.join(map(str, output_table3)))
#print ('\n'.join(map(str, output_table4)))