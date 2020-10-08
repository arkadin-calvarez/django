import re

stored = input("Enter Filename: ")
print("You are opening the following file: " + stored)

#if stored.lower() == "file1":
#    print("You are opening the following file:" + stored)

#filepath = '//Users//outright//Downloads//NETWORK//'+stored
filepath = '//Users//outright//Downloads//'+stored
open_file = open(filepath, "r")
read_file = open_file.read()
print("ALL file content below")
print('')
print(read_file)
print('')

output_table1 = []
output_table2 = []

#regex1 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
#regex1 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
#match_reg1 = regex1.finditer(read_file)

#regex1 = re.compile(r'\D\D\D')
#match_reg1 = regex1.finditer(read_file)

#regex2 = re.compile(r'(MASK)\s\s\s\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
#match_reg2 = regex2.finditer(read_file)
match_reg1 = '255.255.255.0'
mask1 = '255.255.255.0'
#if match_reg1:
for match1 in match_reg1:
    if match1 == mask1:
        output_table2.append(match1)
    else:
        output_table1.append(match1)

print("IP")
print('\n'.join(map(str, output_table1)))
print(" ")
print("MASK")
print('\n'.join(map(str, output_table2))) 