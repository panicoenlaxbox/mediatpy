from typing import Awaitable, Callable, Type

from mediatpy import Mediator, NotificationHandler, PipelineBehavior, RequestHandler


def create_mediator(
    request_handler_factory: Callable[[Type[RequestHandler]], Awaitable[RequestHandler]] | None = None,
    pipeline_behavior_factory: Callable[[Type[PipelineBehavior]], Awaitable[PipelineBehavior]] | None = None,
    notification_handler_factory: Callable[[Type[NotificationHandler]], Awaitable[NotificationHandler]] | None = None,
    raise_error_if_not_any_registered_notification_handler: bool = False,
) -> Mediator:
    return Mediator(
        request_handler_factory,
        pipeline_behavior_factory,
        notification_handler_factory,
        raise_error_if_not_any_registered_notification_handler,
    )
