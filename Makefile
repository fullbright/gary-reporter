#!/bin/bash
SHELL := /bin/bash

install:
	sudo apt-get install python-virtualenv python-pip -y
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('stopwords'); nltk.download('gutenberg'); nltk.download('state_union'); nltk.download('averaged_perceptron_tagger')"
	python -c "import nltk; nltk.download('punkt');"

venv:
	source .venv/bin/activate

init:
	pip install -r requirements.txt

test:
	py.test tests

.PHONY: init test
	
