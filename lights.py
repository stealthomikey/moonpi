import RPi.GPIO as GPIO
import time

readPIN = 23

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(readPIN,GPIO.IN)
GPIO.setwarnings(True)

try:
    while True:
        print("read" + str(GPIO.input(readPIN)) + "", end='\r')
        time.sleep(1)
except KeyboardInterrupt:
        print('interrupted')
        GPIO.cleanup()