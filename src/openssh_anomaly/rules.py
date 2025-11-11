import pandas as pd

def apply_weak_labels(df: pd.DataFrame, fail_threshold: int = 5) -> pd.Series:
    return ((df.get('fails_w', 0) >= fail_threshold) |
            ((df.get('is_failed', 0) == 1) & (df.get('hour', 0).isin([1,2,3])))).astype(int)
