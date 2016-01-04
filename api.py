import json
import signal
import sys

from tornado.httpserver import HTTPServer
from tornado.httputil import HTTPHeaders
import tornado.ioloop
from tornado.options import define, options
from  tornado.web import URLSpec

from orders import Book, Buy, Sell
import constants

try:
    from httplib import responses   # py2
except ImportError:
    from http.client import responses   # py3

define("port", default=3000, help="run on the given port", type=int)


class BookHandler(tornado.web.RequestHandler):
    """
    Handle GET requests to /book API endpoint.
    """
    def get(self):
        ret = Book().orders()
        self.write(ret)


class OrderHandler(tornado.web.RequestHandler):
    """
    Handle POST requests to /buy and /sell API endpoints.
    """
    def post(self, **kwargs):
        order = None
        resp = None
        body = json.loads(self.request.body)
        if self.request.uri == "{}".format(constants.URL_PATH_BUY):
            order = Buy(**body)
        if self.request.uri == "{}".format(constants.URL_PATH_SELL):
            order = Sell(**body)
        if not order.is_valid():
            resp = {"message": responses[constants.HTTP_400_BAD_REQUEST]}
            self.set_status(constants.HTTP_400_BAD_REQUEST)
            self.write(resp)
            return
        try:
            resp = Book().match(order)
            http_status_code = constants.HTTP_201_CREATED
        except Exception as e:
            resp = {"message": e.message}
            http_status_code = constants.HTTP_500_INTERNAL_SERVER_ERROR
        self.set_header("location", "{}://{}{}".format(self.request.protocol,
            self.request.host, self.reverse_url("{}".format(constants.URL_NAME_BOOK))))
        self.set_status(http_status_code)
        self.write(resp)


def stop():
    """
    Stop the IOLoop.
    """
    tornado.ioloop.IOLoop.current().stop()

def sigint_handler(signum, frame):
    """
    Add shutdown task in next IOLoop.
    """
    tornado.ioloop.IOLoop.current().add_callback(stop)

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        URLSpec(
            r"{}".format(constants.URL_PATH_BOOK),
            BookHandler,
            name="{}".format(constants.URL_NAME_BOOK)
        ),
        URLSpec(
            r"{}".format(constants.URL_PATH_BUY),
            OrderHandler,
            name="{}".format(constants.URL_NAME_BUY)
        ),
        URLSpec(
            r"{}".format(constants.URL_PATH_SELL),
            OrderHandler,
            name="{}".format(constants.URL_NAME_SELL)
        ),
    ])
    http_server = HTTPServer(application)
    http_server.listen(options.port)
    signal.signal(signal.SIGINT, sigint_handler)
    tornado.ioloop.IOLoop.current().start()
    sys.exit(0)

if __name__ == "__main__":
    main()

