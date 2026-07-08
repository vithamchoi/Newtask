.PHONY: install init load run test power postprocess analyse clean

install:
	python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

init:
	python -m backend.db --init

load:
	python -m backend.db --load stimuli/stimuli_pool.json

run:
	FLASK_APP=backend.app flask run --debug

test:
	pytest -q tests/

power:
	python analysis/power_analysis.py --out analysis/power_curve.csv

postprocess:
	python analysis/postprocess.py --db data/raw/study.db --out data/processed/

analyse: postprocess
	Rscript analysis/mixed_effects.R data/processed/trials.csv data/processed/tlx.csv analysis/results/
	python analysis/calibration.py --trials data/processed/trials.csv --out analysis/results/
	python analysis/effect_sizes.py --trials data/processed/trials.csv --tlx data/processed/tlx.csv --out analysis/results/effect_sizes.json
	python analysis/plots.py --trials data/processed/trials.csv --tlx data/processed/tlx.csv --out analysis/results/figs/

clean:
	rm -rf .venv data/raw/*.db data/processed/* analysis/results/* analysis/power_curve.csv
