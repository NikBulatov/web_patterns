from typing import Iterable
import views
import middlewares


class Framework:
    def __init__(
        self, routes: dict, fronts: Iterable[callable] = middlewares.middlewares
    ):
        self.routes = routes
        self.fronts = fronts

    @staticmethod
    def _parse_get_data(data: str) -> dict:
        """
        Parsing query params by GET request
        :param data:
        :return:
        """
        result = {}
        if data:
            params = data.split("&")
            for param in params:
                key, value = param.split("=")
                result[key] = value
        return result

    @staticmethod
    def __extract_post_data(env: dict) -> bytes:
        """
        Extract data from post request body
        :param env:
        :return:
        """
        content_length_data = env.get("CONTENT_LENGTH")
        content_length = int(content_length_data) if content_length_data else 0
        data = env["wsgi.input"].read(content_length) if content_length > 0 else b""
        return data

    def _parse_post_data(self, data: bytes) -> dict:
        """
        Parse bytes from post request body
        :param data:
        :return:
        """
        result = {}
        if data:
            data_str = data.decode(encoding="utf-8")
            result = self._parse_get_data(data_str)
        return result

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
            print(
                f"Sender's name: {name} Sender E-mail: {email} Message: {message}"
            )

    def __call__(self, environ: dict, start_response: callable):
        """
        :param environ: data dict by WSGI connector
        :param start_response: response function by server
        """

        request = {}
        path = self._add_backslash(environ["PATH_INFO"])
        query_string = environ["QUERY_STRING"]
        method = environ["REQUEST_METHOD"]

        if method == "GET":
            data = self._parse_get_data(query_string)
            request.update(data)
        elif method == "POST":
            data = self._parse_post_data(self.__extract_post_data(environ))
            request.update(data)

        self.show_message(request)

        if path in self.routes:
            view = self.routes[path]
        else:
            view = views.not_found_404_view

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
