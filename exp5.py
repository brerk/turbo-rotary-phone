from time import sleep

from LCD_Manager import send_data, init_lcd, set_position
from DS18B20_Sensor import read_temp

"""
5. Modifique el programa del punto 3 para que el display muestre en la primera línea del display el
apellido paterno de cada integrante del equipo de trabajo, separados por espacio, como un corrimiento infinito
de marquesina izquierda además de la temperatura en la segunda línea.
"""


def main():
    init_lcd()

    disp_text = "Bravo"
    send_data(disp_text)

    set_position(1, 0)

    while True:

        try:
            temp_c = read_temp()
            temp_f = temp_c * (9 / 5) + 32

            disp_text = f"{temp_c:3.3f} °C  {temp_f}°F"

            for c in disp_text:
                send_data(ord(c))

            sleep(1)
        except KeyboardInterrupt:
            break


main()
