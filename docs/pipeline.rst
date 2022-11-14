Pipeline
========

An useful feature of mediatpy is that you can build a pipeline of chained behaviors that will be executed, both, before and after a request handler.

Usage
-----

.. code-block:: python

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

    async def main():
        request = MyRequest()
        await mediator.send(request)


    if __name__ == '__main__':
        asyncio.run(main())

    # Before MyGenericPipelineBehavior
    # Before MyPipelineBehavior
    # MyRequestHandler
    # After MyPipelineBehavior
    # After MyGenericPipelineBehavior