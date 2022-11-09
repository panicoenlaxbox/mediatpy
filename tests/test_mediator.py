from typing import Awaitable, Callable
from unittest.mock import MagicMock

import pytest
from assertpy import assert_that

from mediator import (
    NoRequestHandlerFoundError,
    NotAnyNotificationHandlerFoundError,
    Notification,
    NotificationHandler,
    PipelineBehavior,
    Request,
    RequestHandler,
)
from tests.create_mediator import create_mediator
from tests.my_notification import MyNotification
from tests.my_request import MyRequest
from tests.my_response import MyResponse


class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest) -> MyResponse:
        return MyResponse("test")


class OtherRequestHandler(RequestHandler[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest) -> MyResponse:
        return MyResponse("other_test")


class MyPipelineBehavior(PipelineBehavior[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest, next_behavior: Callable[..., Awaitable[MyResponse]]) -> MyResponse:
        response = await next_behavior()
        response.add_data("test", "test")
        return response


class OtherPipelineBehavior(PipelineBehavior[Request, MyResponse]):
    async def handle(self, request: Request, next_behavior: Callable[..., Awaitable[MyResponse]]) -> MyResponse:
        response = await next_behavior()
        response.add_data("other_test", "other_test")
        return response


class MyNotificationHandler(NotificationHandler[MyNotification]):
    async def handle(self, notification: MyNotification) -> None:
        notification.add_data("test", "test")


class OtherNotificationHandler(NotificationHandler[Notification]):
    async def handle(self, notification: Notification) -> None:
        if isinstance(notification, MyNotification):
            notification.add_data("other_test", "other_test")


async def test_when_there_is_no_registered_request_handler_then_an_error_is_thrown() -> None:
    mediator = create_mediator()
    request = MyRequest()
    with pytest.raises(NoRequestHandlerFoundError) as excinfo:
        await mediator.send(request)

    assert_that(excinfo.value.request).is_equal_to(request)


async def test_when_a_request_is_sent_then_is_managed_by_a_request_handler() -> None:
    mediator = create_mediator()
    mediator.register_request_handler(MyRequestHandler)

    response = await mediator.send(MyRequest())

    assert_that(response.result).is_equal_to("test")


async def test_when_register_two_request_handlers_for_the_same_request_then_only_the_last_registered_is_executed() -> None:  # noqa: E501
    mediator = create_mediator()
    mediator.register_request_handler(MyRequestHandler)
    mediator.register_request_handler(OtherRequestHandler)

    response = await mediator.send(MyRequest())

    assert_that(response.result).is_equal_to("other_test")


async def test_when_a_request_is_sent_with_a_pipeline_behavior_then_behavior_and_request_handler_are_executed() -> None:
    mediator = create_mediator()
    mediator.register_request_handler(MyRequestHandler)
    mediator.register_pipeline_behavior(MyPipelineBehavior)

    response = await mediator.send(MyRequest())

    assert_that(response.result).is_equal_to("test")
    assert_that(response.data).is_length(1)
    assert_that(response.data["test"]).is_equal_to("test")


async def test_when_a_request_is_sent_with_multiple_pipeline_behaviors_then_behaviors_and_request_handler_are_executed_in_right_order() -> None:  # noqa: E501
    mediator = create_mediator()
    mediator.register_request_handler(MyRequestHandler)
    mediator.register_pipeline_behavior(MyPipelineBehavior)
    mediator.register_pipeline_behavior(OtherPipelineBehavior)

    response = await mediator.send(MyRequest())

    assert_that(response.result).is_equal_to("test")
    assert_that(list(response.data.keys())).is_equal_to(["other_test", "test"])
    assert_that(response.data["other_test"]).is_equal_to("other_test")
    assert_that(response.data["test"]).is_equal_to("test")


async def test_when_there_are_no_any_registered_notification_handlers_then_an_error_is_thrown() -> None:
    mediator = create_mediator(raise_error_if_not_any_registered_notification_handler=True)
    notification = MyNotification()
    with pytest.raises(NotAnyNotificationHandlerFoundError) as excinfo:
        await mediator.publish(notification)

    assert_that(excinfo.value.notification).is_equal_to(notification)


async def test_when_there_are_no_any_registered_notification_handlers_and_raise_error_is_not_configured_then_no_error_is_thrown() -> None:  # noqa: E501
    mediator = create_mediator()
    await mediator.publish(MyNotification())


async def test_when_a_notification_is_sent_then_notification_handlers_are_executed() -> None:
    mediator = create_mediator()
    mediator.register_notification_handler(MyNotificationHandler)
    mediator.register_notification_handler(OtherNotificationHandler)
    notification = MyNotification()

    await mediator.publish(notification)

    assert_that(notification.data.keys()).is_length(2)
    assert_that(notification.data["test"]).is_equal_to("test")
    assert_that(notification.data["other_test"]).is_equal_to("other_test")


async def test_when_a_custom_request_handler_factory_is_supplied_then_is_used() -> None:
    mock_custom_request_handler_factory = MagicMock(return_value=MyRequestHandler())
    mediator = create_mediator(request_handler_factory=mock_custom_request_handler_factory)
    mediator.register_request_handler(MyRequestHandler)
    request = MyRequest()

    await mediator.send(request)

    mock_custom_request_handler_factory.assert_called_once_with(MyRequestHandler)


async def test_when_a_custom_pipeline_behavior_factory_is_supplied_then_is_used() -> None:
    mock_custom_pipeline_behavior_factory = MagicMock(return_value=MyPipelineBehavior())
    mediator = create_mediator(pipeline_behavior_factory=mock_custom_pipeline_behavior_factory)
    mediator.register_request_handler(MyRequestHandler)
    mediator.register_pipeline_behavior(MyPipelineBehavior)
    request = MyRequest()

    await mediator.send(request)

    mock_custom_pipeline_behavior_factory.assert_called_once_with(MyPipelineBehavior)


async def test_when_a_custom_notification_handler_factory_is_supplied_then_is_used() -> None:
    mock_custom_notification_handler_factory = MagicMock(return_value=MyNotificationHandler())
    mediator = create_mediator(notification_handler_factory=mock_custom_notification_handler_factory)
    mediator.register_notification_handler(MyNotificationHandler)
    notification = MyNotification()

    await mediator.publish(notification)

    mock_custom_notification_handler_factory.assert_called_once_with(MyNotificationHandler)
