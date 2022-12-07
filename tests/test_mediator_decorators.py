from typing import Awaitable, Callable

from assertpy import assert_that

from mediatpy import NotificationHandler, PipelineBehavior, RequestHandler
from tests.test_data.create_mediator import create_mediator
from tests.test_data.my_notification import MyNotification
from tests.test_data.my_request import MyRequest
from tests.test_data.my_response import MyResponse

mediator = create_mediator()


@mediator.request_handler
class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest) -> MyResponse:
        return MyResponse("test")


@mediator.pipeline_behavior
class MyPipelineBehavior(PipelineBehavior[MyRequest, MyResponse]):
    async def handle(self, request: MyRequest, next_behavior: Callable[..., Awaitable[MyResponse]]) -> MyResponse:
        response = await next_behavior()
        response.add_data("test", "test")
        return response


@mediator.notification_handler
class MyNotificationHandler(NotificationHandler[MyNotification]):
    async def handle(self, notification: MyNotification) -> None:
        notification.add_data("test", "test")


async def test_when_a_request_handler_is_decorated_then_is_executed_with_no_manual_registration() -> None:
    response = await mediator.send(MyRequest())

    assert_that(response.result).is_equal_to("test")


async def test_when_a_pipeline_behavior_is_decorated_then_is_executed_with_no_manual_registration() -> None:
    response = await mediator.send(MyRequest())

    assert_that(response.result).is_equal_to("test")
    assert_that(response.data).is_length(1)
    assert_that(response.data["test"]).is_equal_to("test")


async def test_when_a_notification_handler_is_decorated_then_is_executed_with_no_manual_registration() -> None:
    notification = MyNotification()

    await mediator.publish(notification)

    assert_that(notification.data.keys()).is_length(1)
    assert_that(notification.data["test"]).is_equal_to("test")
