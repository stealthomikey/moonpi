import RPi.GPIO as GPIO
import time

BuzzerPin = 4
buzRun = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT) 

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

while buzRun == True:
    for i in range(1, len(song)):
        Buzz.ChangeFrequency(song[i])
        time.sleep(beat[i]*0.13)
        print(i)
        if i == 8:
            buzRun = False
print("done")