import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score


def pr_auc_proxy(y_true: np.ndarray, scores: np.ndarray) -> float:
    try:
        return float(average_precision_score(y_true, scores))
    except Exception:
        return float('nan')


def recall_at_k(y_true: np.ndarray, scores: np.ndarray, k: int = 100) -> float:
    order = np.argsort(-scores)
    topk = y_true[order][:k]
    tp = topk.sum()
    positives = y_true.sum() if y_true.sum() > 0 else 1.0
    return float(tp / positives)
