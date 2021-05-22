from slackeventsapi import SlackEventAdapter
from slack import WebClient
import os
import slack_config

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = slack_config.SIGNING_SECRET
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = slack_config.BOT_TOKEN
slack_client = WebClient(slack_bot_token)


@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and "test.url.com" in message.get('text'):
        channel = message["channel"]
        thread_ts = message.get("ts")
        #message = "Hello <@%s>! :tada:" % message["user"]
        message = "If you had a question regarding a ticket, please leave a comment in the ticket itself. It's the best way for us to track the issue and respond in a timely manner."
        slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=message)


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.chat_postMessage(channel=channel, text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=8080)
