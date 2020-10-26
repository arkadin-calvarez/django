#!/usr/bin/python
#--------------------------------------------------------------------------------------------------------

import re
import os
import sys
import requests


def showfindpattern():

    # Import modules for CGI handling 
    import cgi, cgitb 

    # Create instance of FieldStorage 
    form = cgi.FieldStorage() 

    # Get data from fields
    pattern = form.getvalue('pattern')

#    pattern = '10.120.'


    lista1 = []
    output1 = []
    
    for filename in os.listdir('/var/www/finder/configs/'):
        if re.match('.*', filename):
            filepath = '/var/www/finder/configs/'+filename
            fileh = open(filepath, "r")

            for line in fileh.readlines():
                for word in line.split():
                    if re.match(pattern, word):
                        lista1 = [line, filename]
                        output1.append(lista1)
    return output1


#outputx = ['hols', 'fdfd', 'neo']
outputx = showfindpattern()
#outputx = files()

#--------------------------------------------------------------------------------------------------------
# HTML

header = '''
<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\" \"http://www.w3.org/TR/html4/strict.dtd\">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr" lang="fr">
<head>
<title>RANCID Finder tool</title>
<link rel="icon" type="image/png" href="../../resources/site/europeanunion.png" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-15" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<meta http-equiv="Content-Language" content="fr" />
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
<div id="conteneur">
<h1 id="header"></h1>
<table>
<tr>
<td>
<ul id="menu">
<li><a href="https://atlnetutil01.arkadin.lan:8081/inventory/links.html">Links</a></li>
</td>
</tr>
</table>
<div id="contenu">
'''

contentend = '''
</div>
'''

foot = '''
<p id="footer">Copyright 2020 NTT - NIO Team</p>
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



# MAIN TABLE PRINT
print('<table id=\'default\' class=\'tablesorter-default\'>')
print('<thead>')
print('<tr style="color: #fff; background: blue;"><th>line</th><th>Device</th></tr>')
print('</thead>')
print('<tbody>')


# FOR EACH ASSET
for value, val in outputx:

# DISPLAY CLIENTS
    print '''<tr>
                <td>%s</td><td>%s</td>
            </tr>
    ''' % (	value, val )

print('</tbody>')
print('</table>')
print contentend
print foot