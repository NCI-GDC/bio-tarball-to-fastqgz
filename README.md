# Python Project Development

## Developer Environment

All developers should have the ability to have and manage multiple Python installations on their computer.

One way is utilizing the program [pyenv](https://github.com/pyenv/pyenv).

Additionally, all developers should have a way to manage per-project virtual envrionments.

### Python Virtual Environments

It is often the case that a developer will work on multiple Python projects, many of which require different Python versions and different versions of installed dependencies.

Python virtual environments provide self-contained instances of a python version and installed packages, and should be created individually for each project.

There are many utilities to create these virtual environments:

1. `venv`: Built-in virtualenv module. Example: `python3 -m venv -p <path/to/python/binary> venv/` will create a new virtual environment in the `./venv` directory, usable by running `source venv/bin/activate`.
2. `direnv`: A more general utility which can activate different environments based on the current directory.
3. `pyenv-virtualenv`: A plugin for `pyenv` which allows the creation of venvs to use as python installs.

## Project Init

Once the proper virtualenv is created and entered, the next step will be to install required dependencies.

### New Project

If the project is brand new, the dependencies should be added to the `INSTALL_REQUIRES` list in the `setup.py` file.

Then, the `make requirements` command will:
1. Install `pip-tools`
2. Write the dependencies specified in the `setup.py` file to `requirements.in`
3. Run `pip-compile` on the `requirements.in` file to generate the `requirements.txt` file.

### New and Existing Projects

The `make init` command should be run whenever the following files are updated:
1. `requirements.txt`
2. `.pre-commit-config.yml`

This make target will install the pip requirements specified in the `requirements.txt` file, install the python package under development mode, and install `pre-commit` hooks.

## Working with Precommit

The `pre-commit` suite will perform several checks on each commit and push.

Currently these checks include:
1. `check-yaml` and `check-toml`: verifies syntax of respective files
2. `seed-isort-config`: Updates `.isort.cfg` file with known first and third party modules
3. `isort`: Sorts imports on staged files
4. `black`: Autoformats staged files

### Common pre-commit issues

The most common issue with precommit will be that when `isort` or `black` modify a file, those modifications will need to be re-staged for commit.

The output of pre-commit in this case will look like:

```
Check Yaml...........................................(no files to check)Skipped
Check Toml...........................................(no files to check)Skipped
seed isort known_third_party.............................................Passed
isort....................................................................Failed
- hook id: isort
- files were modified by this hook

Fixing /home/charles/dev/github.com/NCI-GDC/variant-filtration-tool/gdc_filtration_tools/__main__.py

black....................................................................Failed
- hook id: black
- files were modified by this hook
```

This shows that the `__main__.py` file was modified. If `git status` is run, it will show both that this file is staged for commit and is ready for staging. Simply re-stage the file `git add <file>` and re-commit, and the checks should then pass.

Another common issue occurs when a brand-new import is used in a module.

This will trigger `seed-isort-config` to update `.isort.cfg` on commit, and return a fail status.

The developer must add the `.isort.cfg` file to the current commit and re-commit.

### Precommit on VMs

When `pre-commit` is first run, even during a `git commit`, it will attempt to download and set up the repos specified in the config.

However, this will fail when on the VM due to needing to specify the proxies.

Before commiting, try to run `with_proxy pre-commit run`.

Otherwise, manually specify the proxy urls before the `git commit` command:

`HTTP_PROXY="" HTTPS_PROXY="" git commit ...`
