#!/usr/bin/python
# 
# Someday add some better description - delete users from AD
#
#

import csv
import requests

token = '{token}'
base_url = 'https://{domain}/api/v1/'
headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

# Ask user for name of csv file
print("Please make sure your csv file is formatted to only contain one column of email addresses and no additional data. \n")
csv_input = input("Enter the filename of the csv: ")

email_address = []

# Open Email CSV and append all rows to array for emailAddress
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        email_address.append(row)
csvfile.close()

app_selected_id = '{some_attribute}'

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
    with open('emails_not_found.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['emailAddress'])
        for i in users_not_found:
            filewriter.writerow([i[0]])

# Delete users from AD
count = 0
for i in user_ids:
    url = base_url + 'apps/' + app_selected_id '/users/' + str(i)
    print("Deleting " + email_address[count][0] + " from AD integration \"" + app_selected_id + "\"")
    requests.delete(url, headers=headers)
    count += 1