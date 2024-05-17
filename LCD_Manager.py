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


# def init_lcd():
#     send_command(LCD_INIT_DISPLAY_8PINS_MODE)
#     sleep(0.005)
#
#     send_command(LCD_CHANGE_TO_4PINS_MODE)
#     sleep(0.005)
#
#     send_command(0x28)  # Configurar modo: 2 lineas y caracteres de 35 puntos
#     sleep(0.005)
#
#     send_command(LCD_ENABLE_DISPLAY_NO_CURSOR)
#     sleep(0.005)
#
#     send_command(LCD_CLEAN_SCREEN)
#     sleep(0.005)


def init_lcd():
    send_command(0x03)
    sleep(0.005)
    send_command(0x03)
    sleep(0.005)
    send_command(0x03)
    sleep(0.005)
    send_command(0x02)
    sleep(0.005)

    send_command(0x28)  # Configurar modo: 2 lineas y caracteres de 5x8 puntos
    sleep(0.005)

    send_command(LCD_ENABLE_DISPLAY_NO_CURSOR)
    sleep(0.005)

    send_command(LCD_CLEAN_SCREEN)
    sleep(0.005)

    # Configurar el modo de entrada
    send_command(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
    sleep(0.005)


def send_routine(raw_data: int, mode: bool):
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
    sleep(0.002)

    raw_data_temp = raw_data_temp & 0xFB  # Switch not ENA to 0
    send_word(LCD_ADDR, raw_data_temp)

    raw_data_temp = (
        raw_data & 0x0F
    ) << 4  # Delete upper nibble and move lower nibble to upper bits

    raw_data_temp = raw_data_temp | 0x04  # not ENA=1, not RW=0, not RS=0

    send_word(LCD_ADDR, raw_data_temp)
    sleep(0.002)

    raw_data_temp = raw_data_temp & 0xFB  # Flip not ENA to 0
    send_word(LCD_ADDR, raw_data_temp)  # End of nibble


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


def send_command(cmd):
    """
    Send commands to LCD Display, like: clear display, enable disable cursos, config input mode, etc.

    This commands are not displayed in screen, they only control LCD behavior.
    """
    send_routine(cmd, True)


def send_data(data):
    """
    Sends data to LCD to be displayed.
    """
    send_routine(data, False)


# Example usage
if __name__ == "__main__":
    init_lcd()
    send_data(0x48)  # Display character 'H'
    send_data(0x65)  # Display character 'e'
    send_data(0x6C)  # Display character 'l'
    send_data(0x6C)  # Display character 'l'
    send_data(0x6F)  # Display character 'o'
