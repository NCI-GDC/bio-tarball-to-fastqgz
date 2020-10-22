#!/bin/sh

case "$1" in
	test) python -m pytest tests;;
	*version) python -m python_project --version;;
	*) python -m python_project $@;;
esac
