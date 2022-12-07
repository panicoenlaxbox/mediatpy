REPR
====

The *REPR Design Pattern (Request, EndPoint, Response)* is the typical usage of mediatpy.

Request/Response
----------------

.. code-block:: python

    class MyResponse:
        pass

    class MyRequest(Request[MyResponse]):
        pass

In both the :class:`mediatpy.Request` and the :class:`mediatpy.Response` you can define any number of attributes.

Response
^^^^^^^^

It's not necessary to explicitly declare a response, you could use any type as the response of your :class:`mediatpy.RequestHandler`.

Command
^^^^^^^^

If you declare the :class:`mediatpy.RequestHandler` to return `None`, you will get a canonical command.

EndPoint
--------

Then, you must create a :class:`mediatpy.RequestHandler` to manage the :class:`mediatpy.Request` and return the expected :class:`mediatpy.Response`.

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

Example
-------

.. code-block:: python

    import asyncio

    from mediatpy import Request, RequestHandler, Mediator


    class MyResponse:
        pass


    class MyRequest(Request[MyResponse]):
        pass

    mediator = Mediator()

    @mediator.request_handler
    class MyRequestHandler(RequestHandler[MyRequest, MyResponse]):
        async def handle(self, request: MyRequest) -> MyResponse:
            return MyResponse()


    async def main():
        request = MyRequest()
        response = await mediator.send(request)
        assert isinstance(response, MyResponse)


    if __name__ == '__main__':
        asyncio.run(main())