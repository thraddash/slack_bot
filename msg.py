#!/usr/bin/env python
# https://api.slack.com/apps

import slack
import os
from slack.errors import SlackApiError
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id'] #get bot id

def bot_chat():
	try:
		response = client.chat_postMessage(
			channel="#python-bot",
			text="test2 :tada:"
		)
	except SlackApiError as e:
		assert e.response["error"]

if __name__ == "__main__":
	bot_chat()
