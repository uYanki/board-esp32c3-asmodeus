from machine import Pin, I2C
import utime
from ssd1306 import SSD1306_I2C
from mpu6050 import MPU6050


i2c = I2C(0, sda=Pin(7), scl=Pin(6), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
imu = MPU6050(i2c)

BLOCK_SIZE = 6
AREA_SIZE = 48
AREA_X = 80
AREA_Y = 8
MOVE_SPAN = AREA_SIZE-BLOCK_SIZE

while True:
    v = imu.get_values()
    acX = v['AcX']/16384.0
    acY = v['AcY']/16384.0
    acZ = v['AcZ']/16384.0
    coorY = int((acX+1)*0.5*MOVE_SPAN)
    coorX = int((acY+1)*0.5*MOVE_SPAN)
    # 清空屏幕
    oled.fill(0)
    oled.text("acX:"+str(acX)[0:4]+"g", 0, 5)
    oled.text("acY:"+str(acY)[0:4]+"g", 0, 20)
    oled.text("acZ:"+str(acZ)[0:4]+"g", 0, 35)
    oled.rect(80, 8, 48, 48, 1)
    oled.fill_rect(AREA_X+coorX, AREA_Y+coorY, BLOCK_SIZE, BLOCK_SIZE, 1)
    oled.show()
    utime.sleep(0.05)
