import sys
from time import sleep

from LCD_Manager import send_data, init_lcd, send_command, set_position
from DS18B20_Sensor import read_temp

"""
1. Realice un programa en Python que despliegue en consola la temperatura sensada por el DS18B20 cada
segundo.
"""

DEGREES_CHAR = chr(0b11011111)


def main():
    init_lcd()

    while True:

        try:
            set_position(0, 0)
            temp = read_temp()

            disp_text = f"{temp:3.3f} {DEGREES_CHAR}C"
            print(disp_text)

            for c in disp_text:
                send_data(ord(c))

            sleep(1)

        except KeyboardInterrupt:
            sys.exit(0)


main()
