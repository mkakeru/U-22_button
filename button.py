import os
from os.path import join, dirname
from dotenv import load_dotenv
import RPi.GPIO as GPIO
import time
from websocket import create_connection
import geocoder

PNO23 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CONNECTION_URI = os.environ.get("CONNECTION_URI")

UID = os.environ.get("UID")

ws = create_connection(CONNECTION_URI)
ws.send(r'{"command": "subscribe","identifier": "{\"channel\": \"HelpButtonChannel\"}"}')
result =  ws.recv()
print("received '%s'" % result)

try:
  while True:
    sw = GPIO.input(PNO23)
    if(sw == GPIO.LOW):
      print("Switch on!")
      g = geocoder.ip('me')
      print("current location: '%s'" % g.latlng)
      lat = g.lat
      lng = g.lng
      ws.send(r'{"command": "message","identifier": "{\"channel\": \"HelpButtonChannel\"}", "data":"{\"action\": \"sendToHelper\", \"status\":\"SUCCESS\", \"message\":\"Sent a help message from Help button\", \"uid\":\"%s\", \"lat\":\"%f\", \"lng\":\"%f\"}"}' % (UID, lat, lng))
      print("Sent")
    else:
      print(".")
    time.sleep(0.5)
except KeyboardInterrupt:
  pass
GPIO.cleanup()