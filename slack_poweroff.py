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

def powerOff():
    try: 
        response = client.users_list()
        users = response["members"]
        for index, item in enumerate(users):
            if (users[index]['id'] == USER_ID) and (users[index]['profile']['status_text'] == "off"):
                print(f"found name: {users[index]['profile']['real_name']}, text_status: {users[index]['profile']['status_text']}")
                os.system('shutdown -s')
    except SlackApiError as e:
        assert e.response["error"]


if __name__ == "__main__":
	#getMembers()
    #getStatus()
