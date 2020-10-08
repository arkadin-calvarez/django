import os.path
import re
import pandas as pd
from tabulate import _table_formats, tabulate

headers = ['index', 'values', 'files']
#result = ['val1', 'val2', 'val3']
result = [['value1','file1'],['value2','file1'],['value3','file99']]
#result = {'value1': 'file1', 'value2': 'file1', 'value3': 'file99'}
result1 = [1, 2 ,3]

print(tabulate(result, headers=headers, tablefmt='plain', showindex="always"))