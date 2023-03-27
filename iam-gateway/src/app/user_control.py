"""Esse módulo realiza a comunicação com o serviço
de controle de usuários através do API Gateway.
"""

import os
import requests

from entities import User

def get_user(username: str) -> None | User:
    endpoint = os.environ['USER_CONTROL_URL']
    response = requests.get(f'{endpoint}/get/{username}')
    
    if response.status_code != 200:
        return None
    
    data = response.json()

    return User(username=data['user']['username'],
                password=data['user']['password'],
                user_type=data['user']['type'],
                permissions=data['permissions'])

