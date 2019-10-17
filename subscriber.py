#!/usr/bin/python
# -*- coding: UTF-8 -*-
import paho.mqtt.client as mqtt
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi('xxxxxxxxxx')
to_group_id = ('xxxxxxxxxx')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("home/alert")

def on_message(client, userdata, msg):
    msg.payload = str(msg.payload, encoding = "utf-8")
    if msg.payload == ('Unlock'):
        line_bot_api.push_message(to_group_id, TextSendMessage(u'解鎖'))
    elif msg.payload == ('Lock'):
        line_bot_api.push_message(to_group_id, TextSendMessage(u'上鎖'))
    elif msg.payload == ('Alert!'):
	    line_bot_api.push_message(to_group_id, TextSendMessage(u'遭受入侵'))
    else:
        line_bot_api.push_message(to_group_id, TextSendMessage(u'已經解鎖'))
		
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
