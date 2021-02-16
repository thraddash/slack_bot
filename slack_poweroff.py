#!/usr/bin/env python
# https://api.slack.com/apps

import slack
import os
import json
from slack.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
client2 = slack.WebClient(token=os.environ['TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id'] #get bot id
USER_ID = os.environ['USER_ID']


# get members
def getMembers():
    try:
        response = client.users_list()
        users = response["members"]
        for index, item in enumerate(users):
            print(index, users[index]['id'], users[index]['real_name'])

        '''
        users = response["members"]
        i = 0
        while i < len(users):
            print(users[i]['id'], users[i]['real_name'])
            i += 1
        '''

    except SlackApiError as e:
        assert e.response["error"]

def userInfo():
    try: 
        response = client.users_list()
        users = response["members"]
        for index, item in enumerate(users):
            if (users[index]['id'] == USER_ID) and (users[index]['profile']['status_text'] == "off"):
                print(f"found name: {users[index]['profile']['real_name']}, text_status: {users[index]['profile']['status_text']}")
    except SlackApiError as e:
        assert e.response["error"]

# Get user profile .env USER_ID

def getProfile():
    try:
        response = client.users_profile_get(
            user=USER_ID
        )
        user = response["profile"]
        if (user['status_text'] == ""):
            print(f"status_text: none")
        elif (user['status_text'] == "off"):
            print(user['status_text'])
            setProfile()
            os.system('shutdown -s')
		
    except SlackApiError as e:
        assert e.response["error"]

def setProfile():
    response = client2.users_profile_set(
        user=USER_ID,
        profile={
            "status_text": "",
            "status_emoji": ""
        }
    )


if __name__ == "__main__":
	#getMembers()
    #userInfo()
    getProfile()
