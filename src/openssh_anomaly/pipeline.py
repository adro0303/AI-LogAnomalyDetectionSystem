from glob import glob
from pathlib import Path
from typing import List
import pandas as pd

from .parser import parse_line
from .io import read_lines
from .clean import clean_record
from .features import feature_row


def parse_to_df(paths: List[str], year: int = 2020) -> pd.DataFrame:
    rows = []
    for p in paths:
        for line in read_lines(p):
            rec = parse_line(line, year=year)
            rec = clean_record(rec)
            if rec:
                rows.append(rec)
    return pd.DataFrame(rows)


def to_features(df: pd.DataFrame) -> pd.DataFrame:
    feat = [feature_row(rec) for rec in df.to_dict(orient='records')]
    return pd.DataFrame(feat)


def rolling_aggregates(feat: pd.DataFrame, window: str = '5min') -> pd.DataFrame:
    df = feat.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    df = df.dropna(subset=['timestamp', 'host'])
    df = df.sort_values('timestamp')
    df = df.set_index('timestamp')
    agg = (
        df.groupby('host')
          .rolling(window)[['is_failed', 'is_accepted', 'msg_len']]
          .sum()
          .rename(columns={'is_failed': 'fails_w', 'is_accepted': 'accepts_w', 'msg_len': 'msgsum_w'})
          .reset_index()
    )
    out = df.reset_index().merge(agg, on=['timestamp', 'host'], how='left')
    for c in ['fails_w', 'accepts_w', 'msgsum_w']:
        out[c] = out[c].fillna(0.0)
    out['hour'] = out['timestamp'].dt.hour
    out['dow'] = out['timestamp'].dt.dayofweek
    out['is_weekend'] = (out['dow'] >= 5).astype(int)
    return out
