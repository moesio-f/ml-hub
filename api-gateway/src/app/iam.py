import logging
import os
import requests

from flask import jsonify

_URL = os.environ['IAM_URL']

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


def authenticate(data: dict):
    response = requests.get(f'{_URL}/authenticate',
                            json=data)
    return jsonify(response.json()), response.status_code


def authorization(data: dict, 
                  jwt: str):
    response = requests.get(f'{_URL}/authorization',
                            json=data,
                            headers={
                                'JWT_TOKEN': jwt,
                            })
    return jsonify(response.json()), response.status_code
