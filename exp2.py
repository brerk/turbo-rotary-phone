from time import sleep

from LCD_Manager import send_data, init_lcd

"""
2. Con base en las especificaciones de la subsección 2.3 realice un programa en Python que imprima en la primera 
línea del display el apellido paterno de uno de los integrantes del equipo de trabajo.
"""


def main():
    init_lcd()

    disp_text = "Bravo"

    for c in disp_text:
        send_data(ord(c))


main()
