from time import sleep

from LCD_Manager import send_data, init_lcd, set_position, left_shift
from DS18B20_Sensor import read_temp

"""
6. Con base en lo aprendido, modifique el programa de los puntos 3 a 5 para que la Raspberry Pi sirva
una página web donde se pueda variar la velocidad y dirección de la marquesina, además de seleccionar si la
temperatura se muestra en escala centígrada, Farenheit o ambas.
"""

DEGREES_CHAR = chr(0b11011111)


def main():
    init_lcd()

    disp_text = "Bravo, Romero, Bravo"
    send_data(disp_text)

    while True:
        try:
            set_position(1, 0)

            temp_c = read_temp()
            temp_f = temp_c * (9 / 5) + 32

            disp_text = f"{temp_c:3.3f} {DEGREES_CHAR}C  {temp_f}{DEGREES_CHAR}F"

            for c in disp_text:
                send_data(ord(c))

            sleep(1)

            left_shift()
        except KeyboardInterrupt:
            break


main()
