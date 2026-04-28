from m5stack import *
from m5ui import *
from uiflow import *
import time


setScreenColor(0x222222)

vitesse = None

BikeDashboard = M5TextBox(29, 22, "Bike Dashboard", lcd.FONT_DejaVu24, 0x4d879e, rotate=0)
speed = M5TextBox(29, 84, "0", lcd.FONT_DejaVu72, 0x47d0db, rotate=0)
unit = M5TextBox(124, 126, "km/h", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)

from numbers import Number

while True:
  vitesse = (vitesse if isinstance(vitesse, Number) else 0) + 1
  speed.setText(str(vitesse))
  wait(1)
  wait_ms(2)

