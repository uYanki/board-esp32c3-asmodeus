from machine import I2C, Pin
from as5600 import AS5600
from time import sleep

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
z = AS5600(i2c, 0x36)
print(z.scan())
while True:
    # print(z.magnet_status())
    print('ZANGLE', z.RAWANGLE)
    # print('ANGLE', z.ANGLE)
    # print('Magnet detected', z.MD)
    sleep(0.1)
