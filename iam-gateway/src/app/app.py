"""Esse módulo contém a aplicação Flask.
"""

from flask import Flask, jsonify, request
from datetime import datetime, timedelta

import jwt_utils
import persistence
import user_control

app = Flask(__name__)


@app.route('/iam/authenticate')
def authenticate():
    data = request.get_json(force=True)
    username = data['username']
    password = data['password']
    key = data['key']

    user = user_control.get_user(username)

    if user is None:
        return jsonify({
            'error': 'Usuário não encontrado.'
        }), 400

    if password != user.password:
        return jsonify({
            'error': 'Senha incorreta.'
        }), 400

    user_jwt = jwt_utils.get_jwt(username=username,
                                 user_type=user.user_type,
                                 key=key,
                                 creation_date=datetime.now(),
                                 expiration_date=datetime.now() + timedelta(hours=1))

    persistence.save_user_jwt(user_jwt)

    return jsonify({
        'jwt': user_jwt.jwt,
        'username': user.username,
        'user_type': user.user_type
    }), 200


@app.route('/iam/authorization')
def authorization():
    jwt_token = request.headers.get('JWT_TOKEN')
    data = request.get_json(force=True)
    username = data['username']
    user_type = data['user_type']
    endpoint = data['endpoint']

    saved_jwt = persistence.read_user_jwt(username)

    if saved_jwt is None:
        return jsonify({
            'permitted': False,
            'reason': 'Usuário não autenticado.'
        }), 200

    if saved_jwt.jwt != jwt_token:
        return jsonify({
            'permitted': False,
            'reason': 'Token inválido.'
        }), 200

    if saved_jwt.is_expired():
        return jsonify({
            'permitted': False,
            'reason': 'O token expirou.'
        }), 200

    if user_type.lower() == 'admin':
        return jsonify({
            'permitted': True,
            'endpoint': endpoint,
            'username': username,
            'reason': 'admin'
        }), 200

    user = user_control.get_user(username)
    permissions = user.permissions

    if endpoint in permissions:
        return jsonify({
            'permitted': True,
            'endpoint': endpoint,
            'username': username,
            'reason': 'permission'
        }), 200

    return jsonify({
        'permitted': False,
        'reason': 'Usuário não possui permissão.'
    }), 200
