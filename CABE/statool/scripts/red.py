import salt.modules.network
import re
import json
from lxml import etree 
from tabulate import tabulate
import pandas
import sys
import time
import yaml



def final():

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




def parse_addresses():

# Salt Module, executing command on router    
    interfaces = __salt__['net.cli']('show configuration interfaces | display set', format='xml')['out']['show configuration interfaces | display set']
#    s = ['set interfaces ge-0/0/1 unit 0 family inet sampling input','set interfaces ge-0/0/1 unit 0 family inet sampling output','set interfaces ge-0/0/0 unit 0 family inet sampling input','set interfaces ge-0/0/0 unit 0 family inet sampling output','set interfaces ge-0/0/0 unit 0 family inet address 192.168.15.66/24','set interfaces ge-0/0/1 unit 0 family inet dhcp','set interfaces ge-0/0/2 unit 0 family inet address 1.1.1.1/30','set interfaces ge-0/0/2 unit 0 family inet address 192.168.99.1/30']

# Saving output, which is now sorted horizontally. (Since is not a list)
    with open("/srv/salt/_modules/table1.txt", "w") as file:
        for char in interfaces:
            sys.stdout.flush()
            file.write("%s\n" % char)

#    r1 = re.findall(r"^\set+", s)
#    return r1

# Defining a variable, where we are looking for the word "sampling"
#    pattern = re.compile(r'sampling')


#    for i, line in enumerate(open("/srv/salt/_modules/table1.txt")):
#        return 'Found on line %s: %s' % (i+1, match.group())
#        for match in re.finditer(pattern, line):
#            print 'Found on line %s: %s' % (i+1, match.group())


# Create a list of list, for every line read:

#    a_file = open("/srv/salt/_modules/table1.txt", "r")

#    list_of_lists = []
#    for line in a_file:
#        stripped_line = line.strip()
#        line_list = stripped_line.split('set')
#        list_of_lists.append(line_list)

#    a_file.close()

#    return(list_of_lists)



'''
interface_dict = {}
return("interfaces | services")
mydict ={}

s = __salt__['net.cli']('show configuration interfaces | display set', format='xml')['out']['show configuration interfaces | display set']

def netflow():

    for i in s:
            interface = re.search(r"ge.{1,7}", i)
            if "sampling" in i:
                service = "sampling"
                mydict.setdefault("router",{interface.group(): service})
            else:
                service = "None"
            print(f"{interface.group()} | {service}")
    if bool(mydict):
        return mydict
    return "None"

return(netflow)
'''



def match():

    list_sampling = []

    interfaces = __salt__['net.cli']('show configuration interfaces | display set', format='xml')['out']['show configuration interfaces | display set']

# This def output ("n/a") works okay, but the REGEX is not done correctly or "interfaces" output
# is verticall, not allowing to find the word "set" as we need
    if re.match(r'(ge.{1,7}).*?(?=sampling)',interfaces):
        list_sampling.append()
    else:
        list_sampling.append('n/a') 

    with open("/srv/salt/_modules/matches_table.txt", "w") as file:
       for item in list_sampling:
           file.write("%s\n" % item)

    return list_sampling
'''
    interfaces = __salt__['net.cli']('show configuration interfaces | display set', format='xml')['out']['show configuration interfaces | display set']

    with open("/srv/salt/_modules/xxx.txt", "w") as file:
        file.write(interfaces)
    
    pattern = re.findall(r'sampling', interfaces)
    pattern1 = re.findall(r'interfaces', interfaces)

    return pattern, pattern1
'''

'''
def test():

    interfaces = __salt__['net.cli']('show interfaces')['out']['show interfaces']

    with open("/srv/salt/_modules/xxx.txt", "w") as file:
        file.write(interfaces)

    return interfaces[0:5]
'''

'''
def wordcount(filename, listwords):

Word Counter from file already stored in some place
    
    try:
        file = open(filename, "r")
        read = file.readlines()
        file.close()
        for word in listwords:
            lower = word.lower()
            count = 0
            for sentance in read:
                line = sentance.split()
                for each in line:
                    line2 = each.lower()
                    line2 = line2.strip("!@#$%^&*()=+")
                    if lower == line2:
                        count += 1
            print(lower, ":", count)
    except FileExistsError:
        print("The file does not exist")

wordcount("/srv/salt/_modules/xxx.txt", ['sample-input,'])   
'''