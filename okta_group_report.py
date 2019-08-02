#!/usr/bin/python
#
# The purpose of this script is to be able to generate a report from an Okta group.
# This script will perform as follows:
#      1. Request a group name from the end user
#      2. Return a list of group Ids that match the group name
#      3. Return a CSV from the group ID that is entered by the user name
# This will create an "okta_group_members.csv" file.
#
# Rory Aptekar
# 08.01.19
# 

import json
import pprint
import csv
import requests
import sys

token = '{token}'
base_url = 'http://{okta_domain}.okta.com/api/v1/'
headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

group_search_text = raw_input("Enter the name of the group to find the group_id: ")

url = base_url + 'groups?q=' + group_search_text
req = requests.get(url, headers=headers)

json_obj = req.json()
for json_row in json_obj:
	group_id = json_row["id"]
	group_name = json_row["profile"]["name"]
	print "Group Name: " + group_name
	print "Group ID: " + group_id

group_selected_id = raw_input("Enter the group id to process for user profile updates: ")

url2 = base_url + 'groups/' + group_selected_id + '/users'
req2 = requests.get(url2, headers=headers)

json_obj2 = req2.json()


with open('okta_group_members.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Full Name','Email Address', 'Status'])
    for json_row in json_obj2:
        fullName = json_row["profile"]["firstName"] + " " + json_row["profile"]["lastName"]
        emailAddress = json_row["profile"]["login"]
        status = json_row["status"]
        filewriter.writerow([fullName, emailAddress, status])
