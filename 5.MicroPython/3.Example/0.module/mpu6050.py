import machine

# 陀螺仪量程：
# reg: 0x1b
# 0x00 -> ±250°/s
# 0x08 -> ±500°/s
# 0x10 -> ±1000°/s
# 0x18 -> ±2000°°/s
# self.iic.writeto(self.addr, bytearray([0x1b, 8*gr])) # gr: 倍率 0~3

# 加速度计量程：
# reg: 0x1c
# 0x00 -> ±2G
# 0x08 -> ±4G
# 0x10 -> ±8G
# 0x18 -> ±16G
# self.iic.writeto(self.addr, bytearray([0x1c, 8*gr])) # gr: 倍率 0~3

SMPLRT_DIV = 0x19  # 陀螺仪输出率的分频，典型值0x07,(1kHz)
CONFIG = 0x1A  # 低通滤波频率,一般0x01~0x05,数值越大带宽越小延时越长
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B    # 加速度计X轴数据高位
ACCEL_XOUT_L = 0x3C    # 加速度计X轴数据低位
ACCEL_YOUT_H = 0x3D    # 以此类推
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40
TEMP_OUT_H = 0x41    # 温度传感器数据
TEMP_OUT_L = 0x42
GYRO_XOUT_H = 0x43    # 陀螺仪X轴数据高位
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48
PWR_MGMT_1 = 0x6B  # 电源管理，典型值：0x00(正常启用)
WHO_AM_I = 0x75  # IIC地址寄存器(默认数值0x68，只读)


class MPU6050():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.writeto(self.addr, bytearray([0x6B, 0]))

    def get_raw_values(self):
        return self.iic.readfrom_mem(self.addr, 0x3B, 14)

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.bytes_toint(
            raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return vals  # returned in range of Int16
        # -32768 to 32767

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while True:
            print(self.get_values())
            sleep(0.05)
