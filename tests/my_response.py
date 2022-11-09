class MyResponse:
    def __init__(self, result: str | None = None):
        self.result = result
        self.data: dict[str, str] = {}

    def add_data(self, key: str, value: str) -> None:
        self.data[key] = value
