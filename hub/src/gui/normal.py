import re
from pathlib import Path

import PySimpleGUI as sg

from exceptions import UserNotPermittedException
from services import artifacts

_FONT = ('Noto Sans', 16, 'bold')
_SMALL = ('Noto Sans', 10, 'bold')

# Aba artefatos (download)
_DOWNLOAD_BTN = '-DOWNLOAD-BTN-'
_ARTIFACT_TYPE_DOWNLOAD = '-ARTIFACT-TYPE-DOWNLOAD-'
_ARTIFACT_NAME_DOWNLOAD = '-ARTIFACT-NAME-DOWNLOAD-'
_ARTIFACT_DETAILS_DOWNLOAD = '-ARTIFACT-DETAILS-DOWNLOAD-'
layout_artifacts_download = [[sg.VPush()],
                             [sg.Push(),
                              sg.Column([
                                  [sg.Text('Tipo',
                                           font=_FONT)],
                                  [sg.Combo(['Modelo', 'Dataset'],
                                            key=_ARTIFACT_TYPE_DOWNLOAD,
                                            font=_FONT,
                                            size=(12, 1),
                                            enable_events=True,
                                            readonly=True)],
                                  [sg.VPush()],
                                  [sg.Text('Artefato',
                                           font=_FONT)],
                                  [sg.Combo([],
                                            key=_ARTIFACT_NAME_DOWNLOAD,
                                            font=_FONT,
                                            size=(12, 1),
                                            readonly=True)],
                                  [sg.VPush()],
                                  [sg.Text('Salvar em',
                                           font=_FONT)],
                                  [sg.Input(size=(12, 1),
                                            font=_FONT),
                                   sg.FileBrowse('Selecionar',
                                                 font=_FONT)]
                              ],
                                 element_justification='c'),
                              sg.Push(),
                              sg.Column([[sg.Multiline(size=(40, 20),
                                                       key=_ARTIFACT_DETAILS_DOWNLOAD,
                                                       no_scrollbar=True,
                                                       disabled=True)]]),
                              sg.Push()],
                             [sg.VPush()],
                             [sg.Button('Download',
                                        key=_DOWNLOAD_BTN,
                                        font=_FONT)],
                             [sg.VPush()]]

# Aba artefatos (upload)
_UPLOAD_BTN = '-UPLOAD-BTN-'
_ARTIFACT_TYPE_UPLOAD = '-ARTIFACT-TYPE-UPLOAD-'
_ARTIFACT_NAME_UPLOAD = '-ARTIFACT-NAME-UPLOAD-'
_UPLOAD_FNAME = '-FILENAME-UPLOAD-'
layout_artifacts_upload = [[sg.VPush()],
                           [sg.Text('Tipo',
                                    font=_FONT)],
                           [sg.Combo(['Modelo', 'Dataset'],
                                     key=_ARTIFACT_TYPE_UPLOAD,
                                     font=_FONT,
                                     size=(12, 1),
                                     readonly=True)],
                           [sg.VPush()],
                           [sg.Text('Nome do artefato',
                                    font=_FONT)],
                           [sg.InputText(size=(24, 1),
                                         key=_ARTIFACT_NAME_UPLOAD,
                                         font=_SMALL)],
                           [sg.VPush()],
                           [sg.Text('Arquivo (.zip)',
                                    font=_FONT)],
                           [sg.Input(size=(30, 1),
                                     key=_UPLOAD_FNAME,
                                     font=_FONT),
                               sg.FileBrowse('Selecionar',
                                             font=_FONT)],
                           [sg.VPush()],
                           [sg.Button('Upload',
                                      key=_UPLOAD_BTN,
                                      font=_FONT)],
                           [sg.VPush()]]

# Aba treinamento (enviar requisição)
layout_training = [[sg.VPush()]]

# Aba treinamento (visualizar resultados)
layout_results = [[sg.VPush()]]

# Layout da janela
layout = [[sg.TabGroup([[sg.Tab('Artefatos: download',
                                layout_artifacts_download,
                                element_justification='c')],
                        [sg.Tab('Artefatos: upload',
                                layout_artifacts_upload,
                                element_justification='c')],
                        [sg.Tab('Treinamento',
                                layout_training,
                                element_justification='c')],
                        [sg.Tab('Resultados',
                                layout_results,
                                element_justification='c')]],
                       size=(600, 400))]]

window = sg.Window('ML Hub',
                   layout,
                   size=(600, 400))


def upload_artifact(username: str):
    artifact_name = re.sub(r"\s+", "", window[_ARTIFACT_NAME_UPLOAD].get())

    if len(artifact_name) <= 0:
        sg.popup("Por favor, digite o nome do artefato.",
                 custom_text="Ok")
        return

    artifact_type = window[_ARTIFACT_TYPE_UPLOAD].get()
    artifact_type = 'model' if artifact_type == 'Modelo' else 'dataset'

    target_path = window[_UPLOAD_FNAME].get()

    if len(target_path) <= 0:
        sg.popup("Por favor, selecione o artefato.",
                 custom_text="Ok")
        return

    target_path = Path(target_path)

    if not target_path.exists() or \
            not target_path.is_file() or \
            '.zip' not in target_path.name:
        sg.popup("Por favor, selecione um artefato válido.",
                 custom_text="Ok")
        return

    try:
        artifacts.upload_artifact(target_path,
                                  artifact_type,
                                  artifact_name,
                                  username)
        _clear_upload_fields()
    except UserNotPermittedException:
        sg.popup("Você não possui permissão para acessar "
                 "esse serviço. Entre em contato com um "
                 "administrador.",
                 custom_text="Ok")
    except Exception:
        sg.popup("Não foi possível salvar artefato, "
                 "tente novamente.",
                 custom_text="Ok")


def update_artifacts():
    artifact_type = window[_ARTIFACT_TYPE_DOWNLOAD].get()
    artifact_type = 'model' if artifact_type == 'Modelo' else 'dataset'

    try:
        data = artifacts.list_artifacts(artifact_type)
        values = list(map(lambda d: d['objectId'],
                          data))
        window[_ARTIFACT_NAME_DOWNLOAD].update(values=values)
    except UserNotPermittedException:
        sg.popup("Você não possui permissão para acessar "
                 "esse serviço. Entre em contato com um "
                 "administrador.",
                 custom_text="Ok")
    except Exception:
        sg.popup("Não foi possível obter lista de modelos.",
                 custom_text="Ok")


def _clear_upload_fields():
    window[_ARTIFACT_NAME_UPLOAD].update('')
    window[_UPLOAD_FNAME].update('')
    window[_ARTIFACT_TYPE_UPLOAD].update('')


def _clear_download_fields():
    window[_ARTIFACT_NAME_UPLOAD].update('')
    window[_UPLOAD_FNAME].update('')
    window[_ARTIFACT_TYPE_UPLOAD].update('')


def start(*args, **kwargs):
    user = args[0]
    should_exit = False

    while True:
        event, _ = window.read()

        if event == sg.WINDOW_CLOSED:
            should_exit = True
            break

        if event == _UPLOAD_BTN:
            upload_artifact(user)
        elif event == _ARTIFACT_TYPE_DOWNLOAD:
            update_artifacts()

    window.close()

    if should_exit:
        exit(0)
