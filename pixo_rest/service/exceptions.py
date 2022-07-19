from requests.exceptions import ConnectionError


class BadConfig(Exception):
    ...


class PixooConnectionError(ConnectionError):
    def __init__(self, name: str):
        self.name = name
