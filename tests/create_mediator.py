from typing import Callable, Type

from mediator import Mediator, NotificationHandler, PipelineBehavior, RequestHandler


def create_mediator(
    request_handler_factory: Callable[[Type[RequestHandler]], RequestHandler] = None,
    pipeline_behavior_factory: Callable[[Type[PipelineBehavior]], PipelineBehavior] = None,
    notification_handler_factory: Callable[[Type[NotificationHandler]], NotificationHandler] = None,
    raise_error_if_not_any_registered_notification_handler: bool = False,
) -> Mediator:
    return Mediator(
        request_handler_factory,
        pipeline_behavior_factory,
        notification_handler_factory,
        raise_error_if_not_any_registered_notification_handler,
    )
