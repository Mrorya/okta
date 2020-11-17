#!/usr/bin/python
#
# This script will take a CSV file containing a list of group names
# and descriptions and create Okta groups based on that spreadsheet.
# 
#
# Rory Aptekar
# 2019.08.13
#
# Updated for Python3+ 2020.09.2
#

import csv
import requests

# Set Okta api token and base URL
token = '$TOKEN'
base_url = 'https://$DOMAIN.okta.com/api/v1/'
headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

# Ask user for name of csv file
print("This script is expecting a CSV with two columns: Name, Description. \n")
csv_input = raw_input("Enter the filename of the csv: ")

# Open Groups CSV and append all rows to two lists for name and description
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    group_name = []
    group_description = []
    for row in reader:
        group_name.append(row[0])
        try:
            group_description.append(row[1])
        except IndexError:
            group_description.append('')
csvfile.close()

# Create Okta groups from names and descriptions above
count = 0
for i in group_name:
    url = base_url + 'groups/'
    data = '{ "profile": { "name": "' + group_name[count] + '", "description": "' + group_description[count] + '" } }'
    print("Creating Okta Group \"" + group_name[count] + "\"")
    requests.post(url, data=data, headers=headers)  
    count += 1
