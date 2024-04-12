from sense_hat import SenseHat
import math
import RPi.GPIO as GPIO
import time
from time import sleep

BUZZER = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT) 

def buzz(noteFreq, duration):
    halveWaveTime = 1 / (noteFreq * 2 )
    waves = int(duration * noteFreq)
    for i in range(waves):
       GPIO.output(BUZZER, True)
       time.sleep(halveWaveTime)
       GPIO.output(BUZZER, False)
       time.sleep(halveWaveTime)
def play():
    t=0
    notes=[262,294,330,262]
    duration=[0.5,0.5,0.5,0.5]
    for n in notes:
        buzz(n, duration[t])
        time.sleep(duration[t] *0.1)
        t+=1

field_strength = 0
sense = SenseHat()
while  field_strength < 130:
  raw = sense.get_compass_raw()
  x = raw["x"]
  y = raw["y"]
  z = raw["z"]

  field_strength =  math.sqrt((x*x)+(y*y)+(z*z))# TODO - calculate the magnetic field

  #print(field_strength)
  print("Door shut")
  
else:
    print("Door open")
play()