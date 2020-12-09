#!/bin/sh

case "$1" in
	test) python -m pytest tests;;
	*version) python -m tarball_to_fastqgz --version;;
	*) python -m tarball_to_fastqgz $@;;
esac
