# bio-tarball-to-fastqgz

Tool to extract fastq files from complicated tarballs and provide them as standard gzipped fastq files with metadata as json.

## Installation

```sh
pip install .
```

## Development

* Clone this repository
* Requirements:
  * Python >= 3.9
  * Tox
* `make venv` to create a virtualenv
* `source .venv/bin/activate` to activate new virtualenv
* `make init` to install dependencies and pre-commit hooks
