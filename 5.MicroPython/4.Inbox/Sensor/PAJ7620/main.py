from machine import Pin, I2C, SoftI2C
from gesture import Gesture
import time


i2c = I2C(0, scl=Pin(26), sda=Pin(25), freq=100000)
g = Gesture(i2c)

msgR = ["", "Forward", "Backward", "Right", "Left", "Up", "Down", "Clockwise", "anti-clockwise", "Wave"]

while True:
    value = g.return_gesture()
    if value != 0:
        print(value, msgR[value])
    time.sleep(0.08)
