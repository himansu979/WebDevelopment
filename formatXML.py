
xml = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><AddResponse xmlns="http://tempuri.org/"><AddResult>15</AddResult></AddResponse></soap:Body></soap:Envelope>"""

#print(xml)

#import xml.etree.ElementTree as ET 
from lxml import etree as ET 

tree = ET.fromstring(xml.encode('utf8'))

result = tree.find('.//{http://tempuri.org/}AddResult').text
print(result)

output = ET.tostring(tree, pretty_print=True, method='xml').decode()

#print(output)

with open("output.xml", "w") as f:
    f.write(output)






