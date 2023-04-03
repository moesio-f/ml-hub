"""Esse módulo provê funcionalidades para
métricas.
"""

import requests

from . import _JWT, _URL

_SERVICES = [
    'API Gateway',
    'IAM Gateway',
    'User Control',
    'Artifacts',
    'Training'
]


def services_names():
    return _SERVICES.copy()


def get_metrics() -> dict:
    response = requests.get(f'{_URL}/metrics',
                            headers={
                                'Authorization': f'Bearer {_JWT[0]}'
                            })

    if response.status_code == 200:
        d = response.json()
        return {k: d[k] for k in _SERVICES}

    return {k: {
        'total_requests': 0,
        'requests_per_second': 0
    } for k in _SERVICES}
