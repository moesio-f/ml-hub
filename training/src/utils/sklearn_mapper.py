"""Esse módulo provê um mapeador entre
strings e suas respectivas classes no scikit.
"""

from __future__ import annotations

from sklearn import (decomposition, ensemble, feature_selection,
                     linear_model, neighbors, neural_network,
                     preprocessing, svm)

_MAPPER = {
    'PCA': decomposition.PCA,
    'KernelPCA': decomposition.KernelPCA,
    'AdaBoostClassifier': ensemble.AdaBoostClassifier,
    'AdaBoostRegressor': ensemble.AdaBoostRegressor,
    'ExtraTreesClassifier': ensemble.ExtraTreesClassifier,
    'ExtraTreesRegressor': ensemble.ExtraTreesRegressor,
    'RandomForestClassifier': ensemble.RandomForestClassifier,
    'RandomForestRegressor': ensemble.RandomForestRegressor,
    'SelectKBest': feature_selection.SelectKBest,
    'RFE': feature_selection.RFE,
    'LogisticRegression': linear_model.LogisticRegression,
    'RidgeClassifier': linear_model.RidgeClassifier,
    'KNeighborsClassifier': neighbors.KNeighborsClassifier,
    'KNeighborsRegressor': neighbors.KNeighborsRegressor,
    'MLPCLassifier': neural_network.MLPClassifier,
    'MLPRegressor': neural_network.MLPRegressor,
    'Binarizer': preprocessing.Binarizer,
    'LabelEncoder': preprocessing.LabelEncoder,
    'StandardScaler': preprocessing.StandardScaler,
    'MinMaxScaler': preprocessing.MinMaxScaler,
    'SVC': svm.SVC,
    'SVR': svm.SVR
}


def get_acceptable_values() -> list[str]:
    return list(_MAPPER.values())


def get_class(target: str) -> type:
    if target not in _MAPPER:
        raise ValueError("Target class not found.")
    return _MAPPER[target]
