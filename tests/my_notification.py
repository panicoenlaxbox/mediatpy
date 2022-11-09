from mediatpy import Notification


class MyNotification(Notification):
    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    def add_data(self, key: str, value: str) -> None:
        self.data[key] = value
