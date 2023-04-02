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
    return jsonify(response.json()), response.status_code
