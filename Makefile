TOP_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

run:	init
	source ${TOP_DIR}/.venv/bin/activate; \
	cd ${TOP_DIR}; \
	python3 app.py

init:
	if [ ! -d "${TOP_DIR}/.venv/" ]; then \
		python3 -m virtualenv ${TOP_DIR}/.venv/; \
		source ${TOP_DIR}/.venv/bin/activate; \
		pip3 install -r requirements.txt; \
	fi
