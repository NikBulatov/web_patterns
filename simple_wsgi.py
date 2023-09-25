def application(environ, start_response):
    """
    :param environ: словарь данных от сервера
    :param start_response: функция для ответа серверу
    """
    start_response("200 OK", [("Content-Type", "text/html")])
    return [b"Hello world from a simple WSGI application!"]
