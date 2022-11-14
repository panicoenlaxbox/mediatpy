Getting started
===============

This library is a port of `Mediatr <https://github.com/jbogard/MediatR>`_ in Python.

Currently, it supports :class:`request handlers <mediatpy.RequestHandler>`, :class:`pipeline behaviors <mediatpy.PipelineBehavior>`, and :class:`notifications <mediatpy.NotificationHandler>`.

Installation
------------

``pip install mediatpy``

Usage
-----

.. code-block:: python

    import asyncio

    from mediatpy import Request, RequestHandler, Mediator


    class MyResponse:
        ...


    class MyRequest(Request[MyResponse]):
        ...


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