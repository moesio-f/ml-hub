import re

import PySimpleGUI as sg

from exceptions import UserNotFoundException, UserAlreadyExistsException
from services import metrics, user_control

_FONT = ('Noto Sans', 16, 'bold')

# Aba de métricas
_METRIC_TABLE = '-TABLE-METRICS-'
layout_metrics = [[sg.VPush()],
                  [sg.Table(headings=['Serviço', 'Total', 'Requisições/s'],
                            values=[[s, 0, 0]
                                    for s in metrics.services_names()],
                            justification='center',
                            key=_METRIC_TABLE,
                            auto_size_columns=False,
                            max_col_width=20,
                            def_col_width=15,
                            num_rows=5,
                            select_mode=sg.TABLE_SELECT_MODE_NONE,
                            hide_vertical_scroll=True,
                            font=_FONT)],
                  [sg.VPush()]]

# Aba de cadastro de usuário
_R_USER_KEY = '-N-USER-'
_R_PASS_KEY = '-N-PASS-'
_PERMISSION_TABLE = '-N-TABLE-PERMISSION'
_ADMIN_CHECKBOX = '-N-ADM-CHECKBOX-'
_CREATE_BTN = '-N-CREATE-BTN-'
layout_register = [[sg.VPush()],
                   [sg.Push(),
                    sg.Text('Usuário:',
                            font=_FONT,
                            size=(20, 1),
                            justification='c'),
                    sg.Push(),
                    sg.Text('Senha:',
                            font=_FONT,
                            size=(20, 1),
                            justification='c'),
                    sg.Push()],
                   [sg.Push(),
                    sg.InputText(key=_R_USER_KEY,
                                 font=_FONT,
                                 justification='c',
                                 size=(20, 1)),
                    sg.Push(),
                    sg.InputText(key=_R_PASS_KEY,
                                 password_char='*',
                                 font=_FONT,
                                 justification='c',
                                 size=(20, 1)),
                    sg.Push()],
                   [sg.Push(),
                    sg.Text('Permissões:',
                            font=_FONT,
                            size=(20, 1),
                            justification='c'),
                    sg.Push()],
                   [sg.Push(),
                    sg.Table(headings=['Permissão', 'Checkbox'],
                             values=[[p[2], '☐']  # ☐ ☑
                                     for p in user_control.get_permissions()],
                             justification='center',
                             key=_PERMISSION_TABLE,
                             auto_size_columns=False,
                             enable_click_events=True,
                             max_col_width=25,
                             def_col_width=25,
                             num_rows=5,
                             font=_FONT),
                    sg.Push()],
                   [sg.Push(),
                    sg.Checkbox('Administrador',
                                font=_FONT,
                                key=_ADMIN_CHECKBOX),
                    sg.Push()],
                   [sg.Push(),
                    sg.Button('Criar',
                              key=_CREATE_BTN,
                              font=_FONT),
                    sg.Push()],
                   [sg.VPush()]]

# Aba de modificação de permissões
_SEARCH_BTN = '-SEARCH-BTN-'
_UPDATE_BTN = '-UPDATE-BTN-'
_U_USER_KEY = '-U-USER-'
_PERMISSION_TABLE_UPDATE = '-TABLE-UPDATE-PERMISSION-'
layout_iam = [[sg.VPush()],
              [sg.Push(),
               sg.Text('Usuário:',
                       font=_FONT,
                       size=(20, 1),
                       justification='c'),
               sg.Push()],
              [sg.Push(),
               sg.InputText(key=_U_USER_KEY,
                            font=_FONT,
                            justification='c',
                            size=(20, 1)),
               sg.Push()],
              [sg.VPush()],
              [sg.Push(),
               sg.Table(headings=['Permissão', 'Checkbox'],
                        values=[[p[2], '☐']  # ☐ ☑
                                for p in user_control.get_permissions()],
                        justification='center',
                        key=_PERMISSION_TABLE_UPDATE,
                        auto_size_columns=False,
                        max_col_width=25,
                        def_col_width=25,
                        num_rows=5,
                        enable_click_events=True,
                        font=_FONT),
               sg.Push()],
              [sg.VPush()],
              [sg.Push(),
               sg.Button('Buscar',
                         key=_SEARCH_BTN,
                         font=_FONT),
               sg.Push(),
               sg.Button('Atualizar',
                         key=_UPDATE_BTN,
                         font=_FONT),
               sg.Push()],
              [sg.VPush()]]

# Aba de usuários
_DELETE_BTN = '-DELETE-BTN-'
_REFRESH_BTN = '-REFRESH-BTN-'
_USER_TABLE = '-TABLE-USERS-'
layout_users = [[sg.VPush()],
                [sg.Push(),
                 sg.Table(headings=['Usuário', 'Tipo', 'Selecionado'],
                          values=[[]],
                          justification='center',
                          key=_USER_TABLE,
                          auto_size_columns=False,
                          max_col_width=12,
                          def_col_width=12,
                          num_rows=10,
                          enable_click_events=True,
                          font=_FONT),
                 sg.Push()],
                [sg.VPush()],
                [sg.Push(),
                 sg.Button('Atualizar',
                           key=_REFRESH_BTN,
                           font=_FONT),
                 sg.Push(),
                 sg.Button('Remover selecionados',
                           key=_DELETE_BTN,
                           font=_FONT),
                 sg.Push()],
                [sg.VPush()]]

