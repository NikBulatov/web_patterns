from wsgiref.simple_server import make_server
from nick_framework.app import Framework
from views import routes
from middlewares import middlewares

application = Framework(routes, middlewares)


if __name__ == "__main__":
    port = 8000
    with make_server("", port, application) as httpd:
        print(f"Serving on port {port}...")
        httpd.serve_forever()
