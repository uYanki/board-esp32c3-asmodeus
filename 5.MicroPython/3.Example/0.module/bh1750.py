
BH1750_CMD_POWERDOWN = 0x0
BH1750_CMD_POWERON = 0x1
BH1750_CMD_RESET = 0x7
BH1750_CMD_H_RESOLUTION = 0x10
BH1750_CMD_H_RESOLUTION2 = 0x11
BH1750_CMD_L_RESOLUTION = 0x13
BH1750_CMD_ONETIME_H = 0x20
BH1750_CMD_ONETIME_H2 = 0x21
BH1750_CMD_ONETIME_L = 0x23

BH1750_I2C_ADD = 0x5c  # 0x23


class BH1750():

    def __init__(self, i2c, addr=BH1750_I2C_ADD):
        self.i2c = i2c
        self.addr = addr
        buf = bytearray(1)
        buf[0] = BH1750_CMD_H_RESOLUTION
        i2c.writeto(self.addr, buf)

    def read(self):
        buf = self.i2c.readfrom(self.addr, 0x2)
        data = buf[0] * 256 + buf[1]
        return data
