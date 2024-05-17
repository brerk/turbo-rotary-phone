# Future imports (Python 2.7 compatibility)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import json
from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer

from LCD_Manager import send_data, init_lcd, set_position, left_shift, right_shift
from DS18B20_Sensor import read_temp

address = "localhost"
port = 8080

"""
6. Con base en lo aprendido, modifique el programa de los puntos 3 a 5 para que la Raspberry Pi sirva
una página web donde se pueda 

        - Variar la velocidad
        - Dirección de la marquesina 
        - Además de seleccionar si la temperatura se muestra en escala centígrada, Farenheit o ambas.

"""

OPTIONS = {"DIRECTION": True, "SPEED": 1}  # True: Right, Left: Left

def shift_lcd(options)
    while True:
        try:
            # Shift direction
            if options["DIRECTION"]:  # shift Right
                right_shift()
            else:  # Shift left
                left_shift()

            sleep(options["SPEED"])

        except KeyboardInterrupt:
            break


def update_lcd_temp(options):
    """
    To be run inside a thread
    """

    disp_text = "Bravo, Romero, Bravo"
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


class WebServer(BaseHTTPRequestHandler):
    def _serve_ui_file(self):
        """Sirve el archivo de interfaz de usuario"""
        if not os.path.isfile("user_interface.html"):
            err = "user_interface.html not found."
            self.wfile.write(bytes(err, "utf-8"))
            print(err)
            return
        try:
            with open("user_interface.html", "r") as f:
                content = "\n".join(f.readlines())
        except:
            content = "Error reading user_interface.html"
        self.wfile.write(bytes(content, "utf-8"))

    def _parse_post(self, json_obj: dict):
        """
        Handles user actions
        """
        global OPTIONS

        print("Received: ", json_obj)

        if json_obj["action"] == "pwr":
            OPTIONS["SPEED"] =  int(json_obj["value"]) if json_obj["value"].isdigit()  else 1

            # update_power(int(json_obj["value"]))
        elif json_obj["action"] == "buttons":
            OPTIONS["DIRECTION"] =  True if json_obj["value"] == "right" else False

    def do_GET(self):
        """do_GET controla todas las solicitudes recibidas vía GET, es
        decir, páginas. Por seguridad, no se analizan variables que lleguen
        por esta vía"""

        if self.path == "/":
            # 200 es el código de respuesta satisfactorio (OK) de una solicitud
            self.send_response(200)

            # La cabecera HTTP siempre debe contener el tipo de datos mime
            # del contenido con el que responde el servidor
            self.send_header("Content-type", "text/html")

            # Fin de cabecera
            self.end_headers()

            # Por simplicidad, se devuelve como respuesta el contenido del
            # archivo html con el código de la página de interfaz de usuario
            self._serve_ui_file()

    def do_POST(self):
        """do_POST controla todas las solicitudes recibidas vía POST, es
        decir, envíos de formulario. Aquí se gestionan los comandos para
        la Raspberry Pi"""

        print("Received post request")

        # Primero se obtiene la longitud de la cadena de datos recibida
        content_length = int(self.headers.get("Content-Length"))
        if content_length < 1:
            return
        # Después se lee toda la cadena de datos
        post_data = self.rfile.read(content_length)
        # Finalmente, se decodifica el objeto JSON y se procesan los datos.
        # Se descartan cadenas de datos mal formados
        try:
            jobj = json.loads(post_data.decode("utf-8"))
            self._parse_post(jobj)
        except:
            print(sys.exc_info())
            print("Datos POST no recnocidos")


def display_handler():
    init_lcd()

    disp_text = "Bravo, Romero, Bravo"
    send_data(disp_text)

    while True:
        try:
            set_position(1, 0)

            temp_c = read_temp()
            temp_f = temp_c * (9 / 5) + 32

            disp_text = f"{temp_c:3.3f} °C  {temp_f}°F"

            for c in disp_text:
                send_data(ord(c))

            sleep(1)

            # shift row 0 to left
            set_position(0, 0)
            left_shift()
        except KeyboardInterrupt:
            break


def main():

    init_lcd()

    webServer = HTTPServer((address, port), WebServer)

    print("Servidor iniciado")
    print("\tAtendiendo solicitudes en http://{}:{}".format(address, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Maneja la interrupción de cierre CTRL+C
        pass
    except:
        print(sys.exc_info())

    webServer.server_close()

    print("Server stopped.")


# Punto de anclaje de la función main
if __name__ == "__main__":
    main()
