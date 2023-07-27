#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from wsgiref.simple_server import make_server
from pprint import pprint

def application(environ: dict, start_response: callable):
    """
    :param environ: data dict by WSGI connector
    :param start_response: response function by server
    """
    pprint(environ)
    start_response("200 OK", [("Content-Type", "text/html")])
    return [b"Hello world from a simple WSGI application!"]


with make_server("", 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
