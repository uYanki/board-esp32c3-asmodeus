import time

# 定义状态常量
# 未按下状态(初始状态)
STATE_COMMON = 0
# 按下状态
STATE_DOWN = 1
# 长按状态
STATE_LONG = 2
# 抬起状态
STATE_UP = 3
# 准备抬起状态
STATE_PRE_UP = 4

# 打印状态的方法(开发调试用)


def printState(preStr, state):
    if state == STATE_COMMON:
        print(preStr, "STATE_COMMON")
    elif state == STATE_DOWN:
        print(preStr, "STATE_DOWN")
    elif state == STATE_LONG:
        print(preStr, "STATE_LONG")
    elif state == STATE_UP:
        print(preStr, "STATE_UP")
    elif state == STATE_PRE_UP:
        print(preStr, "STATE_PRE_UP")


# 长按时间阈值
LONG_THOLD = 500
# 抬起时间阈值
UP_THOLD = 250
# 每次读按键值的次数
BUTTON_READ_COUNT = 20
# 每次读取高电平的次数
BUTTON_HIGH_THOLD = 15


class StateMachineForButton:
    # 初始化状态机的方法
    def __init__(self, bnCallBack, buttonPin):
        # 设置按钮对应的输入Pin
        self.buttonPin = buttonPin
        # 设置按钮事件回调方法
        self.onButtonEvent = bnCallBack
        # 设置初始状态
        self.currState = STATE_COMMON
        # 初始化时间戳
        self.timeStamp = 0
        # 初始化计数器
        self.count = 0
    # 状态检测及转移的方法(定时回调)

    def doTask(self):
        # 防抖开始========================================
        # 高电平的次数
        highCount = 0
        # 循环读取按钮电平值指定的次数
        for i in range(BUTTON_READ_COUNT):
            # 若按钮电平值为高电平则增加高电平计数
            if (self.buttonPin.value() == 1):
                highCount = highCount+1
        # 若高电平次数大于阈值
        if highCount >= BUTTON_HIGH_THOLD:
            # 认为当前是高电平
            eLevel = 1
        # 若低电平次数大于阈值
        elif BUTTON_HIGH_THOLD-highCount >= BUTTON_HIGH_THOLD:
            # 认为当前是低电平
            eLevel = 0
        # 若都不是则返回
        else:
            return
        # 防抖结束========================================
        # printState("before>",self.currState)
        # 若当前状态为未按下
        if self.currState == STATE_COMMON:
            # 若当前为高电平
            if eLevel == 1:
                # 转移到按下状态
                self.currState = STATE_DOWN
                # 记录时间戳
                self.timeStamp = time.ticks_ms()
                # 更新计数器
                self.count = 1
        # 若当前状态为按下
        elif self.currState == STATE_DOWN:
            # 若当前为低电平
            if eLevel == 0:
                # 转移到抬起状态
                self.currState = STATE_UP
                # 记录时间戳
                self.timeStamp = time.ticks_ms()
            else:
                # 检查按下时间是否达到阈值
                if (time.ticks_ms()-self.timeStamp) > LONG_THOLD and self.count == 1:
                    # 转移到长按状态
                    self.currState = STATE_LONG
                    # 回调按钮事件处理方法
                    self.onButtonEvent(True)
                elif (time.ticks_ms()-self.timeStamp) > UP_THOLD and self.count > 1:
                    # 转移到准备抬起状态
                    self.currState = STATE_PRE_UP
                    # 回调按钮事件处理方法
                    self.onButtonEvent(False, self.count)
        # 若当前状态为长按
        elif self.currState == STATE_LONG:
            # 若当前为低电平
            if eLevel == 0:
                # 恢复到初始未按下状态
                self.currState = STATE_COMMON
                self.count = 0
        # 若当前状态为抬起
        elif self.currState == STATE_UP:
            # 若当前为高电平
            if eLevel == 1:
                # 转移到按下状态
                self.currState = STATE_DOWN
                # 更新计数器
                self.count = self.count+1
                # 记录时间戳
                self.timeStamp = time.ticks_ms()
            else:
                # 检查按下时间是否达到阈值
                if (time.ticks_ms()-self.timeStamp) > UP_THOLD:
                    # 转移到准备抬起状态
                    self.currState = STATE_COMMON
                    # 回调按钮事件处理方法
                    self.onButtonEvent(False, self.count)
        # 若当前状态为准备抬起
        elif self.currState == STATE_PRE_UP:
            # 若当前为低电平
            if eLevel == 0:
                # 恢复到初始未按下状态
                self.currState = STATE_COMMON
                self.count = 0
