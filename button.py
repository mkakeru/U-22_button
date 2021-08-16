import os
from os.path import join, dirname
from dotenv import load_dotenv
import RPi.GPIO as GPIO
import time
from websocket import create_connection

PNO23 = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CONNECTION_URI = os.environ.get("CONNECTION_URI")

ws = create_connection(CONNECTION_URI)
ws.send(r'{"command": "subscribe","identifier": "{\"channel\": \"HelpButtonChannel\"}"}')
result =  ws.recv()
print("First received '%s'" % result)

try:
  while True:
    sw = GPIO.input(PNO23)
    if(sw == GPIO.LOW):
      print("Switch on!")
      ws.send(r'{"command": "message","identifier": "{\"channel\": \"HelpButtonChannel\"}", "data":"{\"action\": \"sendToHelper\", \"message\":\"テスト！\"}"}')
      print("Sent")
    else:
      print(".")
    time.sleep(0.5)
except KeyboardInterrupt:
  pass
GPIO.cleanup()