Notifications
=============

You can trigger a :class:`mediatpy.Notification` and it will be processed for any number of registered :class:`mediatpy.NotificationHandler`.

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