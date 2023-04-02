import logging
import os

import requests
from flask import jsonify

_URL = os.environ['USER_CONTROL_URL']

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


def get(username: str):
    response = requests.get(f'{_URL}/get/{username}')
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code


def update(username: str,
           permissions: list[str]):
    user = requests.get(f'{_URL}/get/{username}').json()['user']
    response = requests.put(f'{_URL}/update/{username}',
                             json={
                                 "user": {
                                     "username": username,
                                     "password": user['password'],
                                     "registrationDate": user['registrationDate'],
                                     "type": user['type'],
                                     "name": user['name'],
                                     "notes": user['notes']
                                 },
                                 "permissions": permissions
                             })
    logger.info(response.request.body)
    return jsonify({}), response.status_code


def create(username: str,
           password: str,
           user_type: str,
           permissions: list[str]):
    response = requests.post(f'{_URL}/create',
                             json={
                                 "user": {
                                     "username": username,
                                     "password": password,
                                     "registrationDate": "2023-01-01T00:00:00.000+00:00",
                                     "type": user_type,
                                     "name": username,
                                     "notes": ""
                                 },
                                 "permissions": permissions
                             })
    
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code
