import json
import re
from pathlib import Path

import PySimpleGUI as sg

from exceptions import UserNotPermittedException
from services import artifacts, training

_FONT = ('Noto Sans', 16, 'bold')
_SMALL = ('Noto Sans', 10, 'bold')

# Aba artefatos (download)
_DOWNLOAD_BTN = '-DOWNLOAD-BTN-'
_ARTIFACT_TYPE_DOWNLOAD = '-ARTIFACT-TYPE-DOWNLOAD-'
_ARTIFACT_NAME_DOWNLOAD = '-ARTIFACT-NAME-DOWNLOAD-'
_ARTIFACT_DETAILS_DOWNLOAD = '-ARTIFACT-DETAILS-DOWNLOAD-'
_DOWNLOAD_DIRECTORY = '-DIRECTORY-DOWNLOAD-'
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
                                            enable_events=True,
                                            readonly=True)],
                                  [sg.VPush()],
                                  [sg.Text('Salvar em',
                                           font=_FONT)],
                                  [sg.Input(size=(24, 1),
                                            key=_DOWNLOAD_DIRECTORY,
                                            font=_SMALL),
                                   sg.FolderBrowse('Selecionar',
                                                   font=_FONT)]
                              ],
                                 element_justification='c'),
                              sg.Push(),
                              sg.Column([[sg.Multiline(size=(40, 10),
                                                       key=_ARTIFACT_DETAILS_DOWNLOAD,
                                                       no_scrollbar=True,
                                                       disabled=True,
                                                       font=_FONT)]]),
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
_SEND_BTN = '-SEND-BTN-'
_TRAINING_TYPE = '-TRAINING-TYPE'
_AVAILABLE_DATASETS = '-AVAILABLE-DATASETS-'
_TRAINING_CONFIG = '-TRAINING-CONFIG-'
layout_training = [[sg.VPush()],
                   [sg.Push(),
                    sg.Column([[sg.Multiline(size=(40, 15),
                                             key=_TRAINING_CONFIG,
                                             no_scrollbar=True,
                                             font=_SMALL)]]),
                    sg.Push(),
                    sg.Column([
                        [sg.Text('Tipo',
                                 font=_FONT)],
                        [sg.Combo(['Classificação', 'Regressão'],
                                  key=_TRAINING_TYPE,
                                  font=_FONT,
                                  size=(12, 1),
                                  enable_events=True,
                                  readonly=True)],
                        [sg.VPush()],
                        [sg.Text('Dataset',
                                 font=_FONT)],
                        [sg.Combo([],
                                  key=_AVAILABLE_DATASETS,
                                  font=_FONT,
                                  size=(12, 1),
                                  enable_events=True,
                                  readonly=True)],
                        [sg.VPush()],
                    ],
                       element_justification='c'),
                    sg.Push()],
                   [sg.VPush()],
                   [sg.Button('Enviar',
                              key=_SEND_BTN,
                              font=_FONT)],
                   [sg.VPush()]]

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
    window[_ARTIFACT_NAME_DOWNLOAD].update('', values=[])
    window[_ARTIFACT_DETAILS_DOWNLOAD].update('')

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
        sg.popup("Não foi possível obter lista de artefatos.",
                 custom_text="Ok")


def update_artifact_metadata():
    window[_ARTIFACT_DETAILS_DOWNLOAD].update('')
    artifact_type = window[_ARTIFACT_TYPE_DOWNLOAD].get()
    artifact_type = 'model' if artifact_type == 'Modelo' else 'dataset'
    artifact_name = window[_ARTIFACT_NAME_DOWNLOAD].get()

    try:
        data = artifacts.artifact_metadata(artifact_name,
                                           artifact_type)
        window[_ARTIFACT_DETAILS_DOWNLOAD].update(json.dumps(data,
                                                             indent=4,
                                                             ensure_ascii=False))
    except UserNotPermittedException:
        sg.popup("Você não possui permissão para acessar "
                 "esse serviço. Entre em contato com um "
                 "administrador.",
                 custom_text="Ok")
    except Exception:
        sg.popup("Não foi possível obter metadados do artefato.",
                 custom_text="Ok")


