#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Psychokiller1888

import json
import os.path
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import pytoml
import signal
import snowboydecoder
import sys

SNIPS_CONFIG_PATH = '/etc/snips.toml'
HOTWORD_ID = 'default'

interrupted = False
siteId = 'default'
mqttServer = '127.0.0.1'
mqttPort = 1883
model = ''
sensitivity = 0.5

mqtt_client = mqtt.Client()

def loadConfigs():
	global mqttServer, mqttPort, siteId

	if os.path.isfile(SNIPS_CONFIG_PATH):
		with open(SNIPS_CONFIG_PATH) as confFile:
			configs = pytoml.load(confFile)
			if 'mqtt' in configs['snips-common']:
				if ':' in configs['snips-common']['mqtt']:
					mqttServer = configs['snips-common']['mqtt'].split(':')[0]
					mqttPort = int(configs['snips-common']['mqtt'].split(':')[1])
				elif '@' in configs['snips-common']['mqtt']:
					mqttServer = configs['snips-common']['mqtt'].split('@')[0]
					mqttPort = int(configs['snips-common']['mqtt'].split('@')[1])
			if 'bind' in configs['snips-audio-server']:
				if ':' in configs['snips-audio-server']['bind']:
					siteId = configs['snips-audio-server']['bind'].split(':')[0]
				elif '@' in configs['snips-audio-server']['bind']:
					siteId = configs['snips-audio-server']['bind'].split('@')[0]
	else:
		print('Snips configs not found')

def signal_handler(signal, frame):
	global interrupted
	interrupted = True

def interrupt_callback():
	global interrupted
	return interrupted

def onHotword():
	global mqttServer, mqttPort, siteId
	publish.single('hermes/hotword/{0}/detected'.format(HOTWORD_ID), payload=json.dumps({'siteId': siteId}), hostname=mqttServer, port=1883)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
	try:
		model = sys.argv[1]
		sensitivity = float(sys.argv[2])
	except IndexError:
		print('Please provide model name and sensitivity as argument')
		sys.exit()

	if not os.path.isfile('{}.pmdl'.format(model)):
		print('The specified model doesn\'t exist')
		sys.exit()

	if sensitivity < 0 or sensitivity > 1:
		print('Sensitivity should by a float between 0 and 1')
		sys.exit()

	loadConfigs()
	detector = snowboydecoder.HotwordDetector('{}.pmdl'.format(model), sensitivity=sensitivity)
	print('Listening...')
	detector.start(detected_callback=onHotword, interrupt_check=interrupt_callback, sleep_time=0.03)
	detector.terminate()
