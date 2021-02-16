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
BOT_ID = client.api_call("auth.test")['user_id'] #get bot id
USER_ID = os.environ['USER_ID']

def bot_chat():
	try:
		response = client.chat_postMessage(
			channel="#python-bot",
			text="test2 :tada:"
		)
	except SlackApiError as e:
		assert e.response["error"]

def emphemeral_chat():
	try:
		response = client.chat_postEphemeral(
			channel="#python-bot",
			text="Happy Birthday! :tada:",
            user=USER_ID
		)
	except SlackApiError as e:
		assert e.response["error"]

# list channels
def getChannels():
	try:
		response = client.conversations_list()
		channels = response["channels"]
		list_channels = list(map(lambda x: x["name"], channels))
		print(list_channels)
	except SlackApiError as e:
		assert e.response["error"]

# get members
def getMembers():
    try:
        response = client.users_list()
        users = response["members"]
        for index, item in enumerate(users):
            print(index, users[index]['id'], users[index]['real_name'])
            #print(index, users[index]['id'], users[index]['profile']['display_name'], users[index]['real_name'])

        '''
        users = response["members"]
        i = 0
        while i < len(users):
            print(users[i]['id'], users[i]['real_name'])
            i += 1
        '''

    except SlackApiError as e:
        assert e.response["error"]

def getStatus():
    try: 
        response = client.users_list()
        users = response["members"]
        for index, item in enumerate(users):
            if (users[index]['id'] == USER_ID) and (users[index]['profile']['status_text'] == "off"):
                print(f"found name: {users[index]['profile']['real_name']}, text_status: {users[index]['profile']['status_text']}")
    except SlackApiError as e:
        assert e.response["error"]


if __name__ == "__main__":
	#bot_chat()
    #emphemeral_chat()
    #getChannels()
	getMembers()
    #getStatus()
