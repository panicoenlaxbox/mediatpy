from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cache
from typing import Awaitable, Callable, Coroutine, Generic, Optional, Type, TypeAlias, TypeVar, get_args

TResponse = TypeVar("TResponse")


class Request(Generic[TResponse]):
    """
    Base class for any request
    """

    pass


TRequest = TypeVar("TRequest", bound=Request)


class RequestHandler(ABC, Generic[TRequest, TResponse]):
    """
    Base class for any request handler
    """

    @abstractmethod
    async def handle(self, request: TRequest) -> TResponse:
        pass


class PipelineBehavior(ABC, Generic[TRequest, TResponse]):
    """
    Base class for any pipeline behavior
    """

    @abstractmethod
    async def handle(self, request: TRequest, next_behavior: Callable[..., Awaitable[TResponse]]) -> TResponse:
        """
        Abstract method to handle a request and to return a response

        :param request: Request to be handled
        :param next_behavior: Next pipeline behavior or request handler to execute
        """
        pass


class Notification:
    """
    Base class for any notification
    """

    pass


TNotification = TypeVar("TNotification", bound=Notification)


class NotificationHandler(ABC, Generic[TNotification]):
    """
    Base class for any notification handler
    """

    @abstractmethod
    async def handle(self, notification: TNotification) -> None:
        pass


Handler: TypeAlias = Type[RequestHandler | PipelineBehavior | NotificationHandler]


@dataclass
class _PipelineBehaviorRegistration:
    pipeline_behavior: Type[PipelineBehavior]
    position: int


class NoRequestHandlerFoundError(Exception):
    """
    Error to indicate that a :class:`Request` has not a registered :class:`RequestHandler` to handle it
    """

    def __init__(self, request: Request) -> None:
        self.request = request
        super().__init__(f"There is no registered handler for request {type(request)}.")


class NotAnyNotificationHandlerFoundError(Exception):
    """
    Error to indicate that a :class:`Notification` has not any registered :class:`NotificationHandler` to handle it
    """

    def __init__(self, notification: Notification) -> None:
        self.notification = notification
        super().__init__(f"There are not any registered handler for notification {notification}.")


