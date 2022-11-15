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