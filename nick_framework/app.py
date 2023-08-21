from base64 import decodebytes
from typing import Iterable

import views
import middlewares
from nick_framework.requests import GetRequest, PostRequest


class Framework:
    def __init__(
        self, routes: dict, fronts: Iterable[callable] = middlewares.middlewares
    ):
        self.routes = routes
        self.fronts = fronts

    @staticmethod
    def _decode_value(data: dict) -> dict:
        new_data = {}
        for key, value in data.items():
            data = bytes(value.replace("%", "=").replace("+", " "), "UTF-8")
            decode_data_str = decodebytes(data).decode("UTF-8")
            new_data[key] = decode_data_str
        return new_data

    @staticmethod
    def _add_backslash(path: str) -> str:
        """
        Checks for backslash at the end of a path.
        In case of its absence, adds it to the end and returns

        :param path: endpoint
        :return:
        """

        last_symbol = path[-1]
        return path + "/" if last_symbol != "/" else path

    @staticmethod
    def show_message(data: dict) -> None:
        if data:
            name = data.get("name")
            email = data.get("email")
            message = data.get("message")
            print(f"Sender's name: {name} Sender E-mail: {email} Message: {message}")

    def __call__(self, environ: dict, start_response: callable):
        """
        :param environ: data dict by WSGI connector
        :param start_response: response function by server
        """

        request = {}
        path = self._add_backslash(environ["PATH_INFO"])
        method = environ["REQUEST_METHOD"]

        if method == "GET":
            data = PostRequest().get_params(environ)
            request["data"] = self._decode_value(data)
        elif method == "POST":
            query_params = GetRequest().get_params(environ)
            request["request_params"] = self._decode_value(query_params)

        self.show_message(request)

        if path in self.routes:
            view = self.routes[path]
        else:
            view = views.NotFoundView()

        for middleware in self.fronts:
            middleware(request)

        code, body = view(request)
        start_response(
            code,
            [
                ("Content-Type", "text/html; charset=UTF-8"),
                ("Content-Length", str(len(body))),
            ],
        )

        return [body.encode("utf-8")]
