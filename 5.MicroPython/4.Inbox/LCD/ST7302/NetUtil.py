import network
import utime
from DrawUtil import showString, getCharIndex, drawBorder

# 连接无线网并显示对应信息


def initNetConnection(screen, fonts):
    station = network.WLAN(network.STA_IF)
    while (not station.isconnected()):
        station.active(True)
        try:
            station.connect("wyf001", "1a2b3c4d5e6fabc")
            # 清除屏幕
            screen.fill(1)
            # 绘制边框
            drawBorder(screen)
            # 绘制"连接中..."
            showString(screen, fonts, [22, 25, 16, 45, 45, 45], 16, 0, 25, 30)
            # 屏幕反色
            screen.inv_on()
            # 刷新画面
            screen.flush_buffer()
            utime.sleep(2.0)
        except OSError:
            # 清除屏幕
            screen.fill(1)
            # 绘制边框
            drawBorder(screen)
            # 绘制"出错重连..."
            showString(screen, fonts, [68, 35, 57, 22, 45, 45, 45], 16, 0, 25, 30)
            # 屏幕反色
            screen.inv_on()
            # 刷新画面
            screen.flush_buffer()
            utime.sleep(2.0)

    # 清除屏幕
    screen.fill(1)
    # 绘制边框
    drawBorder(screen)
    # 绘制"连接成功"
    showString(screen, fonts, [22, 25, 31, 39], 16, 0, 25, 14)
    # 绘制"IP地址:"
    showString(screen, fonts, [56, 60, 46, 55, 17,], 16, 0, 25, 30)
    # 绘制IP地址值
    indexList = getCharIndex(str(station.ifconfig()[0]))
    showString(screen, fonts, indexList, 8, 0, 25, 46)
    # 屏幕反色
    screen.inv_on()
    # 刷新画面
    screen.flush_buffer()
