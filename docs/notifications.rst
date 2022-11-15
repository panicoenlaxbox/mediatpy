Notifications
=============

You can trigger a :class:`mediatpy.Notification` and it will be processed for any number of registered :class:`mediatpy.NotificationHandler`.

By default, you can trigger a :class:`mediatpy.Notification` that isn't handled by any :class:`mediatpy.NotificationHandler`. If you want to raise and error if :class:`mediatpy.Notification` it's unhandled, use ``raise_error_if_not_any_registered_notification_handler`` parameter during the creation of :class:`mediatpy.Mediator` instance.

By design, :class:`mediatpy.NotificationHandler` are not guaranteed to be executed in the order they are registered.

As in the case of :class:`mediatpy.PipelineBehavior`, you can use the subtype to handle subtypes as well.

Example
-------

.. code-block:: python

    import asyncio

    from mediatpy import Mediator, Notification, NotificationHandler


    class MyNotification(Notification):
        pass


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