REPR
====

The *REPR Design Pattern (Request, EndPoint, Response)* is the typical usage of mediatpy.

Request/Response
----------------

.. code-block:: python

    class MyResponse:
        ...

    class MyRequest(Request[MyResponse]):
        ...

In both the :class:`mediatpy.Request` and the :class:`mediatpy.Response` you can define any number of attributes.

EndPoint
--------

.. code-block:: python

    class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
        async def handle(self, request: MyRequest) -> MyResponse:
            return MyResponse()

Registration
------------

Manually
^^^^^^^^

.. code-block:: python

    mediator = Mediator()
    mediator.register_request_handler(MyRequestHandler)

Decorator
^^^^^^^^^

.. code-block:: python

    @mediator.request_handler
    class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
        async def handle(self, request: MyRequest) -> MyResponse:
            return MyResponse()

Full example
------------

.. code-block:: python

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