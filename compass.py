from sense_hat import SenseHat
import math

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