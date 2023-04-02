"""Esse módulo provê funcionalidade de controle de usuários.
"""


import requests

from exceptions import UserAlreadyExistsException, UserNotFoundException

from . import _JWT, _URL

_PERMISSIONS = [("/user-control/list",
                 "Obtém uma lista de todos os usuários cadastrados no sistema.",
                 "user_control.list"),
                ("/user-control/get",
                 "Obtém informações de 1 usuário do sistema.",
                 "user_control.get"),
                ("/user-control/delete",
                 "Remove um usuário do sistema.",
                 "user_control.delete"),
                ("/user-control/create",
                 "Adiciona um usuário do sistema.",
                 "user_control.create"),
                ("/user-control/update",
                 "Atualiza informações de um usuário do sistema.",
                 "user_control.update"),
                ("/artifacts/models",
                 "Retorna uma lista de modelos armazenados.",
                 "artifacts.list_models"),
                ("/artifacts/datasets",
                 "Retorna uma lista de datasets armazenados.",
                 "artifacts.list_datasets"),
                ("/artifacts/metadata/model",
                 "Obtém os metadados de um único modelo.",
                 "artifacts.model_metadata"),
                ("/artifacts/metadata/dataset",
                 "Obtém os metadados de um único dataset.",
                 "artifacts.dataset_metadata"),
                ("/artifacts/download/model",
                 "Realizar o download de um modelo.",
                 "artifacts.model_download"),
                ("/artifacts/download/dataset",
                 "Realizar o download de um dataset.",
                 "artifacts.dataset_download"),
                ("/artifacts/save/model",
                 "Realizar o upload de um modelo.",
                 "artifacts.model_upload"),
                ("/artifacts/save/dataset",
                 "Realizar o upload de um dataset.",
                 "artifacts.dataset_upload"),
                ("/artifacts/delete/model",
                 "Realizar a remoção de um modelo.",
                 "artifacts.model_delete"),
                ("/artifacts/delete/dataset",
                 "Realizar a remoção de um dataset.",
                 "artifacts.dataset_delete"),
                ("/training/train",
                 "Realizar o treinamento de um modelo.",
                 "training.train"),
                ("/training/status",
                 "Obter o status de treinamento de um modelo.",
                 "training.status"),
                ("/training/model",
                 "Obter o modelo treinado.",
                 "training.model"),
                ("/training/active",
                 "Lista todas as atividades de treinamento ativas.",
                 "training.list_active"),
                ("/training/inactive",
                 "Lista todas as atividades de treinamento inativas.",
                 "training.list_inactive")]


def get_permissions():
    return _PERMISSIONS.copy()


def search_user(username: str) -> dict:
    """
    {
        "user": {
            "username": "moesiof",
            "password": "moesiof",
            "registrationDate": "2023-01-01T00:00:00.000+00:00",
            "type": "admin",
            "name": "Moésio Filho",
            "notes": ""
        },
        "permissions": [
            "user_control.create",
            "user_control.delete"
        ]
    }
    """
    response = requests.get(f'{_URL}/user-control/get',
                            json={
                                'username': username
                            },
                            headers={
                                'Authorization': f'Bearer {_JWT[0]}'
                            })

    if response.status_code != 200:
        raise UserNotFoundException()

    data = response.json()
    permissions = data['permissions']

    for i in range(len(permissions)):
        permissions[i] = [p[2]
                          for p in _PERMISSIONS
                          if p[0] == permissions[i]][0]

    return data


def create_user(username: str,
                password: str,
                is_admin: bool,
                permissions: list[str]):
    for i in range(len(permissions)):
        permissions[i] = [p[0]
                          for p in _PERMISSIONS
                          if p[2] == permissions[i]][0]

    response = requests.post(f'{_URL}/user-control/create',
                             json={
                                 'username': username,
                                 'password': password,
                                 'admin': is_admin,
                                 'permissions': permissions
                             },
                             headers={
                                 'Authorization': f'Bearer {_JWT[0]}'
                             })

    if response.status_code != 200:
        if response.status_code == 400:
            raise UserAlreadyExistsException()

        raise ValueError()


def update_user(username: str,
                permissions: list[str]):
    for i in range(len(permissions)):
        permissions[i] = [p[0]
                          for p in _PERMISSIONS
                          if p[2] == permissions[i]][0]

    response = requests.put(f'{_URL}/user-control/update',
                            json={
                                'username': username,
                                'permissions': permissions
                            },
                            headers={
                                'Authorization': f'Bearer {_JWT[0]}'
                            })

    if response.status_code != 200:
        if response.status_code == 400:
            raise UserNotFoundException()

        raise ValueError()
