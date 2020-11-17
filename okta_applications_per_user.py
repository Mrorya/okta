#!/usr/bin/python
#
# The purpose of this script is to take the user's input of an email address 
# and return the application's currently assigned to him.
#
# Updated for Python3+ 2020.09.2
#

import urllib2
import json
import csv

token = ''
base_url = 'https://{domain}.okta.com/api/v1/'

email = raw_input("Enter the user's email address: ")

url = base_url + '/users?q=' + email

headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

req = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(req)
the_page = response.read()

json_obj = json.loads(the_page)

for json_row in json_obj:
	display_name = json_row["profile"]["displayName"]
	login = json_row["profile"]["login"]
	title = json_row["profile"]["title"]
	okta_id = json_row["id"]
	url2 = base_url + '/users/' + okta_id + '/appLinks'
	new_req = urllib2.Request(url2, headers=headers)
	response = urllib2.urlopen(new_req)
	the_page2 = response.read()
	json_obj2 = json.loads(the_page2)
	apps = ''
	for json_row in json_obj2:
		apps = apps + json_row["label"] + '; '
	print ("Name: " + display_name)
	print ("Login: " + login)
	print ("Title: " + title)
	print ("Apps: " + apps)
