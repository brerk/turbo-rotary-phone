from time import sleep

from LCD_Manager import send_data, init_lcd, set_position
from DS18B20_Sensor import read_temp

"""
3. Modifique el programa anterior para que el display muestre en la segunda línea del display la temperatura
en grados centígrados registrada por el DS18B20, actualizada cada segundo.
"""


def display_text(text):
    for c in text:
        send_data(ord(c))


def main():
    init_lcd()

    disp_text = "Bravo"
    display_text(disp_text)

    while True:
        set_position(1, 0)

        try:
            temp_c = read_temp()

            disp_text = f"{temp_c:3.3f} {chr(0b11011111)}C"

            display_text(disp_text)

            sleep(1)
        except KeyboardInterrupt:
            break


main()
