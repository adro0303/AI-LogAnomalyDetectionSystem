import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor

SUPPORTED = {'isolation_forest', 'one_class_svm', 'lof'}

class Detector:
    def __init__(self, model_type: str = 'isolation_forest', scaling: str = 'standard', params: dict | None = None):
        assert model_type in SUPPORTED, f"Modelo no soportado: {model_type}"
        self.model_type = model_type
        self.params = params or {}
        self.scaler = StandardScaler() if scaling == 'standard' else MinMaxScaler()
        if model_type == 'isolation_forest':
            self.model = IsolationForest(**self.params)
        elif model_type == 'one_class_svm':
            self.model = OneClassSVM(**self.params)
        elif model_type == 'lof':
            self.model = LocalOutlierFactor(novelty=True, **self.params)

    def fit(self, X: pd.DataFrame):
        Xs = self.scaler.fit_transform(X)
        self.model.fit(Xs)
        return self

    def score(self, X: pd.DataFrame) -> np.ndarray:
        Xs = self.scaler.transform(X)
        if hasattr(self.model, 'decision_function'):
            s = -self.model.decision_function(Xs)
        else:
            preds = self.model.fit_predict(Xs)
            s = (preds == -1).astype(float)
        return s
