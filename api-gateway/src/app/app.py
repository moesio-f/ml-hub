"""Esse módulo contém a aplicação Flask.
"""

import json
import logging
import os
import time
from pathlib import Path

import artifacts
import iam
import jwt as pyjwt
import training
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
def delete_user():
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


@app.route('/artifacts/save/model', methods=['POST'])
def save_model():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = json.loads(request.form['json'])
    resp, code = _auth(jwt, endpoint='/artifacts/save/model')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.save_artifact(username=data['username'],
                                       artifact_name=data['artifact_name'],
                                       artifact_type='model',
                                       file=request.files['file'])
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/artifacts/models')
def list_models():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    resp, code = _auth(jwt, endpoint='/artifacts/models')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.list_artifact('models')
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/artifacts/metadata/model')
def metadata_model():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/artifacts/metadata/model')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.artifact_metadata(data['id'], 'model')
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/artifacts/download/model')
def download_model():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/artifacts/download/model')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.download_artifact(data['id'], 'model')
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/artifacts/save/dataset', methods=['POST'])
def save_dataset():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = json.loads(request.form['json'])
    resp, code = _auth(jwt, endpoint='/artifacts/save/dataset')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.save_artifact(username=data['username'],
                                       artifact_name=data['artifact_name'],
                                       artifact_type='dataset',
                                       file=request.files['file'])
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/artifacts/datasets')
def list_datasets():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    resp, code = _auth(jwt, endpoint='/artifacts/datasets')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.list_artifact('datasets')
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/artifacts/metadata/dataset')
def metadata_dataset():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/artifacts/metadata/dataset')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.artifact_metadata(data['id'], 'dataset')
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/artifacts/download/dataset')
def download_dataset():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/artifacts/download/dataset')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return artifacts.download_artifact(data['id'], 'dataset')
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401


@app.route('/training/train', methods=['POST'])
def train():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/training/train')

    _METRICS['Artifacts']['total_requests'] += 1
    _METRICS['Training']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        models = {
            "models": list(map(lambda d: d['class'],
                               data['models'])),
            "parameters": list(map(lambda d: d['parameters'],
                               data['models']))
        }

        dataset_metadata = {
            "features": data['dataset']['features_columns'],
            "target": data['dataset']['target_column'],
            "train_start": data['dataset']['train']['start'],
            "train_end": data['dataset']['train']['end'],
            "test_start": data['dataset']['test']['start'],
            "test_end": data['dataset']['test']['end']
        }

        resp, code = artifacts.download_artifact(data['dataset_id'],
                                                 'dataset')

        if code != 200:
            return jsonify({}), code
        
        temp_path = Path('/tmp/.ml_hub/api-gateway/')
        temp_path.mkdir(parents=True, exist_ok=False)
        temp_file = temp_path.joinpath('temp.zip')
        with temp_file.open('wb') as f:
            f.write(resp.data)

        unzip = os.system(f'unzip {str(temp_file)} -d {str(temp_path)}')

        if unzip != 0:
            os.system(f'rm -rf {str(temp_path)}')
            return jsonify({}), 500

        temp_file = list(temp_path.glob('*.csv'))[0]
        dataset_csv = temp_file.read_bytes()
        os.system(f'rm -rf {str(temp_path)}')

        return training.train(dataset_csv=dataset_csv,
                              models=models,
                              dataset_metadata=dataset_metadata,
                              model_type=data['model_type'],
                              owner=data['username'])
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401
    

@app.route('/training/list')
def train_list():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    resp, code = _auth(jwt, endpoint='/training/list')

    _METRICS['Training']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return training.list()
    else:
        return jsonify({'msg': 'Usuário não autorizado.'}), 401
    

@app.route('/training/status')
def train_status():
    jwt = request.headers.get('Authorization').split(" ")[-1]
    data = request.get_json(force=True)
    resp, code = _auth(jwt, endpoint='/training/status')

    _METRICS['Training']['total_requests'] += 1
    _METRICS['API Gateway']['total_requests'] += 1
    _METRICS['IAM Gateway']['total_requests'] += 1

    if _is_authorized(resp.get_json(), code):
        return training.status(task_id=data['task_id'])
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
