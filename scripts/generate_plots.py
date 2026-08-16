"""Regenerates the result plots used in the README from the trained pipeline output.
Run from the repo root after `prepare`, `train` and `predict`: python scripts/generate_plots.py
"""
import sys
sys.path.insert(0, "src")

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, average_precision_score

from openssh_anomaly.rules import apply_weak_labels

BG = "#0d1117"
FG = "#c9d1d9"
GRID = "#21262d"
ACCENT_BAD = "#f85149"
ACCENT_OK = "#3fb950"
ACCENT_LINE = "#58a6ff"

plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "axes.edgecolor": GRID,
    "axes.labelcolor": FG,
    "text.color": FG,
    "xtick.color": FG,
    "ytick.color": FG,
    "grid.color": GRID,
    "font.size": 11,
    "font.family": "monospace",
})

df = pd.read_parquet("data/processed/openssh_scored.parquet")
df["weak_label"] = apply_weak_labels(df, fail_threshold=5)
y = df["weak_label"].values
s = df["anom_score"].values

# 1) Score distribution split by weak label
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(s[y == 0], bins=40, alpha=0.75, label="normal (weak label = 0)", color=ACCENT_OK)
ax.hist(s[y == 1], bins=40, alpha=0.75, label="suspicious (weak label = 1)", color=ACCENT_BAD)
ax.set_xlabel("anomaly score (Isolation Forest)")
ax.set_ylabel("event count")
ax.set_title("Anomaly score distribution — OpenSSH events", loc="left", fontweight="bold")
ax.legend(frameon=False)
ax.grid(alpha=0.3)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.tight_layout()
fig.savefig("assets/score_distribution.png", dpi=160)
plt.close(fig)

# 2) Precision-Recall curve
prec, rec, _ = precision_recall_curve(y, s)
ap = average_precision_score(y, s)
fig, ax = plt.subplots(figsize=(6.5, 5))
ax.plot(rec, prec, color=ACCENT_LINE, linewidth=2)
ax.fill_between(rec, prec, alpha=0.15, color=ACCENT_LINE)
ax.set_xlabel("recall")
ax.set_ylabel("precision")
ax.set_title(f"Precision–Recall vs. weak labels  (PR-AUC = {ap:.3f})", loc="left", fontweight="bold")
ax.grid(alpha=0.3)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.tight_layout()
fig.savefig("assets/pr_curve.png", dpi=160)
plt.close(fig)

# 3) Timeline of anomaly scores with flagged events highlighted
d = df.sort_values("timestamp")
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.scatter(d.loc[d.weak_label == 0, "timestamp"], d.loc[d.weak_label == 0, "anom_score"],
           s=6, color=ACCENT_OK, alpha=0.4, label="normal")
ax.scatter(d.loc[d.weak_label == 1, "timestamp"], d.loc[d.weak_label == 1, "anom_score"],
           s=14, color=ACCENT_BAD, alpha=0.85, label="suspicious (weak label)")
ax.set_xlabel("time")
ax.set_ylabel("anomaly score")
ax.set_title("Anomaly score timeline — flagged SSH activity stands out", loc="left", fontweight="bold")
ax.legend(frameon=False, loc="upper right")
ax.grid(alpha=0.3)
fig.autofmt_xdate()
for spine in ax.spines.values():
    spine.set_visible(False)
fig.tight_layout()
fig.savefig("assets/score_timeline.png", dpi=160)
plt.close(fig)

print(f"OK — PR-AUC={ap:.4f}, n={len(df)}, positives={int(y.sum())}")
