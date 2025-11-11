.PHONY: setup lint format test data prepare train predict eval demo

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

lint:
	ruff check src tests
	black --check src tests

format:
	black src tests
	ruff check --fix src tests

test:
	pytest -q

data:
	@echo "Coloca los datos OpenSSH en data/raw/ (ver README)."

prepare:
	python -m openssh_anomaly.cli prepare --config configs/base.yaml

train:
	python -m openssh_anomaly.cli train --config configs/base.yaml

predict:
	python -m openssh_anomaly.cli predict --config configs/base.yaml

eval:
	python -m openssh_anomaly.cli eval --config configs/base.yaml

demo: prepare train eval
