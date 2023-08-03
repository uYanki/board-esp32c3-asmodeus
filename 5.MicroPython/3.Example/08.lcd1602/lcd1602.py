import utime
import gc

from lcd_api import LcdApi
from machine import I2C

# PCF8574 pin definitions
MASK_RS = 0x01      # P0
MASK_RW = 0x02      # P1
MASK_E = 0x04       # P2

SHIFT_BACKLIGHT = 3  # P3
SHIFT_DATA = 4  # P4-P7


class lcd1602_i2c(LcdApi):

    # Implements a HD44780 character LCD connected via PCF8574 on I2C

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytes([0]))
        utime.sleep_ms(20)   # Allow LCD time to powerup
        # Send reset 3 times
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(5)    # Need to delay at least 4.1 msec
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        utime.sleep_ms(1)
        # Put LCD into 4-bit mode
        self.hal_write_init_nibble(self.LCD_FUNCTION)
        utime.sleep_ms(1)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)
        gc.collect()

    def hal_write_init_nibble(self, nibble):
        # Writes an initialization nibble to the LCD.
        # This particular function is only used during initialization.
        byte = ((nibble >> 4) & 0x0f) << SHIFT_DATA
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        gc.collect()

    def hal_backlight_on(self):
        # Allows the hal layer to turn the backlight on
        self.i2c.writeto(self.i2c_addr, bytes([1 << SHIFT_BACKLIGHT]))
        gc.collect()

    def hal_backlight_off(self):
        # Allows the hal layer to turn the backlight off
        self.i2c.writeto(self.i2c_addr, bytes([0]))
        gc.collect()

    def hal_write_command(self, cmd):
        # Write a command to the LCD. Data is latched on the falling edge of E.
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                (((cmd >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        byte = ((self.backlight << SHIFT_BACKLIGHT) |
                ((cmd & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        if cmd <= 3:
            # The home and clear commands require a worst case delay of 4.1 msec
            utime.sleep_ms(5)
        gc.collect()

    def hal_write_data(self, data):
        # Write data to the LCD. Data is latched on the falling edge of E.
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                (((data >> 4) & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        byte = (MASK_RS |
                (self.backlight << SHIFT_BACKLIGHT) |
                ((data & 0x0f) << SHIFT_DATA))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([byte]))
        gc.collect()


class custom_char:
    # generate by https://maxpromer.github.io/LCD-Character-Creator/

    # smiley faces
    happy = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x11, 0x0E, 0x00])
    sad = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x0E, 0x11, 0x00])
    grin = bytearray([0x00, 0x00, 0x0A, 0x00, 0x1F, 0x11, 0x0E, 0x00])
    shock = bytearray([0x0A, 0x00, 0x04, 0x00, 0x0E, 0x11, 0x11, 0x0E])
    meh = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x1F, 0x00, 0x00])
    angry = bytearray([0x11, 0x0A, 0x11, 0x04, 0x00, 0x0E, 0x11, 0x00])
    tongue = bytearray([0x00, 0x0A, 0x00, 0x04, 0x00, 0x1F, 0x05, 0x02])

    # icons
    bell = bytearray([0x04, 0x0e, 0x0e, 0x0e, 0x1f, 0x00, 0x04, 0x00])
    note = bytearray([0x02, 0x03, 0x02, 0x0e, 0x1e, 0x0c, 0x00, 0x00])
    clock = bytearray([0x00, 0x0e, 0x15, 0x17, 0x11, 0x0e, 0x00, 0x00])
    heart = bytearray([0x00, 0x0a, 0x1f, 0x1f, 0x0e, 0x04, 0x00, 0x00])
    duck = bytearray([0x00, 0x0c, 0x1d, 0x0f, 0x0f, 0x06, 0x00, 0x00])
    check = bytearray([0x00, 0x01, 0x03, 0x16, 0x1c, 0x08, 0x00, 0x00])
    cross = bytearray([0x00, 0x1b, 0x0e, 0x04, 0x0e, 0x1b, 0x00, 0x00])
    retarrow = bytearray([0x01, 0x01, 0x05, 0x09, 0x1f, 0x08, 0x04, 0x00])

    # battery icons
    battery0 = bytearray([0x0E, 0x1B, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F])  # 0% Empty
    battery1 = bytearray([0x0E, 0x1B, 0x11, 0x11, 0x11, 0x11, 0x1F, 0x1F])  # 16%
    battery2 = bytearray([0x0E, 0x1B, 0x11, 0x11, 0x11, 0x1F, 0x1F, 0x1F])  # 33%
    battery3 = bytearray([0x0E, 0x1B, 0x11, 0x11, 0x1F, 0x1F, 0x1F, 0x1F])  # 50%
    battery4 = bytearray([0x0E, 0x1B, 0x11, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F])  # 66%
    battery5 = bytearray([0x0E, 0x1B, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F])  # 83%
    battery6 = bytearray([0x0E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F])  # 100% Full
    battery7 = bytearray([0x0E, 0x1F, 0x1B, 0x1B, 0x1B, 0x1F, 0x1B, 0x1F])  # ! Error

    sword = bytearray([0x04, 0x0E, 0x0E, 0x0E, 0x0E, 0x1F, 0x04, 0x04])
    axe = bytearray([0x00, 0x00, 0x0E, 0x13, 0x05, 0x09, 0x10, 0x00])
