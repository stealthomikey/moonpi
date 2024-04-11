from sense_hat import SenseHat
import math
import RPi.GPIO as GPIO
import time

BuzzerPin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT) 


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
global Buzz

Buzz = GPIO.PWM(BuzzerPin, 4) 
Buzz.start(40) 

C4=262
D4=294
E4=330
F4=349
G4=392
A4=440
B4=494

song = [
  G4,
  E4, F4, G4,
  A4, B4, 
  D4, F4,
  C4
]

beat = [
  4,
  4, 4, 2,
  4, 4,
  2, 1,
  1
]

while True:
	for i in range(1, len(song)): 
		Buzz.ChangeFrequency(song[i]) 
		time.sleep(beat[i]*0.13)