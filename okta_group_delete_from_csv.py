#!/usr/bin/python
# 
# This script will take a CSV file containing a list of email
# addresses and remove them from an Okta group specified in the list.
# If any email addreses do not correspond to Okta user accounts
# those email addresses will output to another csv file
# "emails_not_found.csv" in the same directory as the script.
#
# Setup:
# Replace {api_token} with the API token from Okta and ensure the
# base_url is set.
#
# Rory Aptekar
# 2019.08.06
#

import csv
import requests

token = '{api_token}'
base_url = 'https://{subdomain}.okta.com/api/v1/'
headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

# Ask user for name of csv file
print("Please make sure your csv file is formatted to only contain one column of email addresses and no additional data. \n")
csv_input = raw_input("Enter the filename of the csv: ")

# Ask user for group name
group_search_text = raw_input("Enter the name of the group to find the group_id: ")

url = base_url + 'groups?q=' + group_search_text
req = requests.get(url, headers=headers)

# List Group Names + associated group ID based on search
json_obj = req.json()
for json_row in json_obj:
	group_id = json_row["id"]
	group_name = json_row["profile"]["name"]
	print "Group Name: " + group_name
	print "Group ID: " + group_id

# Ask user for group ID copied from above
group_selected_id = raw_input("Enter the group id to process for user profile updates: ")

# Store Group Name from Group Selected ID
url = base_url + 'groups/' + group_selected_id
req = requests.get(url, headers=headers)
json_obj = req.json()
group_selected_name = json_obj["profile"]["name"]

email_address = []

# Open Email CSV and append all rows to array for emailAddress
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        email_address.append(row)
csvfile.close()

user_ids = []
users_not_found = []

# Lookup and store userIds for all users in email array
for i in email_address:
    try:
        url = base_url + 'users/' + str(i[0])
        req = requests.get(url, headers=headers)
        json_obj = req.json()
        user_ids.append(json_obj["id"])
    except KeyError:
        users_not_found.append(i)
        pass

# Write list of users not found to csv file
if users_not_found != []:
    print('Some emails were not found in Okta. Creating export emails_not_found.csv')
    with open('emails_not_found.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['emailAddress'])
        for i in users_not_found:
            filewriter.writerow([i[0]])

# Add users to group
count = 0
for i in user_ids:
    url = base_url + 'groups/' + group_selected_id + '/users/' + str(i)
    print("Removing " + email_address[count][0] + " from the Okta group \"" + group_selected_name + "\"")
    requests.delete(url, headers=headers)
    count += 1
