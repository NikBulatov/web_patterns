from typing import Iterable
import views
import middlewares


class Framework:
    def __init__(
        self, routes: dict, fronts: Iterable[callable] = middlewares.middlewares
    ):
        self.routes = routes
        self.fronts = fronts

    def _parse_data(self, path: str):
        path = self._add_backslash(path)

    def __has_query_params(self, path) -> bool:
        return "?" in path

    def _parse_input_params(self, path: str = None):
        if path:
            params = path.split("?")[-1]
            data = params.split("&")
            for param in data:
                key, value = param.split("=")
                print(key, value)


    def _add_backslash(self, path: str) -> str:
        """
        Checks for backslash at the end of a path.
        In case of its absence, adds it to the end and returns

        :param path: endpoint
        :return:
        """
        if not self.__has_query_params(path):
            last_symbol = path[-1]
            return path + "/" if last_symbol != "/" else path

    def __call__(self, environ: dict, start_response: callable):
        """
        :param environ: data dict by WSGI connector
        :param start_response: response function by server
        """

        path = self._add_backslash(environ["PATH_INFO"])
        environ["PATH_INFO"] = path
        if path in self.routes:
            view = self.routes[path]
        else:
            view = views.not_found_404_view

        request = {}

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
