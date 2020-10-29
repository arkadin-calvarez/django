#!/usr/bin/python
#--------------------------------------------------------------------------------------------------------

import re
import os
import sys
import requests

# Import modules for CGI handling 
import cgi, cgitb 


def showfindpattern():

    # Create instance of FieldStorage 
    form = cgi.FieldStorage() 

    # Get data from main page
    pattern = form.getvalue('pattern')

    # Defining lists
    lista1 = []
    output1 = []
    
    # From local copy of NETWORK devices configs, looks files (manual copy made from /var/rancid/NETWORK/configs to /var/www/finder folder) 
    for filename in os.listdir('/var/www/finder/configs/'):
        if re.match('.*', filename):
            try:
                filepath = '/var/www/finder/configs/'+filename
                fileh = open(filepath, "r")

                for line in fileh.readlines():
                    regex = re.compile(pattern)
                    match_reg = regex.finditer(line)
                    if match_reg:
                        for match in match_reg:
                            lista1 = [line, filename]
                            output1.append(lista1)
            except:
                print('Impossible to open specified path location')
                pass

    return output1

# Storing retuned function output into "outputx" list
outputx = showfindpattern()

#--------------------------------------------------------------------------------------------------------
# HTML Start

header = '''
<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <style>
    h1,h2,h3,h5,b,i,p,a,table {
      margin: 50px;
    }
    tr {
      text-align: center;
      border-bottom: 1px solid #bbb;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
      border-left-radius: 8px;
      border-right-radius: 8px;
    }
    th {
      color: white;
      text-align: center;
      border-bottom: 1px solid #bbb;
      border-top-left-radius: 8px;
      border-top-right-radius: 8px;
      border-left-radius: 8px;
      border-right-radius: 8px;
      background-color: lightskyblue;
      width: 5cm;
    }
  </style>

<title>RANCID Finder tool</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-15" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta http-equiv="Content-Language" content="en" />

<style type="text/css">
@import url(../../resources/style.css);
@import url(../../resources/theme.default.css);
#myDIV {
width: 70%;
padding: 5px 0;
text-align: center;
background-color: WhiteSmoke;
margin-top: 5px;
</style>

<script type="text/javascript" src="../../resources/jquery/jquery-3.2.1.min.js"></script>
<script type="text/javascript" src="../../resources/jquery/jquery.tablesorter.js"></script>
<script type="text/javascript" src="../../resources/jquery/jquery.tablesorter.widgets.js"></script>
<script>
$(function(){
	// call the tablesorter plugin
	$("#default").tablesorter({ sortList: [[1,1]]});
});

function myFunction() {
	var x = document.getElementById("myDIV");
	if (x.style.display === "none") {
		x.style.display = "block";
	} else {
		x.style.display = "none";
	}
}
</script>
</head>
'''

contentstart = '''
<body>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
  <div id="container">
    </br>
    <h1 style="color:blue">REGEX Find Pattern Tool</h1>
    <h3>Results</h3>
    <a href="https://rancid.arkadin.lan/finder/finder.html">Back to main menu</a>
'''

contentend = '''
  </div>
'''

foot = '''
</br>
</br>
<p style="color:blue" id="footer">Copyright 2020 NTT - Powered by NIO Team</p>
</div>
</body>
</html>
'''

# MAIN
print("Content-Type: text/html")
print # blank line, end of headers

# HTML PRINT
print(header)
print(contentstart)



# MAIN TABLE
print('<table id=\'default\' class=\'tablesorter-default\'>')
print('<thead>')
print('<tr><th>Device</th><th>REGEX Pattern</th></tr>')
print('</thead>')
print('<tbody>')


# FOR statement to go through function returned items
if outputx:
    for value, val in outputx:

    # PRINT items in HTTP format
        print '''<tr>
                    <td>%s</td><td>%s</td>
                </tr>
        ''' % (	val, value )
else:
    # PRINT not found
        print '''<tr>
                    </br>
                    </br>
                    </br>
                    <h2 style="color:red">Regex value not Found</h2>
                </tr>'''
        
print('</tbody>')
print('</table>')
print contentend
print foot


#--------------------------------------------------------------------------------------------------------
# HTML End