class Mediator:
    """
    Class to register handlers and coordinate their execution in response to arrivals of requests and notifications

    :param request_handler_factory: Custom :class:`RequestHandler` factory
    :param pipeline_behavior_factory: Custom :class:`PipelineBehavior` factory
    :param notification_handler_factory: Custom :class:`NotificationHandler` factory
    :param raise_error_if_not_any_registered_notification_handler: Raise an error if no :class:`NotificationHandler`
        is found when a :class:`Notification` is published
    """

    def __init__(
        self,
        request_handler_factory: Optional[Callable[[Type[RequestHandler]], RequestHandler]] = None,
        pipeline_behavior_factory: Optional[Callable[[Type[PipelineBehavior]], PipelineBehavior]] = None,
        notification_handler_factory: Optional[Callable[[Type[NotificationHandler]], NotificationHandler]] = None,
        raise_error_if_not_any_registered_notification_handler: bool = False,
    ) -> None:
        self._request_handler_factory = (
            self._default_request_handler_factory if request_handler_factory is None else request_handler_factory
        )
        self._request_handlers: dict[Type[Request], Type[RequestHandler]] = {}
        self._pipeline_behavior_factory = (
            self._default_pipeline_behavior_factory if pipeline_behavior_factory is None else pipeline_behavior_factory
        )
        self._pipeline_behaviors: dict[Type[Request], list[_PipelineBehaviorRegistration]] = {}
        self._pipeline_behavior_position = 0
        self._notification_handler_factory = (
            self._default_notification_handler_factory
            if notification_handler_factory is None
            else notification_handler_factory
        )
        self._notification_handlers: dict[Type[Notification], list[Type[NotificationHandler]]] = {}
        self._raise_error_if_not_any_registered_notification_handler = (
            raise_error_if_not_any_registered_notification_handler
        )

    @staticmethod
    def _default_request_handler_factory(request_handler: Type[RequestHandler]) -> RequestHandler:
        return request_handler()

    @staticmethod
    def _default_pipeline_behavior_factory(pipeline_behavior: Type[PipelineBehavior]) -> PipelineBehavior:
        return pipeline_behavior()

    @staticmethod
    def _default_notification_handler_factory(notification_handler: Type[NotificationHandler]) -> NotificationHandler:
        return notification_handler()

    @staticmethod
    def _get_request_type(handler: Handler) -> Type[Request]:
        return get_args(handler.__orig_bases__[0])[0]  # type: ignore

    @staticmethod
    def _get_notification_type(notification_handler: Type[NotificationHandler]) -> Type[Notification]:
        return get_args(notification_handler.__orig_bases__[0])[0]  # type: ignore

    def request_handler(self, request_handler: Type[RequestHandler]) -> None:
        """
        Decorator to register a :class:`RequestHandler`
        """
        self.register_request_handler(request_handler)

    def pipeline_behavior(self, pipeline_behavior: Type[PipelineBehavior]) -> None:
        """
        Decorator to register a :class:`PipelineBehavior`
        """
        self.register_pipeline_behavior(pipeline_behavior)

    def notification_handler(self, notification_handler: Type[NotificationHandler]) -> None:
        """
        Decorator to register a :class:`NotificationHandler`
        """
        self.register_notification_handler(notification_handler)

    def register_request_handler(self, request_handler: Type[RequestHandler]) -> None:
        """
        Manual registration of a :class:`RequestHandler`
        """
        request = self._get_request_type(request_handler)
        self._request_handlers[request] = request_handler

    def register_notification_handler(self, notification_handler: Type[NotificationHandler]) -> None:
        """
        Manual registration of a :class:`NotificationHandler`
        """
        notification = self._get_notification_type(notification_handler)
        notification_handlers = self._notification_handlers.get(notification, [])
        notification_handlers.append(notification_handler)
        self._notification_handlers[notification] = notification_handlers

    def register_pipeline_behavior(self, pipeline_behavior: Type[PipelineBehavior]) -> None:
        """
        Manual registration of a :class:`PipelineBehavior`
        """
        request = self._get_request_type(pipeline_behavior)
        pipeline_behaviors = self._pipeline_behaviors.get(request, [])
        pipeline_behaviors.append(_PipelineBehaviorRegistration(pipeline_behavior, self._pipeline_behavior_position))
        self._pipeline_behaviors[request] = pipeline_behaviors
        self._pipeline_behavior_position += 1

    async def send(self, request: Request[TResponse]) -> TResponse:
        """
        Send a :class:`Request`

        .. code-block:: python

            my_request = MyRequest()
            await mediator.send(my_request)
        """
        if not type(request) in self._request_handlers:
            raise NoRequestHandlerFoundError(request)
        request_handler = self._create_request_handler(self._request_handlers[type(request)])
        pipeline_behaviors = self._resolve_pipeline_behaviors(request)
        if not any(pipeline_behaviors):
            return await request_handler.handle(request)
        first_pipeline_behavior = self._create_pipeline_behavior(pipeline_behaviors[0].pipeline_behavior)
        next_pipeline_behavior: Callable[..., Awaitable[TResponse]] = self._get_next_pipeline_behavior(
            request, request_handler, pipeline_behaviors, 0
        )
        return await first_pipeline_behavior.handle(request, next_pipeline_behavior)

    async def publish(self, notification: Notification) -> None:
        """
        Publish a :class:`Notification`

        .. code-block:: python

            my_notification = MyNotification()
            await mediator.publish(my_notification)
        """
        notification_handlers = self._resolve_notification_handlers(notification)
        if not any(notification_handlers) and self._raise_error_if_not_any_registered_notification_handler:
            raise NotAnyNotificationHandlerFoundError(notification)

        for notification_handler in notification_handlers:
            await self._create_notification_handler(notification_handler).handle(notification)

    def _create_request_handler(self, request_handler: Type[RequestHandler]) -> RequestHandler:
        return self._request_handler_factory(request_handler)

    def _create_pipeline_behavior(self, pipeline_behavior: Type[PipelineBehavior]) -> PipelineBehavior:
        return self._pipeline_behavior_factory(pipeline_behavior)

    def _create_notification_handler(self, notification_handler: Type[NotificationHandler]) -> NotificationHandler:
        return self._notification_handler_factory(notification_handler)

    @cache
    def _resolve_pipeline_behaviors(self, request: Request) -> list[_PipelineBehaviorRegistration]:
        matching = [value for key, value in self._pipeline_behaviors.items() if issubclass(type(request), key)]
        flattened = [pipeline_behavior for sublist in matching for pipeline_behavior in sublist]
        return sorted(flattened, key=lambda pipeline_behavior: pipeline_behavior.position)

    @cache
    def _resolve_notification_handlers(self, request: Request) -> list[Type[NotificationHandler]]:
        matching = [value for key, value in self._notification_handlers.items() if issubclass(type(request), key)]
        return [notification_handler for sublist in matching for notification_handler in sublist]

    def _get_next_pipeline_behavior(
        self,
        request: Request,
        request_handler: RequestHandler,
        pipeline_behaviors: list[_PipelineBehaviorRegistration],
        index: int,
    ) -> Callable[..., Awaitable[TResponse]]:
        def _() -> Coroutine:
            next_index = index + 1
            is_last_pipeline_behavior = next_index == len(pipeline_behaviors)
            if is_last_pipeline_behavior:
                return request_handler.handle(request)
            else:
                next_pipeline_behavior = pipeline_behaviors[next_index]
                return self._create_pipeline_behavior(next_pipeline_behavior.pipeline_behavior).handle(
                    request, self._get_next_pipeline_behavior(request, request_handler, pipeline_behaviors, next_index)
                )

        return _
