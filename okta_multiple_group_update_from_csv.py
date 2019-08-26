#!/usr/bin/python
# 
# This script will take a CSV with two columnns, Email and Group Name and
# search Okta for both the group name and the user ID from the email
# referenced in the script. In order to avoid erroneous group additions,
# the group will error and exit if either the email address or the group
# name does not correspond to a user or group.
#
#
# Setup:
# Replace {api_token} with the API token from Okta and ensure the
# base_url is set.
#
# Rory Aptekar
# 2019.08.26
#

import csv
import requests
import sys

token = '{api_token}'
base_url = 'https://{domain}.okta.com/api/v1/'
headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

# Ask user for name of csv file
print("Please make sure your csv file is formatted with two columns, the first column being the email and the second column being the group name. \n")
csv_input = raw_input("Enter the filename of the csv: ")

# Open CSV and append all rows to lists for email and group
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    email_address = []
    group_name = []
    for row in reader:
        email_address.append(row[0])
        group_name.append(row[1])
csvfile.close()

# Remove header row from lists
del email_address[0]
del group_name[0]

# Lookup and store userIds for all users in email array
count = 0
user_ids = []
for i in email_address:
    try:
        url = base_url + 'users/' + str(i)
        req = requests.get(url, headers=headers)
        json_obj = req.json()
        user_ids.append(json_obj["id"])
        count += 1
    except KeyError:
        print("Failed to find user " + email_address[count] + " referenced in the spreadsheet. Quitting script.")
        sys.exit(1)

# Lookup and store groupIds for all groups in group array
count = 0
group_ids = []
for i in group_name:
    url = base_url + 'groups/?q=' + str(i)
    req = requests.get(url, headers=headers)
    json_obj = req.json()
    if json_obj == []:
         print("Failed to find group " + group_name[count] + " referenced in the spreadsheet. Quitting script.")
         sys.exit(1)
    for json_row in json_obj:
        group_ids.append(json_row["id"])
    count += 1

# Add users to respective groups
count = 0
for i in user_ids:
    url = base_url + 'groups/' + str(group_ids[count]) + '/users/' + str(i)
    print("Adding " + email_address[count] + "to the Okta group \"" + group_name[count] + "\"")
    requests.put(url, headers=headers)
    count += 1
