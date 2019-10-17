#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
import RPi.GPIO as GPIO
import threading
import time
import paho.mqtt.client as mqtt

LED_PIN = 17
MQTTServerIP = "localhost"
MQTTServerPort = 1883 #port
MQTTTopicName = "home/alert" #TOPIC name

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.LOW)
 
app = Flask(__name__)
passphrase = (u'芝麻開門')
handler = WebhookHandler('xxxxxxxxxx')
to_group_id = ('xxxxxxxxxx')



@app.route("/", methods=['POST'])
def index():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'
 
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text==passphrase and event.source.group_id==to_group_id:
        mqttc = mqtt.Client("python_pub")
        mqttc.connect(MQTTServerIP, MQTTServerPort)
        if GPIO.input(LED_PIN)==0:
            GPIO.output(LED_PIN, GPIO.HIGH)
            mqttc.publish(MQTTTopicName, 'Unlock')
            lock_thread = threading.Thread(target = unlock)
            lock_thread.start()
        else:
            mqttc.publish(MQTTTopicName, 'Already Unlocked')

def unlock():
    time.sleep(10)
    GPIO.output(LED_PIN, GPIO.LOW)
    mqttc = mqtt.Client("python_pub")
    mqttc.connect(MQTTServerIP, MQTTServerPort)
    mqttc.publish(MQTTTopicName, 'Lock')
		
		
if __name__ == "__main__":
    app.run(host='127.0.0.1', port= 80)