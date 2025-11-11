from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import yaml

@dataclass
class ProjectConfig:
    root: Path
    seed: int
    data: Dict[str, Any]
    features: Dict[str, Any]
    model: Dict[str, Any]
    scaling: Dict[str, Any]
    eval: Dict[str, Any]

    @staticmethod
    def load(path: str | Path) -> 'ProjectConfig':
        p = Path(path)
        cfg = yaml.safe_load(p.read_text())
        return ProjectConfig(
            root=Path(cfg.get('project', {}).get('root', '.')),
            seed=int(cfg.get('project', {}).get('seed', 42)),
            data=cfg.get('data', {}),
            features=cfg.get('features', {}),
            model=cfg.get('model', {}),
            scaling=cfg.get('scaling', {}),
            eval=cfg.get('eval', {}),
        )
