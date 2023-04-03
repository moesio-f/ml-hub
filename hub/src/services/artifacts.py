"""Esse módulo provê funcionalidade de controle de artefatos.
"""
import json
from pathlib import Path

import requests

from exceptions import UserNotPermittedException
from . import _JWT, _URL


def upload_artifact(artifact_path: Path,
                    artifact_type: str,
                    artifact_name: str,
                    username: str):
    response = requests.post(f'{_URL}/artifacts/save/{artifact_type}',
                             files={
                                 'file': (f'{artifact_name}.zip',
                                          artifact_path.read_bytes(),
                                          'application/zip'),
                                 'json': (None,
                                          json.dumps({
                                              'username': username,
                                              'artifact_name': artifact_name,
                                          }),
                                          'application/json')
                             },
                             headers={
                                 'Authorization': f'Bearer {_JWT[0]}'
                             })

    if response.status_code != 200:
        if response.status_code == 401:
            raise UserNotPermittedException()

        raise ValueError()

    return response.json()


def list_artifacts(artifact_type: str):
    response = requests.get(f'{_URL}/artifacts/{artifact_type}s',
                            headers={
                                'Authorization': f'Bearer {_JWT[0]}'
                            })

    if response.status_code != 200:
        if response.status_code == 401:
            raise UserNotPermittedException()

        print(response)
        raise ValueError()

    return response.json()


def artifact_metadata(artifact_id: str,
                      artifact_type: str):
    response = requests.get(f'{_URL}/artifacts/metadata/{artifact_type}',
                            json={
                                'id': artifact_id
                            },
                            headers={
                                'Authorization': f'Bearer {_JWT[0]}'
                            })

    if response.status_code != 200:
        if response.status_code == 401:
            raise UserNotPermittedException()

        raise ValueError()

    return response.json()


def download_artifact(artifact_id: str,
                      artifact_type: str,
                      save_path: Path):
    response = requests.get(f'{_URL}/artifacts/download/{artifact_type}',
                            json={
                                'id': artifact_id
                            },
                            headers={
                                'Authorization': f'Bearer {_JWT[0]}'
                            })

    if response.status_code != 200:
        if response.status_code == 401:
            raise UserNotPermittedException()

        raise ValueError()

    with save_path.open('wb') as f:
        f.write(response.content)
