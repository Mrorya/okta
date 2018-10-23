#!/usr/bin/python
#
# This script will run an import of all Okta groups and export 
# the application assignment, group type, and notes
# into a csv file
#


import urllib2
import json
import csv
import re

token = '[REDACTED]'
url = '[INSERT]/api/v1/groups'

headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

req = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(req)
the_page = response.read()

json_obj = json.loads(the_page)

def remove_unicode(string_data):
    if string_data is None:
        return string_data

    if isinstance(string_data, str):
        string_data = str(string_data.decode('ascii', 'ignore'))
    else:
        string_data = string_data.encode('ascii', 'ignore')

    remove_ctrl_chars_regex = re.compile(r'[^\x20-\x7e]')

    return remove_ctrl_chars_regex.sub('', string_data)

with open('okta_group_export.csv', 'wb') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	filewriter.writerow(['groupId', 'groupName', 'groupType', 'Description', 'Apps'])
	for json_row in json_obj:
		groupId = json_row["id"]
		groupName = remove_unicode(json_row["profile"]["name"]).replace(',', ' ')
		groupType = json_row["type"]
		if json_row["profile"]["description"]:
			description = remove_unicode(json_row["profile"]["description"]).replace(',', ' ')
		else:
			description = 'None'
		apps_url = json_row["_links"]["apps"]["href"]
		new_req = urllib2.Request(apps_url, headers=headers)
		response = urllib2.urlopen(new_req)
		the_page2 = response.read()
		json_obj2= json.loads(the_page2)
		apps = ''
		for json_row in json_obj2:
			apps = apps + json_row["label"] + '; '
		filewriter.writerow([groupId, groupName, groupType, description, apps])
