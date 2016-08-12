import urllib
import xml.etree.ElementTree as ET
from APIKey import *

# url = raw_input('Enter link: ')
url = "".join(['http://api.amp.active.com/camping/campgrounds?pstate=CA&siteType=2003&api_key=', API_KEY])

uh = urllib.urlopen(url)
data = uh.read()
print('Retrieved',len(data),'characters')
tree = ET.fromstring(data)

campgrounds = tree.findall('.//result')
print('Count: ',len(campgrounds))
# print(ccount)
# print(i.facilityName.text for i in ccount)
# print('Sum: ', sum([int(i.text) for i in ccount]))
for child in campgrounds:
	print(child.get("facilityName"))
	if child.get("facilityName") == "PINECREST":
		print(child.tag, child.attrib)
