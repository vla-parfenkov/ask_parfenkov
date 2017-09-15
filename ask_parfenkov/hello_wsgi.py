from pprint import pformat
from cgi import parse_qsl

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    str = "Hello world!\n"
    return [str]

def app(environ, start_response):
    str = ""
    if environ.get("REQUEST_METHOD") == 'GET' and environ["QUERY_STRING"]:
        str += environ["QUERY_STRING"]
        print("Get = ", str)
    if environ["REQUEST_METHOD"] == 'POST' and environ["wsgi.input"]:
        str += environ["wsgi.input"].read()
        print("Post = ", str)
    status = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    return [str]


