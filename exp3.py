from time import sleep

from LCD_Manager import send_data, init_lcd, set_position
from DS18B20_Sensor import read_temp

"""
3. Modifique el programa anterior para que el display muestre en la segunda línea del display la temperatura
en grados centígrados registrada por el DS18B20, actualizada cada segundo.
"""


def main():
    init_lcd()

    disp_text = "Bravo"
    send_data(disp_text)

    set_position(1, 0)

    while True:

        try:
            temp_c = read_temp()

            disp_text = f"{temp_c:3.3f} °C"

            for c in disp_text:
                send_data(ord(c))

            sleep(1)
        except KeyboardInterrupt:
            break


main()
