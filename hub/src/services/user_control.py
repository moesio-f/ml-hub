"""Esse módulo provê funcionalidade de controle de usuários.
"""

from exceptions import UserNotFoundException, UserAlreadyExistsException

_PERMISSIONS = [("/user-control/list",
                 "Obtém uma lista de todos os usuários cadastrados no sistema.",
                 "user_control.list"),
                ("/user-control/get/",
                 "Obtém informações de 1 usuário do sistema.",
                 "user_control.get"),
                ("/user-control/delete/",
                 "Remove um usuário do sistema.",
                 "user_control.delete"),
                ("/user-control/create/",
                 "Adiciona um usuário do sistema.",
                 "user_control.create"),
                ("/user-control/update/",
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
                 "training.list_inactive"),
                ("/metrics/requests",
                 "Retorna a quantidade de solicitações a um dado endpoint.",
                 "metrics.requests")]


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
    if not True:
        raise UserNotFoundException()

    return {
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


def create_user(username: str,
                password: str,
                is_admin: bool,
                permissions: list[str]):
    raise ValueError()
