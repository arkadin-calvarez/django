import salt.modules.network
import re
import json
from lxml import etree 
from tabulate import tabulate
import pandas
import sys
import time
import yaml

interfaces = []
output_table1 = []
output_table2 = []
output_table3 = []

interfaces = __salt__['net.cli']('show configuration interfaces | display set', format='xml')['out']['show configuration interfaces | display set']

# Saving output into a file for further use
with open("/srv/salt/_modules/aaa.txt", "w") as file:
    file.write(interfaces)

# Reading content from a YAML file and print it as list
#    with open("/srv/salt/_modules/aaa.txt") as out:
#        list = yaml.load(out, Loader=yaml.FullLoader)
#        return(list)

# Regex patterns to match things
regex1 = re.compile(r'(ge.{1,7}.{7}).*?(?=sampling)')
match_reg1 = regex1.finditer(interfaces)

regex2 = re.compile(r'ge.{1,7}.{7}')
match_reg2 = regex2.finditer(interfaces)


# IF stataments and FOR, to match and print
if match_reg1:
    output_table1.insert(0, "Sampled interfaces")
    for match1 in match_reg1:
        output_table1.append(match1.group(1))

if match_reg2:
    output_table2.insert(0, "Not sampled interfaces")
    for match2 in match_reg2:
        output_table2.append(match2.group())

# Differences between two tables: 
difference_list = []
for item in output_table2:
    if item not in output_table1:
        difference_list.append(item)

final = []
final.insert(0, "To enable sampling, insert the following on target device")
for line in difference_list:
    final.append("set interfaces " + line + "family inet sampling [input/output]")

return output_table1, difference_list, final
  
#    return difference_list, output_table1
#    return ("No sampled interfaces : " + str(difference_list))
#    return output_table1, difference_list