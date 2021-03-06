#!/home/bostonnp/virtualenv/public__html_tap/3.6/bin/python
print("Content-type: text/html")
print()
print("<!DOCTYPE html>")
print("<html><head><meta charset='utf-8'/><link rel='stylesheet' href='styles.css'></head><body>")
import sites
import events
import cgi
import datetime

import cgitb
cgitb.enable()

postData = cgi.FieldStorage()
dateReq = dateReq = datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
siteReq = "all"
DATA = {}

try:
	if "date" in postData:
		dateStrArray = postData['date'].value.split("-")
		dateReq = datetime.datetime(int(dateStrArray[0]),int(dateStrArray[1]),int(dateStrArray[2]))
	if "showDate" in postData and postData['showDate'].value == 'true':
		print("<div class='dateDiv'><h2>" + dateReq.strftime("%A %B %d, %Y") +"</h2></div>")
		print("<div style='height:5em;width:100%'></div>")
	else:
		print('<p style="display:none">' + dateReq.isoformat("T") + '</p>')

	exclusions = {}
	if "exclude" in postData:
		for ex in postData["exclude"].value.split(","):
			exclusions[ex] = True
	inclusions = {}
	if "include" in postData:
		for incl in postData["include"].value.split(","):
			inclusions[incl] = True
	#else:
		#inclusions = False

	if "site" in postData:
		siteReq = postData['site'].value.split(",")
		DATA['sites'] = sites.getData(siteReq,dateReq)['sites']
		keywords = []
		for s in DATA['sites']:
			for k in s['keywords']:
				keywords.append(k)
			for l in s['locations']:
				keywords.append(l)
		if (not "events" in exclusions) and (not inclusions) or ("events" in inclusions):
			DATA['events'] = events.getData(keywords,dateReq)['events']
	else:
		DATA['sites'] = sites.getData(["all"],dateReq)['sites']
		if (not "events" in exclusions) and (not inclusions) or ("events" in inclusions):
			DATA['events'] = events.getData(['all'],dateReq)['events']

	for site in DATA['sites']:
		siteString = "<div class='%s'>" %site['abbr']
		if (not "name" in exclusions) and (not inclusions) or ("name" in inclusions):
			siteString += "<h1 class='name'>" + site['name'] + "</h1>"
		if (not "hours" in exclusions) and (not inclusions) or ("hours" in inclusions):
			siteString += "<div class='hours'><img src='https://www.nps.gov/bost/planyourvisit/images/hours.png'>"
			siteString += "<h3 class='listing'>Today&apos;s hours: " + site["hours"] + "</h3></div>"
		if (site["fees_required"]) and (not "fees" in exclusions) and (not inclusions) or ("fees" in inclusions):
			siteString += "<div class='fees'>"
			if site["fees_required"] == "true":
				siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/fee.png">'
			else:
				if(site["fees_required"] == "false"):
					siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/non-fee.png">'
			siteString += "<ul class='listing'>"
			for fee in site["fees"]:
				siteString += "<li style='list'>%s</li>" % fee
			siteString += "</ul>"	
			siteString += "</div>"
		if len(site["accessibility"]) > 0 and (not "accessibility" in exclusions) and (not inclusions) or ("accessibility" in inclusions):
			for consideration in site["accessibility"]:
				siteString += "<div class='accessibility'>"
				if consideration["accessible"] == "true":
					siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/accessible.png">'
				else:
					if(consideration["accessible"] == "false"):
						siteString += '<img src="https://www.nps.gov/bost/planyourvisit/images/not-accessible.png">'
				siteString += "<span class='listing'>" + consideration["consideration"] + "</span>"
				siteString += "</div>"

		if len(site["websites"]) > 0 and (not "websites" in exclusions) and (not inclusions) or ("websites" in inclusions):
			siteString += "<div class='websites'><img src='https://www.nps.gov/bost/planyourvisit/images/www.png'>"
			siteString += "<ul class='listing'>"
			for website in site["websites"]:
				siteString += "<li><a href='%s' target='_blank'>%s</a></li>" % (website["href"], website["text"])
			siteString += "</ul>"
			siteString += "</div>"
		if "events" in DATA and ((not "events" in exclusions) and (not inclusions) or ("events" in inclusions)):
			eventString = ''
			for event in DATA['events']:
				if event['location'] in site['keywords'] or event['location'] in site['locations']:
					eventString += "<div class='event'>"
					eventString += "<h3 class='event_title'>%s</h3>" %event['title'].encode('utf-8')
					eventString += "<div class='event_location'>%s</div>" %event['location'].encode('utf-8')
					eventString += "<div class='event_time'><span class='event_start'>%(formattedStartTime)s</span><span class='event_end'>%(formattedEndTime)s</span></div>" %{'formattedStartTime':event['formattedStartTime'].encode('utf-8'),'formattedEndTime':event['formattedEndTime'].encode('utf-8')}
					eventString += "<div class='event_description'>" + str(event['content'].encode('utf-8')) + "</div>"
					eventString += "</div>"
			if len(eventString) > 0:
				siteString += "<div class='events'>"
				if not(len(inclusions) == 1 and "events" in inclusions):
					siteString += "<h2>Events:</h2>"
				siteString += eventString 
				siteString += "</div>"
			if eventString == '' and "noEmpty" in postData and postData['noEmpty'].value == 'true':
				continue
		siteString += "</div>"
		if "separator" in postData:
			siteString += postData['separator'].value
		print(siteString)
except (IndexError,ValueError):
	print("<h1>Error: Invalid date.</h1>")
print("</body></html>")
