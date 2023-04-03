import PySimpleGUI as sg

from services import login

_USER_KEY = '-USER-'
_PASS_KEY = '-PASSWORD-'
_LOGIN_KEY = 'Entrar'
_ERROR_KEY = '--ERROR--'

layout = [[sg.VPush()],
          [sg.Text('ML Hub',
                   font=('Noto Sans', 32, 'bold'))],
          [sg.VPush()],
          [sg.Text('Digite o nome de usuário:',
                   font=('Noto Sans', 22, 'bold'))],
          [sg.InputText(key=_USER_KEY,
                        font=('Noto Sans', 22, 'bold'),
                        justification='c')],
          [sg.Text('Digite a senha:',
                   font=('Noto Sans', 22, 'bold'))],
          [sg.InputText(key=_PASS_KEY,
                        password_char='*',
                        font=('Noto Sans', 22, 'bold'),
                        justification='c')],
          [sg.Submit(button_text=_LOGIN_KEY,
                     font=('Noto Sans', 22, 'bold'))],
          [sg.Text('Não foi possível realizar o login. Tente novamente.',
                   text_color='Red',
                   visible=False,
                   key=_ERROR_KEY)],
          [sg.VPush()]]

window = sg.Window('ML Hub', layout,
                   auto_size_text=True,
                   auto_size_buttons=True,
                   text_justification='c',
                   element_justification='c',
                   size=(600, 400))


def start() -> str:
    jwt = None
    username = None
    should_exit = False

    while True:
        event, _ = window.read()

        if event == sg.WINDOW_CLOSED:
            should_exit = True
            break
        elif event == _LOGIN_KEY:
            u, p = window[_USER_KEY].get(), window[_PASS_KEY].get()
            if len(u) > 0 and len(p) > 0:
                try:
                    jwt, user_type = login.authenticate(u, p)
                    username = u
                    break
                except ValueError:
                    sg.popup("Não foi possível autenticar,"
                             " tente novamente.",
                             custom_text='Ok')
            else:
                sg.popup("Por favor, digite o nome de usuário "
                         "e senha.",
                         custom_text='Ok')

    window.close()

    if should_exit:
        exit(0)

    return jwt, user_type, username
