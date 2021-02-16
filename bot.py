#!/usr/bin/env python
# https://api.slack.com/apps

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from datetime import datetime, timedelta

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id'] #get bot id

message_counts = {}

SCHEDULED_MESSAGES = [
	{'text': 'He is a perfect match for you!' , 'post_at': (datetime.now() + timedelta(seconds=20)).timestamp(), 'channel': 'C01MQT7S3PU' },
	{'text': 'The mouse just wandered to the west.' , 'post_at': (datetime.now() + timedelta(seconds=30)).timestamp() , 'channel': 'C01MQT7S3PU'}
]

def list_scheduled_messages(channel):
	response = client.chat_scheduledMessages_list(channel=channel)
	#print(response.data)
	messages = response.data.get('scheduled_messages')
	ids = []
	for msg in messages:
	#	print(msg)
		ids.append(msg.get('id'))

	return ids

def schedule_messages(messages):
    ids = []
    for msg in messages:
        response = client.chat_scheduleMessage(
        	channel=msg['channel'], text=msg['text'], post_at=msg['post_at']).data
        id_ = response.get('scheduled_message_id')
        ids.append(id_)

    return ids

def delete_scheduled_messages(ids, channel):
	for _id in ids:
		try:
			client.chat_deleteScheduledMessage(
				channel=channel, scheduled_message_id=_id)
		except Exception as e:
			print(e)

# Events
@slack_event_adapter.on('message')
def message(payload):
	event = payload.get('event', {})
	channel_id = event.get('channel')
	user_id = event.get('user')
	text = event.get('text')

	if BOT_ID != user_id:
		if user_id in message_counts:
			message_counts[user_id] += 1
		else:
			message_counts[user_id] = 1

		#client.chat_postMessage(channel=channel_id, text="He is a perfect match for you!")

#Slash commands
@app.route('/message-count', methods=['POST'])
def message_count():
	data = request.form
	#print(data)
	user_id = data.get('user_id')
	channel_id = data.get('channel_id')
	message_count = message_counts.get(user_id, 0)
	client.chat_postMessage(channel=channel_id, text=f"Message: {message_count}")

	return Response(), 200

if __name__ == "__main__":
	#schedule_messages(SCHEDULED_MESSAGES)
	#list_scheduled_messages('C01MQT7S3PU')
	#ids = list_scheduled_messages('C01MQT7S3PU')
	#delete_scheduled_messages(ids, 'C01MQT7S3PU')
	app.run(debug=True)
