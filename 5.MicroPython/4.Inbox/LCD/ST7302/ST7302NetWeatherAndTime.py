import network
import utime
from machine import Pin, SPI
import machine
import FileUtil as fu
import ST7302
import NetUtil
from WeatherUtil import getAndShowWeatherInfo
from TimeUtil import getAndShowTimeInfo

# 创建服务于ST7302的SPI对象
spi = SPI(1, baudrate=10000000, sck=Pin(25), mosi=Pin(26), polarity=0, phase=0)
# ST7302 DC对应的GPIO
dc_pin = Pin(27, Pin.OUT)
# ST7302 RESET对应的GPIO
rest_pin = Pin(14, Pin.OUT, Pin.PULL_UP)
# 创建ST7302屏幕显示对象
screen = ST7302.ST7302(spi, dc_pin, rest_pin, 250, 122)

# 加载字库图集
fonts = fu.loadPics("weather-time.bnbapic")

# 连接无线网
NetUtil.initNetConnection(screen, fonts)
# 休眠2000ms，便于看清联网信息
utime.sleep(2.0)
# 获取并显示天气信息
getAndShowWeatherInfo(screen, fonts)
# 不断循环获取时间信息并显示
while True:
    # 获取时间信息并显示
    getAndShowTimeInfo(screen, fonts)
    # 屏幕反色
    screen.inv_on()
    # 刷新画面
    screen.flush_buffer()
