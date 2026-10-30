PYTHON := .venv/bin/python

.PHONY: setup doctor step1 test prompt clean-generated
setup:
	python3 -m venv .venv
	cargo build --locked --manifest-path egraph/Cargo.toml
	$(PYTHON) scripts/doctor.py

doctor:
	$(PYTHON) scripts/doctor.py

step1:
	$(PYTHON) scripts/run_step1.py
	$(PYTHON) scripts/build_prompt.py

test:
	@mkdir -p build
	cargo build --locked --offline --manifest-path egraph/Cargo.toml
	$(PYTHON) -B -m unittest discover -s tests -v

prompt:
	$(PYTHON) scripts/build_prompt.py

clean-generated:
	$(PYTHON) scripts/clean_generated.py --apply
