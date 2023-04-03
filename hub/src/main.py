"""Módulo principal.
"""

import PySimpleGUI as sg
import gui
import services
from exceptions import JWTExpiredException


if __name__ == '__main__':
    while True:
        jwt, u_type, username = gui.login.start()
        target = gui.admin if (u_type == 'admin') else gui.normal
        services._JWT[0] = jwt

        try:
            target.start(username)
        except JWTExpiredException:
            sg.popup_error("Tempo de uso excedido,"
                           " por favor realize o login novamente.")
