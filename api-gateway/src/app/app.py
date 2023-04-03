"""Esse módulo contém a aplicação Flask.
"""

import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import iam
import jwt as pyjwt
import user_control
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
    _METRICS['API Gateway']['total_requests'] += 1

    return iam.authenticate(data)


@app.route('/user-control/get')
def get_user():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/user-control/get')

    _METRICS['User Control']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return user_control.get(data['username'])
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/user-control/list')
def list_users():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    resp, code = _auth(jwt, endpoint='/user-control/list')

    _METRICS['User Control']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return user_control.users()
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/user-control/create', methods=['POST'])
def create_user():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/user-control/create')

    _METRICS['User Control']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return user_control.create(username=data['username'],
                                   password=data['password'],
                                   user_type='admin' if data['admin'] else 'normal',
                                   permissions=data['permissions'])
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/user-control/update', methods=['PUT'])
def update_user():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/user-control/update')

    _METRICS['User Control']['total_requests'] += 2
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return user_control.update(username=data['username'],
                                   permissions=data['permissions'])
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401
    

@app.route('/user-control/delete', methods=['DELETE'])
def delte_user():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/user-control/delete')

    _METRICS['User Control']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return user_control.delete(username=data['username'])
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/metrics/')
def metrics():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    user_type = pyjwt.decode(jwt, key=_KEY, algorithms=["HS256"])['user_type']
    _METRICS['API Gateway']['total_requests'] += 1

    if user_type == 'admin':
        delta = time.time() - _START_TIME

        for k in _METRICS:
            v = _METRICS[k]['total_requests'] / delta
            _METRICS[k]['requests_per_second'] = v

        return jsonify(_METRICS), 200

    return jsonify({
        'msg': 'Usuário não autorizado.'
    }), 400


def _auth(jwt, endpoint):
    jwt_ = pyjwt.decode(jwt, key=_KEY, algorithms=["HS256"])
    return iam.authorization({
        'username': jwt_['user'],
        'user_type': jwt_['user_type'],
        'endpoint': endpoint
    },
        jwt)


def _is_authorized(auth, status):
    app.logger.info(auth)
    if status != 200:
        return False

    k = 'permitted'
    return k in auth and auth[k]
