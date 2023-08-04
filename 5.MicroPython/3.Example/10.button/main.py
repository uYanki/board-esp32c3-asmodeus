import time
from machine import Pin
from ButtonStateMachine import StateMachineForButton

# 按钮状态机对象


def btnCbk(isLong, count=0):
    if isLong:
        print("Long push!")
    else:
        print("Click>", count)  # 连按


buttonPin = Pin(9, Pin.IN, Pin.PULL_UP)
smfb = StateMachineForButton(btnCbk, buttonPin)

while True:
    smfb.doTask()
    time.sleep(0.005)
