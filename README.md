[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
![Upload Python Package](https://github.com/panicoenlaxbox/mediatpy/actions/workflows/python-publish.yml/badge.svg)
<a href="https://twitter.com/intent/follow?screen_name=panicoenlaxbox">
    <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/panicoenlaxbox?style=social">
</a>

# Introduction

This library is "almost" a port of [Mediatr](https://github.com/jbogard/MediatR).

> I say "almost" because along the way, I've made some decisions that seemed right to me.

# Usage

First, install package:

`pip install mediatpy`

## Request Handler

### Create a Request

You must create a `Request` and define what Response will return.

In this example, both `Request` and Response has no data, but of course, you can define whatever attributes you want.

```python
class MyResponse:
    ...
    
class MyRequest(Request[MyResponse]):
    ...
```

### Create a Request Handler

Then, you must create a `RequestHandler` to manage the `Request` and return the expected Response.

```python
class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest) -> MyResponse:
        return MyResponse()
```

### Register Request Handler

With an instance of `Mediator`, you can use `register_request_handler`.

```python
mediator = Mediator()
mediator.register_request_handler(MyRequestHandler)
```

### Use them all together

```python
import asyncio

from mediatpy import Request, RequestHandler, Mediator


class MyResponse:
    ...


class MyRequest(Request[MyResponse]):
    ...


class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest) -> MyResponse:
        return MyResponse()


async def main():
    mediator = Mediator()
    mediator.register_request_handler(MyRequestHandler)
    request = MyRequest()
    response = await mediator.send(request)
    assert isinstance(response, MyResponse)


if __name__ == '__main__':
    asyncio.run(main())
```

### Decorator

If you prefer, you can use a python decorator to associate in a more declarative way the `RequestHandler`.

```python
import asyncio

from mediatpy import Request, RequestHandler, Mediator


class MyResponse:
    ...


class MyRequest(Request[MyResponse]):
    ...


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

## Typing

The library has been created using [generics](https://docs.python.org/3.10/library/typing.html#building-generic-types) and using [mypy](http://mypy-lang.org/) to validate types. This means, that you will have autocomplete in editors that support it.

![image](https://raw.githubusercontent.com/panicoenlaxbox/mediatpy/main/docs/IntelliSense.png)

## Pipeline Behavior

You can create a pipeline where both, before and after `RequestHandler` execution, execute whatever number of `PipelineBehavior` you define.

### Create a Pipeline Behavior

```python
import asyncio
from typing import Callable, Awaitable

from mediatpy import Request, RequestHandler, Mediator, PipelineBehavior


class MyResponse:
    ...


class MyRequest(Request[MyResponse]):
    ...


mediator = Mediator()


@mediator.request_handler
class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest) -> MyResponse:
        print(self.__class__.__name__)
        return MyResponse()


@mediator.pipeline_behavior
class MyPipelineBehavior(PipelineBehavior[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest, next_behavior: Callable[..., Awaitable[MyResponse]]) -> MyResponse:
        print(f"Before {self.__class__.__name__}")
        response = await next_behavior()
        print(f"After {self.__class__.__name__}")
        return response


async def main():
    request = MyRequest()
    await mediator.send(request)


if __name__ == '__main__':
    asyncio.run(main())
```

Which writes the following to the standard output:

```text
Before MyPipelineBehavior
MyRequestHandler
After MyPipelineBehavior
```

### More Pipeline Behaviors

You can define more `PipelineBehavior` and even define some of them with a supertype to catch all of the executions of their subtypes. Moreover, you can be sure that the execution order of `PipelineBehavior` will be the expected right.

For example, `MyGenericPipelineBehavior` is defined before `MyPipelineBehavior` and it's using `Request` instead of `MyRequest` in their definition, so it will be executed for `Request` and for all their subtypes as `MyRequest`.

```python
@mediator.pipeline_behavior
class MyGenericPipelineBehavior(PipelineBehavior[Request, MyResponse]):  # Request instead of MyRequest
    async def handle(self, request: MyRequest, next_behavior: Callable[..., Awaitable[MyResponse]]) -> MyResponse:
        print(f"Before {self.__class__.__name__}")
        response = await next_behavior()
        print(f"After {self.__class__.__name__}")
        return response


@mediator.pipeline_behavior
class MyPipelineBehavior(PipelineBehavior[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest, next_behavior: Callable[..., Awaitable[MyResponse]]) -> MyResponse:
        print(f"Before {self.__class__.__name__}")
        response = await next_behavior()
        print(f"After {self.__class__.__name__}")
        return response
```

```text
Before MyGenericPipelineBehavior
Before MyPipelineBehavior
MyRequestHandler
After MyPipelineBehavior
After MyGenericPipelineBehavior
```

## Notification

Last but not least, you can trigger a `Notification` and it will be processed for any number of registered `NotificationHandler`.

By default, you can trigger a `Notification` that isn't handled by any `NotificationHandler`. If you want to raise and error if `Notification` it's unhandled, use `raise_error_if_not_any_registered_notification_handler` parameter during the creation of `Mediator` instance.

By design, `NotificationHandler` are not guaranteed to be executed in the order they are registered.

As in the case of `PipelineBehavior`, you can use the subtype to handle subtypes as well.

```python
import asyncio

from mediatpy import Mediator, Notification, NotificationHandler


class MyNotification(Notification):
    ...


mediator = Mediator()


@mediator.register_notification_handler
class MyNotificationHandler(NotificationHandler[MyNotification]):
    async def handle(self, notification: MyNotification) -> None:
        print(self.__class__.__name__)


@mediator.register_notification_handler
class MyGenericNotificationHandler(NotificationHandler[Notification]):
    async def handle(self, notification: Notification) -> None:
        # You could use isinstance if you want...
        if isinstance(notification, MyNotification):
            print(self.__class__.__name__)


async def main():
    notification = MyNotification()
    await mediator.publish(notification)


if __name__ == '__main__':
    asyncio.run(main())
```

```text
MyNotificationHandler
MyGenericNotificationHandler
```

## Dependency Injection

`Mediator` does not know anything about third-party dependency containers, but for easing its integration with them, it supplies optional parameters in its constructor that you can use to create (or maybe delegate) objects when they are needed.

```python
import asyncio
from typing import Type

from mediatpy import Mediator, Notification, NotificationHandler


class MyNotification(Notification):
    ...


def my_custom_notification_handler_factory(notification_handler: Type[NotificationHandler]) -> NotificationHandler:
    # Here you could delegate to the container or do anything else to create the requested object
    return notification_handler()


mediator = Mediator(notification_handler_factory=my_custom_notification_handler_factory)


@mediator.register_notification_handler
class MyNotificationHandler(NotificationHandler[MyNotification]):
    async def handle(self, notification: MyNotification) -> None:
        print(self.__class__.__name__)


async def main():
    notification = MyNotification()
    await mediator.publish(notification)


if __name__ == '__main__':
    asyncio.run(main())
```
