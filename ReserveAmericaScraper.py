# coding=utf-8
#!/usr/bin/env python
import os
import urllib
import xml.etree.ElementTree as ET
import mechanize
from bs4 import BeautifulSoup
from APIKey import *
from HTMLparser import *
import smtplib
from EMail import *

def CADataBase():
	filename1 = "CACampgrounds.xml"
	if os.path.isfile(filename1):
		tree = ET.parse(filename1).getroot()
		CampGrounds = tree.findall('.//result')
	else:
		# Campground API to find facility name, contractCode, and parkId.
		cgapi_url = "".join(['http://api.amp.active.com/camping/campgrounds?pstate=CA&siteType=2003&api_key=', API_KEY])
		cgapi = urllib.urlopen(cgapi_url)
		cgapi_data = cgapi.read()
		# print('Retrieved',len(cgapi_data),'characters')
		elems = ET.fromstring(cgapi_data)
		CampGrounds = elems.findall('.//result')
		# print('Campgrounds Count: ',len(CampGrounds))
		tree = ET.ElementTree(elems)
		tree.write(filename1)
		# print(filename1, "is saved!")
	return CampGrounds

def CADataBaseShower():
	# Screen amenities - Showers
	filename2 = "CACampgrounds_Showers.xml"
	if os.path.isfile(filename2):
		tree = ET.parse(filename2).getroot()
		TargetCampGrounds = tree.findall('.//result')
	else:
		TargetCampGrounds = ET.Element("root")
		CampGrounds = CADataBase()
		for campground in CampGrounds:
			# Campsite API to get all amenities.
			url = "".join(["http://api.amp.active.com/camping/campground/details?contractCode=", \
											campground.get("contractID"), "&parkId=", campground.get("facilityID"), \
											"&api_key=", API_KEY])
			details = urllib.urlopen(url)
			details_data = details.read()
			tree = ET.fromstring(details_data)
			if campground.get("facilityName") == "MONO HOT SPRINGS" or \
				 campground.get("facilityName") == "GROVER HOT SPRINGS SP":
				TargetCampGrounds.append(campground)
				# print(campground.get("facilityName"))
			else:
				for ams in tree.findall('.//amenity'):
					if ams.get("name") == "Showers" and ams.get("distance") == "Within Facility":
						TargetCampGrounds.append(campground)
						# print(campground.get("facilityName"))
		tree = ET.ElementTree(TargetCampGrounds)
		tree.write(filename2)
		# print(filename2, "is saved!")
	return TargetCampGrounds

def SearchCampground(SearchParameters, TargetCampGrounds):
	date = SearchParameters["date"]
	lengthOfStay = SearchParameters["length"]
	siteCode = ""
	# Give the Google maps base link
	GOOGLE_MAPS = "https://maps.google.com/maps/?q="
	# Looping through all campgrounds
	RESULTs = []
	for campground in TargetCampGrounds:
		# url of your desired campground
		name = campground.get("facilityName").replace(" ", '-')
		url = "".join(["http://www.reserveamerica.com/camping/", name, \
									 "/r/campgroundDetails.do?contractCode=", campground.get("contractID"), \
									 "&parkId=", campground.get("facilityID")])

		# Create browser
		br = mechanize.Browser()

		# Browser options
		br.set_handle_equiv(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1);
		br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')];
		br.open(url);

		# Fill out form
		br.select_form(nr=0)
		br.form.set_all_readonly(False) # allow changing the .value of all controls
		br.form["campingDate"] = date
		br.form["lengthOfStay"] = lengthOfStay
		br.form["siteCode"] = siteCode
		response = br.submit()

		# Scrape result
		soup = BeautifulSoup(response, "html.parser")
		table = soup.findAll("table", {"id": "shoppingitems"})
		rows = table[0].findAll("tr", {"class": "br"})
		hits = []

		for row in rows :
			cells = row.findAll("td")
			l = len(cells)
			label = cells[0].findAll("div",{"class": "siteListLabel"})[0].text
			status = cells[l-1].text
			non_hc = cells[3].findAll("img", {"alt": "Accessible"})
			if status.startswith( 'available' ) and len(non_hc) == 0:
				hits.append(label)

		if( len(hits) > 0 ):
			hdisplay = ', '.join(hits)
			maplink = "".join([GOOGLE_MAPS, campground.get("latitude"), ",",
												campground.get("longitude")])
			tmp = [url, campground.get("facilityName"), maplink, hdisplay]
			try:
				RESULTs.append(tmp)
			except:
				raise
	return RESULTs

if __name__ == "__main__":
	htmlt = Template(body)
	fname = 'index.html'
	f = open(fname, 'w')
	f.write(head)
	f.close()
	if os.path.isfile('CADesire.xml'):
		tree = ET.parse('CADesire.xml').getroot()
		Campgrounds = tree.findall('.//result')
	else:
		Campgrounds = CADataBaseShower()
	DateLength = [
		("Labor Day", "09/10/2016", "1"), \
		("Memorial Day", "09/24/2016", "2"), \
		]
	for (tag, date, length) in DateLength:
		result = SearchCampground({"date":date, "length":length}, Campgrounds)
		with open(fname, 'a') as f:
			f.write(htmlt.render(header1=tag, lines=result))
	f = open(fname, 'a')
	f.write(tail)
	f.close()
	print("Campgrounds searching is finished.")

	# Email_Alerts = False
	# if Email_Alerts:
	# 	# Send out emails
	# 	server = smtplib.SMTP('smtp.gmail.com', 587)
	# 	server.ehlo()
	# 	server.starttls()
	# 	server.login(SendFrom, Pwd)
	# 	Subject = "".join(["Campground Update for ", date])
	# 	msg = """\
	# 	From: %s
	# 	To: %s
	# 	Subject: %s
	#
	# 	%s
	# 	""" % (SendFrom, ", ".join(SendTo), Subject, RESULTs)
	#
	# 	server.sendmail(SendFrom, SendTo, msg)
	# 	server.close()
	# else:
	# 	print(RESULTs)
