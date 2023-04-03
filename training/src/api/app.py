"""Esse módulo contém a aplicação Flask.
"""
import json
import logging
import os
from pathlib import Path

import pandas as pd
from celery.result import AsyncResult
from flask import Flask, jsonify, request, Response
from joblib import dump
from werkzeug.utils import secure_filename

from api.storage import TaskResult, add_task, get_tasks
from config.celery import app as celery_app

app = Flask(__name__)

_UPLOAD_PATH = Path('.ml-hub/api/files').absolute()
_UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
_DOWNLOAD_PATH = Path('.ml-hub/api/results').absolute()
_DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
app.config['UPLOAD_FOLDER'] = str(_UPLOAD_PATH)
app.config['DOWNLOAD_FOLDER'] = str(_DOWNLOAD_PATH)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


@app.route('/training/train', methods=['POST'])
def train():
    req_form = request.form.to_dict()

    data = dict()
    for k, v in req_form.items():
        value = v
        app.logger.debug(value)
        if '{' in value:
            value = json.loads(value)
        data[k] = value

    app.logger.debug(data)
    conditions = ['models' in data,
                  'dataset_metadata' in data,
                  'owner' in data,
                  'model_type' in data,
                  'file' in request.files]

    if not all(conditions):
        app.logger.debug(conditions)
        return jsonify({
            'msg': 'Parâmetros incompletos na requisição.'
        }), 400

    # Leitura dos dados da requisição
    username = data['owner']
    models = data['models']['models']
    params = data['models']['parameters']
    dataset_metadata = data['dataset_metadata']
    model_type = data['model_type']

    features_columns = dataset_metadata['features']
    target_column = dataset_metadata['target']
    train_start, train_end = dataset_metadata['train_start'], dataset_metadata['train_end']
    test_start, test_end = dataset_metadata['test_start'], dataset_metadata['test_end']

    # Salvamento do dataset de treino
    file = request.files['file']
    fname = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    file.save(save_path)

    # Carregamento dos datasets
    df = pd.read_csv(save_path)
    train = df.iloc[train_start:train_end, :]
    test = df.iloc[test_start:test_end, :]

    # Envio da task
    async_task = celery_app.send_task(
        'training.train_supervised',
        kwargs={
            'models': models,
            'parameters': params,
            'train_data': train.to_dict(),
            'test_data': test.to_dict(),
            'dataset_metadata': {
                'features': features_columns,
                'target': target_column
            },
            'model_type': model_type
        },
        serializer='pickle')

    app.logger.info(async_task)

    task_id = async_task.id
    task_status = async_task.status
    add_task(task_id=task_id,
             started_by=username,
             status=task_status)

    return jsonify({
        'task_id': task_id,
        'status': task_status,
        'owner': username,
    }), 200


@app.route('/training/status', methods=['GET'])
def status():
    data = request.get_json(force=True)
    tasks = get_tasks()
    task_id = data['task_id']

    if task_id not in tasks:
        return jsonify({
            'msg': 'Task não encontrada.'
        }), 400

    t = tasks[task_id]
    async_result = AsyncResult(id=task_id, app=celery_app)
    result = None

    if t.result is None and async_result.ready():
        try:
            result = async_result.get()
            t.result = TaskResult(metrics=result['metrics'],
                                  pipeline_size=result['pipeline_size'],
                                  train_samples=result['train_size'],
                                  test_samples=result['test_size'])
            t.status = async_result.status

            model = result['model']
            root = Path(app.config['DOWNLOAD_FOLDER'],
                        f'{t.id}')
            root.mkdir(parents=True, exist_ok=True)
            dump(model, root.joinpath('model.joblib'))
        except Exception:
            output.update({'msg': 'Resultado já foi obtido.'})

    output = {
        'task_id': t.id,
        'start_time': t.start_time,
        'owner': t.started_by,
        'status': t.status
    }

    if t.result is not None:
        output.update({
            'metrics': t.result.metrics,
            'pipeline_size': t.result.pipeline_size,
            'train_samples': t.result.train_samples,
            'test_samples': t.result.test_samples
        })

    return jsonify(output)


@app.route('/training/model', methods=['GET'])
def model():
    data = request.get_json(force=True)
    tasks = get_tasks()
    task_id = data['task_id']

    if task_id not in tasks:
        return jsonify({
            'msg': 'Task não encontrada.'
        }), 400

    t = tasks[task_id]
    target = Path(app.config['DOWNLOAD_FOLDER'],
                  f'{t.id}').absolute()

    if not target.exists():
        return jsonify({'msg': 'Modelo não encontrado.'}), 400

    dest = Path(app.config['DOWNLOAD_FOLDER'],
                f'{t.id}',
                f'model.zip').absolute()
    os.system(f'zip -j -r {str(dest)} {str(target)}')

    for p in Path(app.config['DOWNLOAD_FOLDER']).glob('*/'):
        if p.is_dir() and t.id not in str(p):
            os.system(f'rm -rf {str(p.absolute())}')

    return Response(dest.read_bytes(),
                    mimetype='application/zip',
                    headers={'Content-Disposition': f'attachment;filename={t.id}.zip'})


@app.route('/training/list', methods=['GET'])
def active_tasks():
    return jsonify([{
        'task_id': t.id,
        'start_time': t.start_time,
        'owner': t.started_by
    } for t in get_tasks().values()])
