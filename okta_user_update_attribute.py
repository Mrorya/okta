#!/usr/bin/python
#
# Update specific user profile data from a targeted group
#
#

import json
import pprint
import requests
import sys

token = '{api_token}'
base_url = 'https://{domain}/api/v1/'
headers = {'Authorization' : 'SSWS ' + token,
          'Accept' : 'application/json',
          'Content-Type' : 'application/json' }

group_search_text = input("Enter the name of the group to find the group_id: ")

url = base_url + 'groups?q=' + group_search_text
req = requests.get(url, headers=headers)

json_obj = req.json()
for json_row in json_obj:
	group_id = json_row["id"]
	group_name = json_row["profile"]["name"]
	print ("Group Name: " + group_name)
	print ("Group ID: " + group_id)

group_selected_id = input("Enter the group id to process for user profile updates: ")

url2 = base_url + 'groups/' + group_selected_id + '/users'
req2 = requests.get(url2, headers=headers)

def ask_user():
    check = str(input("Are you sure you want to update all users in the group " + group_name + " ? (Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
        	sys.exit(1)
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()

ask_user()

json_obj2 = req2.json()
for json_row in json_obj2:
    user_id = json_row["id"]
    first_name = json_row["profile"]["firstName"]
    last_name = json_row["profile"]["lastName"]
    payload_dict = {"profile":{"division":""}}
    url3 = base_url + 'users/' + user_id
    requests.post(url3, data=json.dumps(payload_dict), headers=headers)
    print("Updated " + first_name + " " + last_name + "'s division to blank")