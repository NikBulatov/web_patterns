def parse_input_data(data: str) -> dict:
    """
    Parsing query params
    :param data:
    :return:
    """
    result = {}
    if data:
        params = data.split("&")
        for item in params:
            k, v = item.split("=")
            result[k] = v
    return result


class GetRequest:
    @staticmethod
    def get_params(environ: dict) -> dict:
        query_string = environ["QUERY_STRING"]
        request_params = parse_input_data(query_string)
        return request_params


class PostRequest:
    @staticmethod
    def _get_wsgi_input_data(environ: dict) -> bytes:
        """
        Extract data from post request body
        :param environ:
        :return:
        """
        content_length_data = environ.get("CONTENT_LENGTH")
        content_length = int(content_length_data) if content_length_data else 0
        data = environ["wsgi.input"].read(content_length) if content_length > 0 else b""
        return data

    @staticmethod
    def _parse_wsgi_input_data(data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding="utf-8")
            result = parse_input_data(data_str)
        return result

    def get_params(self, environ: dict) -> dict:
        data = self._get_wsgi_input_data(environ)
        data = self._parse_wsgi_input_data(data)
        return data
