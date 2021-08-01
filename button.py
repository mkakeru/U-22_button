import RPi.GPIO as GPIO
import time
PNO23 = 23
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(PNO23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
try:
  while True:
    sw = GPIO.input(PNO23)
    if(sw == GPIO.LOW):
      print("switch on!")
    else:
      print(".")
    time.sleep(0.5)
except KeyboardInterrupt:
  pass
GPIO.cleanup()