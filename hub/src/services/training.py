"""Esse módulo provê funcionalidades para o
treinamento de modelos.
"""
import json
from pathlib import Path

import requests

from exceptions import UserNotPermittedException
from . import _JWT, _URL


def send_training(username: str,
                  dataset_id: str,
                  model_type: str,
                  config: dict):
    data = {
        'username': username,
        'dataset_id': dataset_id,
        'model_type': model_type
    }
    data.update(config)

    response = requests.post(f'{_URL}/training/train',
                             json=data,
                             headers={
                                 'Authorization': f'Bearer {_JWT[0]}'
                             })

    if response.status_code != 200:
        if response.status_code == 401:
            raise UserNotPermittedException()

        raise ValueError()
