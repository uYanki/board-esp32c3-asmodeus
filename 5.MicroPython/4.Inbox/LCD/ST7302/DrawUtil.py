# 获取文本内容对应自定义字库索引列表的方法
def getCharIndex(nrStr):
    srcStr = "0123456789雨暴大雪到-中:小阵尘沙连气：接风雷特指有成向云北错多力东功度级质天温.地°冰阴伴夹强冻霾址I重前量P当南扬浮数晴雹出空雾西."
    result = []
    for i in range(len(nrStr)):
        currChar = nrStr[i]
        currIndex = 0
        for cTemp in srcStr:
            if (cTemp == currChar):
                result.append(currIndex)
                break
            currIndex = currIndex+1
    return result

# 在屏幕上显示指定字符串的方法
# 参数依次为
# 屏幕显示对象、字库图、内容索引序列、X方向步进、Y方向步进、X起始位置、Y起始位置
def showString(screen, fonts, indexList, xSpan, ySpan, startX, startY):
    count = len(indexList)
    for i in range(count):
        screen.blit(fonts[indexList[i]].fbuf, 50+startX+i*xSpan, 20+startY+i*ySpan)


# 绘制边框
def drawBorder(screen):
    screen.rect(5, 5, 240, 112, 0)
    screen.rect(10, 10, 230, 102, 0)