def download_artifact():
    artifact_type = window[_ARTIFACT_TYPE_DOWNLOAD].get()
    artifact_id = window[_ARTIFACT_NAME_DOWNLOAD].get()
    save_location = window[_DOWNLOAD_DIRECTORY].get()

    if len(artifact_type) <= 0 or \
            len(artifact_id) <= 0 or \
            len(save_location) <= 0:
        sg.popup("Por favor, preencha todos os campos.",
                 custom_text="Ok")
        return

    artifact_type = 'model' if artifact_type == 'Modelo' else 'dataset'
    save_location = Path(save_location).joinpath(f'{artifact_id}.zip')

    try:
        artifacts.download_artifact(artifact_id,
                                    artifact_type,
                                    save_location)
        _clear_download_fields()
    except UserNotPermittedException:
        sg.popup("Você não possui permissão para acessar "
                 "esse serviço. Entre em contato com um "
                 "administrador.",
                 custom_text="Ok")
    except Exception:
        sg.popup("Não foi possível realizar download do artefato.",
                 custom_text="Ok")


def fetch_datasets():
    try:
        data = artifacts.list_artifacts('dataset')
        values = list(map(lambda d: d['objectId'],
                          data))
        window[_AVAILABLE_DATASETS].update(values=values)
    except UserNotPermittedException:
        sg.popup("Você não possui permissão para acessar "
                 "esse serviço. Entre em contato com um "
                 "administrador.",
                 custom_text="Ok")
    except Exception:
        sg.popup("Não foi possível obter lista de artefatos.",
                 custom_text="Ok")


def send_training(user: str):
    training_type = window[_TRAINING_TYPE].get()
    dataset = window[_AVAILABLE_DATASETS].get()
    config = window[_TRAINING_CONFIG].get()

    if len(training_type) <= 0 or \
            len(dataset) <= 0 or \
            len(config) <= 0:
        sg.popup("Por favor, preencha todos os campos.",
                 custom_text="Ok")
        return

    model_type = 'classifier' if training_type == 'Classificação' else 'regressor'

    try:
        config = json.loads(config)
    except Exception:
        sg.popup("Configuração de treinamento não é um JSON.",
                 custom_text="Ok")
        return

    if not _is_valid_config(config):
        sg.popup("Configuração de treinamento inválida.",
                 custom_text="Ok")
        return

    try:
        training.send_training(user,
                               dataset,
                               model_type,
                               config)
        _clear_training_fields()
    except UserNotPermittedException:
        sg.popup("Você não possui permissão para acessar "
                 "esse serviço. Entre em contato com um "
                 "administrador.",
                 custom_text="Ok")
    except Exception:
        sg.popup("Não foi possível enviar a requisição de treinamento.",
                 custom_text="Ok")


def _clear_upload_fields():
    window[_ARTIFACT_NAME_UPLOAD].update('')
    window[_UPLOAD_FNAME].update('')
    window[_ARTIFACT_TYPE_UPLOAD].update('')


def _clear_download_fields():
    window[_ARTIFACT_NAME_DOWNLOAD].update('')
    window[_ARTIFACT_NAME_DOWNLOAD].update(values=[])
    window[_ARTIFACT_DETAILS_DOWNLOAD].update('')
    window[_ARTIFACT_TYPE_DOWNLOAD].update('')
    window[_DOWNLOAD_DIRECTORY].update('')


def _clear_training_fields():
    window[_TRAINING_TYPE].update('')
    window[_AVAILABLE_DATASETS].update('')
    window[_TRAINING_CONFIG].update('')


def _is_valid_config(data) -> bool:
    if 'models' not in data:
        return False
    elif 'dataset' not in data:
        return False

    if len(data['models']) <= 0:
        return False
    else:
        for m in data['models']:
            if 'class' not in m or \
                    'parameters' not in m:
                return False

    if 'features_columns' not in data['dataset']:
        return False
    elif 'target_column' not in data['dataset']:
        return False
    elif 'train' not in data['dataset'] or \
            'test' not in data['dataset']:
        return False
    else:
        if any(['start' not in data['dataset'][k] or
                'end' not in data['dataset'][k]
                for k in ['train', 'test']]):
            return False

    return True


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
        elif event == _ARTIFACT_NAME_DOWNLOAD:
            update_artifact_metadata()
        elif event == _DOWNLOAD_BTN:
            download_artifact()
        elif event == _TRAINING_TYPE:
            fetch_datasets()
        elif event == _SEND_BTN:
            send_training(user)

    window.close()

    if should_exit:
        exit(0)
