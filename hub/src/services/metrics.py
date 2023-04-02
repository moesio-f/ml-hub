"""Esse módulo provê funcionalidades 
"""

import random

_SERVICES = {
    'API Gateway',
    'IAM Gateway',
    'User Control',
    'Artifacts',
    'Training'
}


def services_names():
    return _SERVICES.copy()


def get_metrics() -> dict:
    return {k: {
        'total_requests': random.randint(0, 500),
        'requests_per_second': random.randint(0, 100)
    } for k in _SERVICES}
