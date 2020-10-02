  
#!/bin/bash

export REQ_FILE = requirements.txt
export PROJECT_DIR = redgiant
export TEST_DIR = tests
export REDGIANT_VERSION = 0.0.0

#############################################################
#              Commands for Python environment              #
#############################################################


.PHONY: py-init
py-init:
	if [[ -d ./venv ]]; then rm -rf venv; fi \
	&& python3.6 -m venv venv \
	&& . venv/bin/activate \
	&& pip install --upgrade pip setuptools wheel --progress-bar off \
	&& pip install -r ${REQ_FILE} --progress-bar off


.PHONY: requirements
requirements:
	if [[ -f ${REQ_FILE} ]]; then rm -f ${REQ_FILE}; fi \
	&& . venv/bin/activate \
	&& pip freeze | grep 'redgiant' -v > ${REQ_FILE}


.PHONY: update
update:
	. venv/bin/activate \
	&& pip install --upgrade pip setuptools wheel


.PHONY: install
install:
	pip install -e .


#############################################################
#              Commands for testing                         #
#############################################################


.PHONY: lint
lint:
	. venv/bin/activate \
	&& python -m flake8 ${PROJECT_DIR} ${TEST_DIR}


.PHONY: test
test:
	. venv/bin/activate \
	&& python -m pytest ${TEST_DIR} -p no:warnings -s


.PHONY: qa
qa:
	make test
	make lint


#############################################################
#              Build and Distribution                       #
#############################################################


.PHONY: build
build:
	. venv/bin/activate \
	&& python setup.py sdist bdist_wheel


.PHONY: release
release:
	. venv/bin/activate \
	&& python ./bin/release.py --version ${REDGIANT_VERSION}
