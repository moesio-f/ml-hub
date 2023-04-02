"""Esse módulo contém a aplicação Flask.
"""

import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import jwt as pyjwt

import iam
from flask import Flask, jsonify, request

app = Flask(__name__)
_KEY = 'API_GATEWAY_KEY'
_METRICS = {k: {'total_requests': 0,
                'requests_per_second': 0}
            for k in ['API Gateway',
                      'IAM Gateway',
                      'User Control',
                      'Artifacts',
                      'Training']}
_START_TIME = time.time()

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@app.route('/iam/authenticate')
def authenticate():
    data = request.get_json(force=True)
    data.update({
        'key': _KEY
    })

    _METRICS['IAM Gateway']['total_requests'] += 1

    return iam.authenticate(data)


@app.route('/metrics/')
def metrics():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    user_type = pyjwt.decode(jwt, key=_KEY, algorithms=["HS256"])['user_type']

    if user_type == 'admin':
        delta = time.time() - _START_TIME
        _METRICS['API Gateway']['total_requests'] = sum(
            [_METRICS[k]['total_requests'] for k in _METRICS if k != 'API Gateway'])

        for k in _METRICS:
            v = int(_METRICS[k]['total_requests'] / delta)
            _METRICS[k]['requests_per_second'] = v

        return jsonify(_METRICS), 200

    return jsonify({
        'msg': 'Usuário não autorizado.'
    }), 400
