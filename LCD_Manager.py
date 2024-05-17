import smbus2  # I2C
from time import sleep

"""
I2C --> Controls LCD Display.
"""

LCD_ENABLE_LIGHT = 0x08
LCD_DISABLE_LIGHT = 0xF7

LCD_INIT_DISPLAY_8PINS_MODE = 0x33
LCD_CHANGE_TO_4PINS_MODE = 0x32
LCD_ENABLE_DISPLAY_NO_CURSOR = 0x0C
LCD_CLEAN_SCREEN = 0x01

LCD_ENTRYMODESET = 0x04
LCD_ENTRYLEFT = 0x02

# 33
# 32
# 28
# 0C
# 01

BUS = smbus2.SMBus(1)

# NOTE: Check if LCD Address Driver is correct
# LCD_ADDR = 0x3F
LCD_ADDR = 0x27

BLEN = 1  # LCD Backlight State


# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00


def init_lcd():
    # Waiting for display to be ready
    send_command(0x03)
    send_command(0x03)
    send_command(0x03)

    # Enable 4 bits mode
    send_command(0x02)

    send_command(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
    send_command(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
    send_command(LCD_CLEARDISPLAY)

    send_command(LCD_ENTRYMODESET | LCD_ENTRYLEFT)

    sleep(0.2)


def set_position(row: int, column: int):
    if column < 0 or column > 16:
        return

    if row < 0 or row > 1:
        return

    send_command(0x80 + 0x40 * column + row)


def send_routine(raw_data: int, mode=True):
    """
    mode: True --> send command
          False --> send data
    """

    raw_data_temp = raw_data & 0xF0  # Discard low nibble

    if mode:
        raw_data_temp = raw_data_temp | 0x04  # not ENA=1, not RW = 0, not RS = 0
    else:
        raw_data_temp = raw_data_temp | 0x05  # not ENA=1, not RW = 0, not RS = 1

    send_word(LCD_ADDR, raw_data_temp)
    sleep(0.0005)

    raw_data_temp = raw_data_temp & 0xFB  # Switch not ENA to 0
    send_word(LCD_ADDR, raw_data_temp)
    sleep(0.0001)

    raw_data_temp = (
        raw_data & 0x0F
    ) << 4  # Delete upper nibble and move lower nibble to upper bits

    if mode:
        raw_data_temp = raw_data_temp | 0x04  # not ENA=1, not RW=0, not RS=0
    else:
        raw_data_temp = raw_data_temp | 0x05  # not ENA=1, not RW = 0, not RS = 1

    send_word(LCD_ADDR, raw_data_temp)
    sleep(0.0005)

    raw_data_temp = raw_data_temp & 0xFB  # Flip not ENA to 0
    send_word(LCD_ADDR, raw_data_temp)  # End of nibble

    sleep(0.0001)


def send_word(addr, data):
    """
    addr: hex
    data: hex - 8 bits - 1 byte
    """
    global BLEN

    temp = data
    if BLEN == 1:
        temp |= LCD_ENABLE_LIGHT
    else:
        temp &= LCD_DISABLE_LIGHT

    BUS.write_byte(addr, temp)

    sleep(0.0001)


def send_command(cmd):
    """
    Send commands to LCD Display, like: clear display, enable disable cursos, config input mode, etc.

    This commands are not displayed in screen, they only control LCD behavior.
    """
    send_routine(cmd, True)

    sleep(0.0005)


def send_data(data):
    """
    Sends data to LCD to be displayed.
    """
    send_routine(data, False)

    sleep(0.0005)


# Example usage
if __name__ == "__main__":
    text = input("Inserte texto:")

    init_lcd()

    for c in text:
        print(f"{c=} --> {ord(c)=}")
        send_data(ord(c))

    print("done")
