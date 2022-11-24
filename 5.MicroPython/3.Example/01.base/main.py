from machine import Pin, SoftI2C
from time import sleep
from neopixel import NeoPixel
from sht30 import SHT30
from mpu6050 import MPU6050
from bmp280 import BMP280
from bh1750 import BH1750
from math import atan2

print("hello esp32c3")
sleep(1)


############### KEY ###############

sw_boot = Pin(9, Pin.IN, Pin.PULL_UP)
sw_boot.irq(trigger=Pin.IRQ_FALLING, handler=lambda pin: print(pin))

############### RGBLED ###############

rgb = Pin(8, Pin.OUT)
np = NeoPixel(rgb, n=2, bpp=3, timing=1)
np[0] = (2, 2, 2)
np[1] = (2, 2, 2)
np.write()

############### I2C ###############

i2c = SoftI2C(sda=Pin(7), scl=Pin(6), freq=400000)

devs = i2c.scan()

if len(devs) > 0:

    print(devs)

    sht = SHT30(i2c, i2c_address=0x44)
    bh = BH1750(i2c)
    bmp = BMP280(i2c, addr=118)

    sleep(1)

    for i in range(10):
        print("sht", sht.measure())
        print('bh', bh.read())
        print("bmp", bmp.temperature,  bmp.pressure)

        try:
            # 海拔换算公式：H=44300*(1- (P/P0)^(1/5.256))， 海平面压力P0值不固定, 随温度天气地理位置变化
            # http://www.yihuan.org/jishuzhichi/tec-32.html
            # 天津海拔高度3 大气压力10.35mm水柱 (1mmH2O=9806.38Pa) -> 输出 -22, 误差在30m左右
            print("h", 44300 * (1 - (bmp.pressure / (9806.38*10.35))**(1/5.256)))
        except:
            pass

        sleep(0.3)

    mpu = MPU6050(i2c)

    for i in range(50):
        vals = mpu.get_values()
        print({
            "picth": atan2(vals["AcY"], vals["AcZ"]) * 57.3,
            "roll": atan2(vals["AcX"], vals["AcZ"]) * 57.3
        })
        sleep(0.1)

    print("run ok")


else:
    print("can't find i2c dev")
