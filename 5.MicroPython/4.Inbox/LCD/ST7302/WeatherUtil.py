from DrawUtil import showString, getCharIndex, drawBorder
import ujson
import urequests

# 从天气预报JSON字符串中提取
# 天气情况、温度、风向、风力、空气指数的方法


def getWeaInfoFromJSONStr(jsonStr):
    jo = ujson.loads(jsonStr)
    return (jo["wea"], jo["tem"], jo["win"], jo["win_speed"], jo["air"])

# 获取并显示天气信息


def getAndShowWeatherInfo(screen, fonts):
    # 北京的天气
    response = urequests.get("https://www.tianqiapi.com/free/day?appid=44164882&appsecret=gdbO1VkB&city=%E5%8C%97%E4%BA%AC")
    jsonStr = response.text
    # jsonStr='{"cityid":"101020100","city":"上海","update_time":"15:28","wea":"多云","wea_img":"yun","tem":"17","tem_day":"8","tem_night":"6","win":"东北风","win_speed":"2级","win_meter":"6km\/h","air":"32"}'
    response.close()
    # 从网络获取的JSON字符串中解析出所需内容
    tqData = getWeaInfoFromJSONStr(jsonStr)

    # 清除屏幕
    screen.fill(1)
    # 绘制边框
    drawBorder(screen)
    # 绘制"天气："
    showString(screen, fonts, [43, 23, 24], 16, 0, 23, 0-7)
    # 绘制天气内容
    indexList = getCharIndex(tqData[0])
    showString(screen, fonts, indexList, 16, 0, 71, 0-7)
    # 绘制"温度："
    showString(screen, fonts, [44, 40, 24], 16, 0, 23, 16-7)
    # 绘制温度内容
    indexList = getCharIndex(tqData[1])
    # 度符号“°”
    indexList.append(47)
    showString(screen, fonts, indexList, 8, 0, 71, 16-7)
    # 绘制风向内容
    indexList = getCharIndex(tqData[2])
    showString(screen, fonts, indexList, 16, 0, 23, 32-7)
    # 绘制风力内容
    indexList = getCharIndex(tqData[3])
    showString(screen, fonts, indexList, 16, 0, 16*len(tqData[2])+31, 32-7)
    # 绘制"空气质量："
    showString(screen, fonts, [69, 23, 42, 59, 24], 16, 0, 23, 48-7)
    # 绘制空气质量指数值
    indexList = getCharIndex(tqData[4])
    showString(screen, fonts, indexList, 8, 0, 103, 48-7)
