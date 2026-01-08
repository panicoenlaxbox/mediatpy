# mediatpy

A lightweight mediator implementation for Python inspired by [MediatR](https://github.com/jbogard/MediatR). It helps you decouple request/response flows and event-style notifications with minimal boilerplate.

## Install

```bash
pip install mediatpy
```

## Quickstart (Request/Response)

Define a request type and a handler, register it on a `Mediator`, then send the request.

```python
import asyncio

from mediatpy import Mediator, Request, RequestHandler


class GetUser:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


class UserResponse:
    def __init__(self, name: str) -> None:
        self.name = name


class GetUserRequest(Request[UserResponse]):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


mediator = Mediator()


@mediator.request_handler
class GetUserHandler(RequestHandler[GetUserRequest, UserResponse]):
    async def handle(self, request: GetUserRequest) -> UserResponse:
        return UserResponse(name=f"User {request.user_id}")


async def main() -> None:
    response = await mediator.send(GetUserRequest(42))
    print(response.name)


if __name__ == "__main__":
    asyncio.run(main())
```

## Notifications (Publish/Subscribe)

Use notifications to broadcast events to one or more handlers.

```python
import asyncio

from mediatpy import Mediator, Notification, NotificationHandler


class UserCreated(Notification):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


mediator = Mediator()


@mediator.notification_handler
class SendWelcomeEmail(NotificationHandler[UserCreated]):
    async def handle(self, notification: UserCreated) -> None:
        print(f"Welcome email for {notification.user_id}")


@mediator.notification_handler
class LogUserCreation(NotificationHandler[UserCreated]):
    async def handle(self, notification: UserCreated) -> None:
        print(f"User {notification.user_id} created")


async def main() -> None:
    await mediator.publish(UserCreated(42))


if __name__ == "__main__":
    asyncio.run(main())
```

## Pipeline Behaviors

Pipeline behaviors wrap request handling to implement cross-cutting concerns (logging, validation, etc.).

```python
from mediatpy import Mediator, PipelineBehavior, Request, RequestHandler


class Ping(Request[str]):
    pass


mediator = Mediator()


@mediator.pipeline_behavior
class LoggingBehavior(PipelineBehavior[Ping, str]):
    async def handle(self, request: Ping, next_behavior):
        print("before")
        result = await next_behavior()
        print("after")
        return result


@mediator.request_handler
class PingHandler(RequestHandler[Ping, str]):
    async def handle(self, request: Ping) -> str:
        return "pong"
```

## Custom Factories

Provide factories if you want dependency injection or custom handler construction.

```python
from mediatpy import Mediator, RequestHandler


async def handler_factory(handler_type: type[RequestHandler]) -> RequestHandler:
    return handler_type()


mediator = Mediator(request_handler_factory=handler_factory)
```

## More

Full documentation: https://mediatpy.readthedocs.io/en/latest/
