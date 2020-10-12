import os.path
import re
from tabulate import tabulate


print(" ")
pattern = input("Please insert what look for: ")
print(" ")
print("Entered word is: "+pattern)
print(" ")
list = []
output1 = []
headers = ['Index', 'Network Device','Full Line']

for filename in os.listdir('//Users//outright//Downloads//NETWORK//'):
    if re.match('.*', filename):
        try:
            filepath = '//Users//outright//Downloads//NETWORK//'+filename
            fileh = open(filepath, "r")

            for line in fileh.readlines():
                for word in line.split():
                    if re.match(pattern, word):
                        list = [filename, line]
                        output1.append(list)
        except:
            pass

print(tabulate(output1, headers=headers, tablefmt='plain', showindex="always"))