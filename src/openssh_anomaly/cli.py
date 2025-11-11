import argparse
from pathlib import Path
import sys
import pandas as pd

from .config import ProjectConfig
from .pipeline import parse_to_df, to_features, rolling_aggregates
from .rules import apply_weak_labels
from .unsupervised import Detector
from .scoring import pr_auc_proxy, recall_at_k


def cmd_prepare(cfg: ProjectConfig):
    raw_dir = Path(cfg.data['raw_dir'])
    year = int(cfg.data.get('year', 2020))
    paths = [str(p) for p in raw_dir.glob('*') if p.is_file()]
    if not paths:
        print(f"No se encontraron archivos en {raw_dir}. Coloca los logs OpenSSH allí.")
        sys.exit(1)
    df = parse_to_df(paths, year=year)
    feat = to_features(df)
    feat = rolling_aggregates(feat, window=cfg.features.get('window', '5min'))
    out = Path(cfg.data['processed_dir']) / 'openssh_features.parquet'
    out.parent.mkdir(parents=True, exist_ok=True)
    feat.to_parquet(out, index=False)
    print(f"Features preparadas → {out} ({len(feat)} filas)")


def cmd_train(cfg: ProjectConfig):
    proc = Path(cfg.data['processed_dir']) / 'openssh_features.parquet'
    if not proc.exists():
        print("No existe processed data. Ejecuta 'prepare' primero.")
        sys.exit(1)
    df = pd.read_parquet(proc)
    df = df.sort_values('timestamp')
    cut = int(0.8 * len(df))
    train = df.iloc[:cut].copy()
    num_cols = ['msg_len','fails_w','accepts_w','msgsum_w','hour','dow']
    Xtr = train[num_cols].fillna(0.0)
    det = Detector(cfg.model.get('type', 'isolation_forest'), cfg.scaling.get('method','standard'), cfg.model.get('params', {}))
    det.fit(Xtr)
    import pickle
    model_path = Path(cfg.data['processed_dir']) / 'detector.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump({'det': det, 'num_cols': num_cols}, f)
    print(f"Modelo entrenado → {model_path}")


def cmd_predict(cfg: ProjectConfig):
    proc = Path(cfg.data['processed_dir']) / 'openssh_features.parquet'
    model_path = Path(cfg.data['processed_dir']) / 'detector.pkl'
    if not proc.exists() or not model_path.exists():
        print("Faltan datos procesados o modelo. Ejecuta prepare y train.")
        sys.exit(1)
    import pickle
    df = pd.read_parquet(proc)
    with open(model_path, 'rb') as f:
        obj = pickle.load(f)
    det, num_cols = obj['det'], obj['num_cols']
    X = df[num_cols].fillna(0.0)
    df['anom_score'] = det.score(X)
    out = Path(cfg.data['processed_dir']) / 'openssh_scored.parquet'
    df.to_parquet(out, index=False)
    print(f"Scores escritos → {out}")


def cmd_eval(cfg: ProjectConfig):
    proc = Path(cfg.data['processed_dir']) / 'openssh_features.parquet'
    scored = Path(cfg.data['processed_dir']) / 'openssh_scored.parquet'
    if not proc.exists():
        print("No existe processed data. Ejecuta 'prepare' primero.")
        sys.exit(1)
    df = pd.read_parquet(proc)
    if not scored.exists():
        print("No existen scores. Ejecuta 'predict' o usa 'train' y 'eval' en secuencia.")
    df['weak_label'] = apply_weak_labels(df, fail_threshold=int(cfg.features.get('fail_threshold', 5)))
    if scored.exists():
        s = pd.read_parquet(scored)['anom_score'].values
    else:
        s = df['fails_w'].astype(float).values
    y = df['weak_label'].values
    ap = pr_auc_proxy(y, s)
    r_at_k = recall_at_k(y, s, k=int(cfg.eval.get('topk', 200)))
    print(f"PR-AUC (proxy): {ap:.4f}")
    print(f"Recall@{cfg.eval.get('topk', 200)}: {r_at_k:.4f}")


def main():
    p = argparse.ArgumentParser(description='OpenSSH Anomaly Detection CLI')
    p.add_argument('command', choices=['prepare', 'train', 'predict', 'eval'])
    p.add_argument('--config', default='configs/base.yaml')
    args = p.parse_args()
    cfg = ProjectConfig.load(args.config)
    if args.command == 'prepare':
        cmd_prepare(cfg)
    elif args.command == 'train':
        cmd_train(cfg)
    elif args.command == 'predict':
        cmd_predict(cfg)
    elif args.command == 'eval':
        cmd_eval(cfg)

if __name__ == '__main__':
    main()
