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

TRIG = 14
ECHO = 15
ALARM_PIN = 3
LED_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(ALARM_PIN, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(ALARM_PIN, GPIO.LOW)

MQTTServerIP = "localhost"
MQTTServerPort = 1883 #port
MQTTTopicName = "home/alert" #TOPIC name

def get_distance():

    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO)==0:
        start = time.time()
    while GPIO.input(ECHO)==1:
        end = time.time()

    return (end - start) * 17000

while True:
    GPIO.output(ALARM_PIN, GPIO.LOW)
    if get_distance() < 20 and GPIO.input(LED_PIN)==0:
        GPIO.output(ALARM_PIN, GPIO.HIGH)
        mqttc = mqtt.Client("python_pub")
        mqttc.connect(MQTTServerIP, MQTTServerPort)
        mqttc.publish(MQTTTopicName, "Alert!")
        time.sleep(2)