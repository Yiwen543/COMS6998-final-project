PYTHON := .venv/bin/python
export PATH := /opt/homebrew/bin:/usr/local/bin:$(PATH)
export CARGO_HOME := $(CURDIR)/.cache/cargo

.PHONY: setup doctor step1 test prompt
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
	$(PYTHON) -m unittest discover -s tests -v

prompt:
	$(PYTHON) scripts/build_prompt.py

.PHONY: cvdp
cvdp:
	$(PYTHON) scripts/vscode_task.py cvdp
