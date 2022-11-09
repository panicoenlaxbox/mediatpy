from mediatpy import Request
from tests.my_response import MyResponse


class MyRequest(Request[MyResponse]):
    def __init__(self, q: str | None = None):
        self.q = q
        self.data: dict[str, str] = {}

    def add_data(self, key: str, value: str) -> None:
        self.data[key] = value
