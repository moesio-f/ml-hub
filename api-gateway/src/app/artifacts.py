import logging
import os

import requests
from flask import jsonify, Response

_URL = os.environ['ARTIFACTS_URL']

logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)


def save_artifact(username: str,
                  artifact_name: str,
                  artifact_type: str,
                  file,
                  ):
    response = requests.post(f'{_URL}/save/{artifact_type}/{username}/{artifact_name}',
                             files={
                                 'file': file
                             })
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code


def list_artifact(artifact_type: str):
    response = requests.get(f'{_URL}/{artifact_type}')
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code


def artifact_metadata(artifact_id: str,
                      artifact_type: str):
    response = requests.get(f'{_URL}/metadata/{artifact_type}/{artifact_id}')
    data = {}

    if response.status_code == 200:
        data = response.json()

    return jsonify(data), response.status_code


def download_artifact(artifact_id: str,
                      artifact_type: str):
    response = requests.get(f'{_URL}/download/{artifact_type}/{artifact_id}')
    data = jsonify({})

    if response.status_code == 200:
        content = response.content
        data = Response(content,
                        mimetype='application/zip',
                        headers={'Content-Disposition':
                                 f'attachment;filename={artifact_id}.zip'})

    return data, response.status_code
