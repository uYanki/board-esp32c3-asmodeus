import os
from framebuf import FrameBuffer
import framebuf
import gc

# 读文本文件返回字符串


def readTxtFile(fname):
    msgFile = open(fname, "r")
    strData = msgFile.read()
    return strData

# 将四个字节组装为整数的方法


def readInt(bytesArray, start):
    result = bytesArray[start]+(bytesArray[start+1] << 8)+(bytesArray[start+2] << 16)+(bytesArray[start+3] << 24)
    return result

# 加载自定义格式地图文件的方法
# 此格式地图文件最开始四个字节为地图宽度方向格子数
# 接着四个字节为地图高度格子数


def loadMap(fname):
    msgFile = open(fname, "rb")
    strData = msgFile.read()
    # 首先读出四个字节组装为地图宽度
    width = readInt(strData, 0)
    # 接着读出四个字节组装为地图高度
    height = readInt(strData, 4)
    # 接着读出四个字节组装为地图格子尺寸
    span = readInt(strData, 8)
    # 地图数据列表
    mapData = []
    # 接着循环读出每行每列每个格子的数据
    for i in range(height):
        rowdata = strData[(12+i*width):(12+i*width+width)]
        mapData.append(rowdata)
    return mapData, span


# 自定义的二值化图类
class BNBinPic(object):
    def __init__(self, w, h, pdata):
        self.width = w
        self.height = h
        # 图象像素数据对应的帧缓冲
        self.fbuf = FrameBuffer(bytearray(w*h//8), w, h, framebuf.MONO_VLSB)
        # 将图象的像素数据绘制入帧缓冲
        self.drawBNbPicToBuf(pdata)

    # 将图预加载到buffer
    def drawBNbPicToBuf(self, pdata):
        # 当前字节
        currByte = pdata[0]
        # 当前字节计数器
        byteCount = 0
        # 当前比特计数器
        bitCount = 0
        # 当前比特掩码
        bitMask = 0b10000000
        # 遍历每一行
        for i in range(self.height):
            # 此行当前像素位置
            currX = 0
            # 遍历每一列
            for j in range(self.width):
                # 计算当前像素值
                color = (currByte & bitMask) >> (7-bitCount)
                # 绘制当前像素
                self.fbuf.pixel(currX, i, color)
                # X坐标右移一格
                currX = currX+1
                # 比特掩码右移1位
                bitMask = bitMask >> 1
                # 比特计数器加1
                bitCount = bitCount+1
                # 如果比特计数器等于7且还有下一个字节，则换字节
                if bitCount == 8 and byteCount < len(pdata)-1:
                    bitCount = 0
                    byteCount = byteCount+1
                    currByte = pdata[byteCount]
                    bitMask = 0b10000000


def loadPics(fname):
    # 结果列表
    pics = []
    # 读取文件字节数据
    dataFile = open(fname, "rb")
    bytesData = dataFile.read()
    # 字节计数器
    bcount = 0
    # 首先读出四个字节组装为图集中图的数量
    count = readInt(bytesData, bcount)
    bcount = bcount+4
    # 遍历图集中的每一幅图
    for i in range(int(count)):
        # 读取当前图片的宽度、高度
        w = readInt(bytesData, int(bcount))
        bcount = bcount+4
        h = readInt(bytesData, int(bcount))
        bcount = bcount+4
        # 提取此图片像素数据字节序列
        dataCurr = bytesData[int(bcount):int(bcount+w*h/8)]
        bcount = bcount+w*h/8
        pics.append(BNBinPic(w, h, dataCurr))
    return pics

# 加载指定编号文字对应二值图的方法


def getSpecCharBNBinPic(fname, code):
    # 读取文件字节数据
    dataFile = open(fname, "rb")
    # bytesData=dataFile.read()
    # 图像计数器
    pCount = 0
    # 字节计数器
    bcount = 0
    # 首先读出四个字节组装为图集中图的数量
    buf4 = dataFile.read(4)
    count = readInt(buf4, 0)
    bcount = bcount+4
    # 遍历图集中的每一幅图
    for i in range(int(count)):
        # 读取当前图片的宽度、高度
        dataFile.seek(int(bcount))
        buf4 = dataFile.read(4)
        w = readInt(buf4, 0)
        bcount = bcount+4
        dataFile.seek(int(bcount))
        buf4 = dataFile.read(4)
        h = readInt(buf4, 0)
        bcount = bcount+4
        if pCount == code:
            # 提取此图片像素数据字节序列
            dataFile.seek(int(bcount))
            bufPD = dataFile.read(int(w*h/8))
            return BNBinPic(w, h, bufPD)
        bcount = bcount+w*h/8
        pCount = pCount+1


# 自定义的自由物体图类
class BNFreeObject(object):
    def __init__(self, picId, x, y):
        self.x = x
        self.y = y
        self.picId = picId

# 加载自由物体列表文件的方法
# 此文件最开始四个字节为自由物体数量
# 接着为每个自由物体的图像编号以及XY


def loadFreeObject(fname):
    msgFile = open(fname, "rb")
    strData = msgFile.read()
    # 首先读出四个字节组装为自由物体数量
    count = readInt(strData, 0)
    bCount = 4
    # 自由物体列表
    freeObjList = []
    # 接着循环读出每个自由物体
    for i in range(count):
        picId = readInt(strData, bCount)
        bCount = bCount+4
        x = readInt(strData, bCount)
        bCount = bCount+4
        y = readInt(strData, bCount)
        bCount = bCount+4
        freeObjList.append(BNFreeObject(picId, x, y))
    return freeObjList
