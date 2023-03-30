"""Esse módulo contém as Celery Tasks
realizadas pelo worker.
"""
from __future__ import annotations

import pandas as pd
from sklearn import pipeline
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error, r2_score

from config.celery import app as celery_app
from utils.sklearn_mapper import get_class


@celery_app.task(name='training.train_supervised')
def train_supervised(models: list[str],
                     parameters: list[dict],
                     train_data: dict,
                     test_data: dict,
                     dataset_metadata: dict,
                     model_type: str) -> dict:
    """Essa função permite realizar o treinamento de um modelo
    através do scikit-learn e um conjunto de dados.

    Returns:
        dict: dicionário contendo as especificações 
            do modelo treinado.
    """
    # Carregamento dos dados de treinamento e avaliação
    assert 'features' in dataset_metadata
    assert 'target' in dataset_metadata
    features_columns = dataset_metadata['features']
    target_column = dataset_metadata['target']
    train = pd.DataFrame.from_dict(train_data)
    test = pd.DataFrame.from_dict(test_data)

    # Instanciação do modelo que deve ser treinado
    assert len(models) == len(parameters)
    instances = []

    for m, p in zip(models, parameters):
        instances.append(get_class(m)(**p))

    model_pipeline = pipeline.make_pipeline(*instances)

    # Treinamento
    X_train, Y_train = train[features_columns].values, train[target_column].values
    model_pipeline.fit(X_train, Y_train)

    # Avaliação
    X_test, Y_test = test[features_columns].values, test[target_column].values
    predictions = model_pipeline.predict(X_test)
    metrics = None

    if model_type == 'classifier':
        metrics = classification_report(y_true=Y_test,
                                        y_pred=predictions,
                                        output_dict=True,
                                        digits=3)
    else:
        metrics = {
            'MSE': mean_squared_error(y_true=Y_test,
                                      y_pred=predictions),
            'MAE': mean_absolute_error(y_true=Y_test,
                                       y_pred=predictions),
            'R2': r2_score(y_true=Y_test,
                           y_pred=predictions)
        }

    return {
        'pipeline_size': len(model_pipeline.steps),
        'train_size': len(train),
        'test_size': len(test),
        'metrics': metrics,
        'model': model_pipeline
    }
