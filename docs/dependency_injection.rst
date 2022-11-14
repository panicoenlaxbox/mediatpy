Dependency injection
====================

:class:`mediatpy.Mediator` class does not know anything about third-party dependency containers, but for easing its integration with them, it supplies optional parameters in its constructor that you can use to create (or maybe delegate) objects when they are needed.

.. code-block:: python

    import asyncio
    from typing import Type

    from mediatpy import Mediator, Notification, NotificationHandler


    class MyNotification(Notification):
        ...


    def my_custom_notification_handler_factory(notification_handler: Type[NotificationHandler]) -> NotificationHandler:
        # Here you could delegate to the container or do anything else to create the requested object
        return notification_handler()


    mediator = Mediator(notification_handler_factory=my_custom_notification_handler_factory)


    @mediator.register_notification_handler
    class MyNotificationHandler(NotificationHandler[MyNotification]):
        async def handle(self, notification: MyNotification) -> None:
            print(self.__class__.__name__)


    async def main():
        notification = MyNotification()
        await mediator.publish(notification)


    if __name__ == '__main__':
        asyncio.run(main())

    .. code-block:: python

        import asyncio

        from mediatpy import Mediator, Notification, NotificationHandler


        class MyNotification(Notification):
            ...


        mediator = Mediator()


        @mediator.register_notification_handler
        class MyNotificationHandler(NotificationHandler[MyNotification]):
            async def handle(self, notification: MyNotification) -> None:
                print(self.__class__.__name__)


        @mediator.register_notification_handler
        class MyGenericNotificationHandler(NotificationHandler[Notification]):
            async def handle(self, notification: Notification) -> None:
                # You could use isinstance if you want...
                if isinstance(notification, MyNotification):
                    print(self.__class__.__name__)


        async def main():
            notification = MyNotification()
            await mediator.publish(notification)


        if __name__ == '__main__':
            asyncio.run(main())