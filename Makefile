#!/bin/bash

install:
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('stopwords'); nltk.download('gutenberg'); nltk.download('state_union'); nltk.download('averaged_perceptron_tagger')"
	
