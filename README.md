
# OpenSSH Log Anomaly Detection (Open Data / Loghub)

> Detección de comportamientos anómalos en **logs OpenSSH** mediante ingeniería de características temporal + modelos **no supervisados** (Isolation Forest, LOF, One-Class SVM) y **supervisión débil** para evaluación proxy. Repositorio orientado a **empleabilidad**: ingeniería de datos, MLOps ligero, reproducibilidad y comunicación técnica.

## 🚀 Quickstart

```bash
# 1) Crear entorno
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Colocar datos (OpenSSH desde Loghub)
# Clona o copia los archivos de https://github.com/logpai/loghub/tree/master/OpenSSH a data/raw/

# 3) Ejecutar pipeline mínimo (prepare → train → eval)
python -m openssh_anomaly.cli prepare --config configs/base.yaml
python -m openssh_anomaly.cli train   --config configs/base.yaml
python -m openssh_anomaly.cli eval    --config configs/base.yaml
```

> **Nota:** Este repo no incluye los datos por licencia/tamaño. Usa la carpeta `data/raw/` para colocar los logs.

## 🧭 Objetivo de negocio (resumen)
Reducir intentos de intrusión SSH detectando patrones anómalos en logs. Entregable: un pipeline reproducible que prioriza alertas con explicaciones, métricas **PR-AUC (proxy)** y **Recall@K** sobre **weak labels**.

## 🧱 Arquitectura (alto nivel)
```mermaid
digraph G {
  rankdir=LR;
  A[Logs OpenSSH (raw)] -> B[Parser & Clean];
  B -> C[Feature Engineering
(ventanas, plantillas, flags)];
  C -> D[Modelos no supervisados
(IF/LOF/OCSVM)];
  C -> E[Reglas heurísticas
(weak labels)];
  D -> F[Ranking & Scores];
  E -> G[Evaluación proxy
PR-AUC / Recall@K];
  F -> G;  F -> H[Reportes & Visualización];
}
```

## 📂 Estructura
```
openssh-anomaly/
├─ docs/                  # model_card, system_design, labeling_strategy, security
├─ data/{raw,interim,processed}
├─ notebooks/             # 00_pipeline.ipynb (demo)
├─ src/openssh_anomaly/   # paquete python (pipeline y CLI)
├─ tests/                 # pytest (parser, features, pipeline)
├─ configs/               # YAMLs de config
├─ docker/                # Dockerfile
├─ .github/workflows/     # CI (lint + tests)
└─ Makefile, requirements.txt, README.md
```

## 📊 Métricas
- **Proxy (weak labels)**: `average_precision_score` (PR-AUC) y `Recall@K`.
- **Operativas**: alertas/día, reducción vs. baseline de reglas simples.

## ⚠️ Limitaciones y ética
- Weak labels pueden contener ruido; se documentan en `docs/labeling_strategy.md`.
- Minimiza exposición de PII (hash de IP/usuario para muestras públicas).

## 🛣️ Roadmap corto
- LOF y OCSVM + tuning básico.
- Backtesting temporal.
- Explicabilidad adicional y tablero ligero (opcional).

## Citado
- Datos: Loghub / OpenSSH → https://github.com/logpai/loghub/tree/master/OpenSSH
- Inspiración de métricas y pipeline: documentación scikit-learn, literatura de anomaly detection.
