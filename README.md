# OpenSky Datashader

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Build Status](https://travis-ci.org/jackdbd/opensky-datashader.svg?branch=master)](https://travis-ci.org/jackdbd/opensky-datashader) [![Code Coverage](https://codecov.io/gh/jackdbd/opensky-datashader/coverage.svg)](https://codecov.io/gh/jackdbd/opensky-datashader) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) 

Snippets that show how to use the OpenSky REST API.

## Installation

:warning: Do **NOT** use the `requirements.txt` file to install the dependencies on your machine. I need to keep it to deploy on Heroku because [Heroku does not yet support poetry](https://github.com/heroku/heroku-buildpack-python/issues/796) (I tried [this buildpack](https://elements.heroku.com/buildpacks/moneymeets/python-poetry-buildpack) but it didn't work).

This project uses [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage the Python virtual environment, and [poetry](https://poetry.eustace.io/) to manage the project dependencies.

If you don't have it, install python `3.8.5`.

```shell
pyenv install 3.8.5
```

Create a virtual environment and activate it.

```shell
pyenv virtualenv 3.8.5 opensky_datashader
pyenv activate opensky_datashader
```

Remember to activate the virtual environment every time you work on this project.

Install all the dependencies from the `poetry.lock` file.

```shell
poetry install
```

## Tests

```sh
pipenv run tests
```


## Data
https://opensky-network.org/


## See also:
https://anaconda.org/jbednar/opensky/notebook

```shell
sudo apt-get install libgeos-dev
sudo apt-get install libproj-dev
```
