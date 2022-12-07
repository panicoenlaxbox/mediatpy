from typing import Callable, Optional, Type

from mediatpy import Mediator, NotificationHandler, PipelineBehavior, RequestHandler


def create_mediator(
    request_handler_factory: Optional[Callable[[Type[RequestHandler]], RequestHandler]] = None,
    pipeline_behavior_factory: Optional[Callable[[Type[PipelineBehavior]], PipelineBehavior]] = None,
    notification_handler_factory: Optional[Callable[[Type[NotificationHandler]], NotificationHandler]] = None,
    raise_error_if_not_any_registered_notification_handler: bool = False,
) -> Mediator:
    return Mediator(
        request_handler_factory,
        pipeline_behavior_factory,
        notification_handler_factory,
        raise_error_if_not_any_registered_notification_handler,
    )