# Layout da janela
layout = [[sg.TabGroup([[sg.Tab('Dashboard',
                                layout_metrics,
                                element_justification='c',
                                expand_x=True,
                                expand_y=True)],
                        [sg.Tab('Cadastro', layout_register)],
                        [sg.Tab('IAM', layout_iam)],
                        [sg.Tab('Usuários', layout_users)]],
                       size=(600, 400))]]

window = sg.Window('ML Hub',
                   layout,
                   size=(600, 400))


def update_metrics():
    table = window[_METRIC_TABLE]
    m = metrics.get_metrics()
    values = [[k, v['total_requests'], f"{v['requests_per_second']:.2f}"]
              for k, v in m.items()]
    table.update(values=values)


def search_user() -> str | None:
    username = window[_U_USER_KEY].get()
    username = re.sub(r"\s+", "", username)

    if len(username) <= 0:
        sg.popup("Por favor, digite um usuário.",
                 custom_text="Ok")
        table = window[_PERMISSION_TABLE_UPDATE]
        values = table.get()

        for i in range(len(values)):
            values[i][1] = '☐'

        table.update(values=values)
        return None

    try:
        permissions = user_control.search_user(username)['permissions']
        table = window[_PERMISSION_TABLE_UPDATE]
        values = table.get()

        for i in range(len(values)):
            values[i][1] = '☑' if values[i][0] in permissions else '☐'

        table.update(values=values)
    except UserNotFoundException:
        sg.popup("Usuário não encontrado.",
                 custom_text="Ok")
        _clear_update_fields()
        return None

    return username


def create_user():
    username = re.sub(r"\s+", "", window[_R_USER_KEY].get())
    password = re.sub(r"\s+", "", window[_R_PASS_KEY].get())
    admin = window[_ADMIN_CHECKBOX].get()

    if len(username) <= 0 or len(password) <= 0:
        sg.popup("Nome de usuário ou senha não "
                 "podem ser vazios.",
                 custom_text="Ok")
        return

    table = window[_PERMISSION_TABLE]
    values = table.get()
    permissions = [v[0] for v in values if v[1] == '☑']

    try:
        user_control.create_user(username=username,
                                 password=password,
                                 is_admin=admin,
                                 permissions=permissions)
    except UserAlreadyExistsException:
        sg.popup("Usuário já existe.",
                 custom_text="Ok")
    except Exception:
        sg.popup("Não foi possível criar "
                 "o usuário, tente novamente.",
                 custom_text="Ok")

    _clear_create_fields()


def update_user(username: str | None):
    if username is None:
        sg.popup("Selecione um usuário.",
                 custom_text="Ok")
        return

    table = window[_PERMISSION_TABLE_UPDATE]
    values = table.get()
    permissions = [v[0] for v in values if v[1] == '☑']

    try:
        user_control.update_user(username=username,
                                 permissions=permissions)
    except Exception:
        sg.popup("Não foi possível atualizar permissões "
                 "do usuário, tente novamente.",
                 custom_text="Ok")

    _clear_update_fields()


def refresh_users():
    users = user_control.list_users()
    table = window[_USER_TABLE]
    values = [[d['username'], d['type'], '☐']
              for d in users
              if d['username'] != 'root']
    table.update(values)


def delete_user():
    table = window[_USER_TABLE]
    values = table.get()
    user = [v[0] for v in values
            if v[2] == '☑'][0]

    try:
        user_control.delete_user(username=user)
    except Exception:
        sg.popup("Não foi possível remover usuário, "
                 "tente novamente.",
                 custom_text="Ok")


def selected_permission_row(table_key, row, column):
    if row is None or column is None:
        return

    if table_key not in [_PERMISSION_TABLE,
                         _PERMISSION_TABLE_UPDATE,
                         _USER_TABLE]:
        return

    table = window[table_key]
    values = table.get()

    def _update():
        current = values[row][column]
        values[row][column] = '☐' if current == '☑' else '☑'
        table.update(values=values)

    if table_key == _USER_TABLE:
        if column != 2:
            return
        _update()
        for i in range(len(values)):
            if i != row:
                values[i][2] = '☐'
        table.update(values=values)
    else:
        if column != 1:
            return
        _update()


def _clear_update_fields():
    table = window[_PERMISSION_TABLE_UPDATE]
    values = table.get()
    values = [[v[0], '☐'] for v in values]
    table.update(values=values)
    window[_U_USER_KEY].update('')


def _clear_create_fields():
    table = window[_PERMISSION_TABLE]
    values = table.get()
    values = [[v[0], '☐'] for v in values]
    table.update(values=values)
    window[_R_USER_KEY].update('')
    window[_R_PASS_KEY].update('')
    window[_ADMIN_CHECKBOX].update(False)


def start(*args, **kwargs):
    should_exit = False
    selected_user = None

    while True:
        event, _ = window.read(timeout=1000)

        if event == sg.WINDOW_CLOSED:
            should_exit = True
            break

        if event == _CREATE_BTN:
            create_user()
        elif event == _SEARCH_BTN:
            selected_user = search_user()
        elif event == _UPDATE_BTN:
            update_user(selected_user)
            selected_user = None
        elif event == _REFRESH_BTN:
            refresh_users()
        elif event == _DELETE_BTN:
            delete_user()
            refresh_users()
        elif '+CLICKED+' in event:
            selected_permission_row(event[0],
                                    event[-1][0],
                                    event[-1][1])

        update_metrics()

    window.close()

    if should_exit:
        exit(0)
