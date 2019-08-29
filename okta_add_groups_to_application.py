#!/usr/bin/python
#
# The purpose of this script is to be able to iterate through a csv list of group names
# and add those groups to a specified application. This allows an IT team to easily add
# a large number of groups via CLI to an application in Okta.
#
# Be sure to setup the API token and the Base URL in the script prior to running.
#
# Rory Aptekar
# 2019.08.29
#

import csv
import requests
import sys

token = '{api_token}'
base_url = 'https://{subdomain}.okta.com/api/v1/'
headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

# Ask user for name of csv file
print("Please make sure your csv file is formatted with one column, consisting of the list of groups you would like to add.\n")
csv_input = raw_input("Enter the filename of the csv: ")

# Open Groups CSV and append all rows to array for group_names
group_names = []
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        group_names.append(row)
csvfile.close()

# Remove header row from list
del group_names[0]

# Lookup and store groupIds for all groups in group array
count = 0
group_ids = []
for i in group_names:
    url = base_url + 'groups/?q=' + str(i[0])
    req = requests.get(url, headers=headers)
    json_obj = req.json()
    if json_obj == []:
        print("Failed to find group " + str(group_names[count]) + " referenced in the spreadsheet. Quitting script.")
        sys.exit(1)
    for json_row in json_obj:
        group_ids.append(json_row["id"])
    count += 1

# Store group name from group IDs
count = 0
group_selected_name = []
for i in group_ids:
    url = base_url + '/groups/' + group_ids[count]
    req = requests.get(url, headers=headers)
    json_obj = req.json()
    group_selected_name.append(json_obj["profile"]["name"])
    count += 1

# Request the application name to search for from the user
app_search_text = raw_input("Enter the name of the application to find the application id: ")

# Execute search on Okta
url = base_url + 'apps?q=' + app_search_text
req = requests.get(url, headers=headers)
json_obj = req.json()
for json_row in json_obj:
    app_id = json_row["id"]
    app_name = json_row["label"]
    print "App Name: " + app_name
    print "App ID: " + app_id

# Ask user for the app ID to execute the group assignment on
app_selected_id = raw_input("Enter the application id to process for group assignment updates: ")

count = 0
for i in group_ids:
    url = base_url + '/apps/' + app_selected_id + '/groups/' + i
    print ("Adding " + group_selected_name[count] + " to the application.")
    req = requests.put(url, headers=headers)
    count += 1
