from machine import Pin
from stepper import Stepper

s = Stepper(Pin(0, Pin.OUT), Pin(2, Pin.OUT), Pin(1, Pin.OUT))
s.power_on()
s.set_step_time(1000)
s.abs_angle(-100)
s.rel_angle(80)
s.abs_angle(0)
