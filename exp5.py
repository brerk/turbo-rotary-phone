from time import sleep

from LCD_Manager import send_data, init_lcd, set_position, left_shift
from DS18B20_Sensor import read_temp

"""
5. Modifique el programa del punto 3 para que el display muestre en la primera línea del display el
apellido paterno de cada integrante del equipo de trabajo, separados por espacio, como un corrimiento infinito
de marquesina izquierda además de la temperatura en la segunda línea.
"""

DEGREES_CHAR = chr(0b11011111)


def main():
    init_lcd()

    disp_text = "Bravo, Romero, Bravo"

    for c in disp_text:
        send_data(ord(c))

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
