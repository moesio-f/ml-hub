import json
import logging
import os

import requests
from flask import jsonify

_URL = os.environ['TRAINING_URL']

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


def train(dataset_csv: bytes,
          models: dict,
          dataset_metadata: dict,
          owner: str,
          model_type: str):
    response = requests.post(f'{_URL}/train',
                             files={
                                 'file': (f'dataset.csv',
                                          dataset_csv,
                                          'text/csv'),
                                 'models': (None,
                                            json.dumps(models),
                                            'application/json'),
                                 'dataset_metadata': (None,
                                                      json.dumps(
                                                          dataset_metadata),
                                                      'application/json'),
                                 'model_type': (None,
                                                model_type,
                                                'text/plain'),
                                 'owner': (None,
                                           owner,
                                           'text/plain')
                             })
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code


def list():
    response = requests.get(f'{_URL}/list')
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code


def status(task_id: str):
    response = requests.get(f'{_URL}/status',
                            json={
                                'task_id': task_id
                            })
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code
