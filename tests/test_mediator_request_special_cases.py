from assertpy import assert_that

from mediatpy import RequestHandler
from tests.test_data.create_mediator import create_mediator
from tests.test_data.my_request import MyRequest


class RequestHandlerWithNoUserDefinedClassAsResponse(RequestHandler[MyRequest, list[str]]):
    async def handle(self, request: MyRequest) -> list[str]:
        return ["foo", "bar"]


class RequestHandlerWithNoResponse(RequestHandler[MyRequest, None]):
    async def handle(self, request: MyRequest) -> None:
        ...


async def test_when_a_request_with_no_user_defined_class_as_response_is_sent_then_is_managed_by_a_request_handler() -> None:  # noqa: E501
    mediator = create_mediator()
    mediator.register_request_handler(RequestHandlerWithNoUserDefinedClassAsResponse)

    response = await mediator.send(MyRequest())

    assert_that(response).is_equal_to(["foo", "bar"])


async def test_when_a_request_with_no_response_is_sent_then_is_managed_by_a_request_handler() -> None:
    mediator = create_mediator()
    mediator.register_request_handler(RequestHandlerWithNoResponse)

    response = await mediator.send(MyRequest())

    assert_that(response).is_none()
