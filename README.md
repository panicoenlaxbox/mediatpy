[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
![Upload Python Package](https://github.com/panicoenlaxbox/mediatpy/actions/workflows/python-publish.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/panicoenlaxbox/mediatpy/badge.svg?branch=main)](https://coveralls.io/github/panicoenlaxbox/mediatpy?branch=main)
[![Documentation Status](https://readthedocs.org/projects/mediatpy/badge/?version=latest)](https://mediatpy.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/mediatpy.svg)](https://badge.fury.io/py/mediatpy)

# Introduction

This library is a port of [Mediatr](https://github.com/jbogard/MediatR) in Python.

For more information and usage instructions, see the [documentation](https://mediatpy.readthedocs.io/en/latest/).

# Usage

`pip install mediatpy`

```python
import asyncio

from mediatpy import Request, RequestHandler, Mediator


class MyResponse:
    pass


class MyRequest(Request[MyResponse]):
    pass


mediator = Mediator()


@mediator.request_handler
class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest) -> MyResponse:
        return MyResponse()


async def main():
    request = MyRequest()
    response = await mediator.send(request)
    assert isinstance(response, MyResponse)


if __name__ == '__main__':
    asyncio.run(main())
```

# Development

The easiest way to set up the development environment is by using `pipx` and `poetry`.

To install [pipx](https://pipx.pypa.io/en/stable/installation/):

```powershell
py -m pip install --user pipx
.\pipx.exe ensurepath
```

To install [poetry](https://python-poetry.org/docs/#installation):

```
pipx install poetry
```

Now you can clone the repository and navigate to the project root directory and execute the following commands:

```bash
poetry install
poetry run pre-commit install
```

# Documentation

Documentation is hosted on [Read the Docs](https://mediatpy.readthedocs.io/en/latest/) and is built automatically upon each commit to the main branch using the `.readthedocs.yml` file.

If you want to build the documentation locally, you can do so by installing the dependencies with 
`pip install -r docs/requirements.txt` and executing `.\make.bat html` from `docs` directory.

# Codex

To facilitate the installation of project dependencies by Codex, a `requirements-codex.txt` file has been generated using the following command:

```bash
poetry export -f requirements.txt --with dev --without-hashes -o requirements-codex.txt
```

In order for this command to work, you need to have the `poetry-plugin-export` plugin installed. You can do it by running:

```bash
poetry self add poetry-plugin-export
```

## Setup script

Once we have this file available, the Setup script for Codex would be the following:

```bash
pip install -r requirements-codex.txt
```