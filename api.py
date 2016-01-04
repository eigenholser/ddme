import json
import signal
from tornado.httpserver import HTTPServer
from tornado.httputil import HTTPHeaders
from  tornado.web import URLSpec
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from orders import Book, Buy, Sell

define("port", default=3000, help="run on the given port", type=int)
Book()


class BookHandler(tornado.web.RequestHandler):
    """
    Handle GET requests to /book API endpoint.
    """
    def get(self):
        self.set_header("content-type", "application/json")
        ret = json.dumps(Book().orders())
        self.write(ret)


class OrderHandler(tornado.web.RequestHandler):
    """
    Handle POST requests to /buy and /sell API endpoints.
    """
    def post(self, **kwargs):
        order = None
        body = json.loads(self.request.body)
        if self.request.uri == "/buy":
            order = Buy(**body)
        if self.request.uri == "/sell":
            order = Sell(**body)
        fills = Book().match(order)
        # TODO: Would prefer to handle the headers more cleverly like with
        # a decorator.
        self.set_header("content-type", "application/json")
        self.set_header("location", "{}://{}{}".format(self.request.protocol,
            self.request.host, self.reverse_url("book")))
        self.write(json.dumps(fills))


def stop():
    tornado.ioloop.IOLoop.current().stop()

def sigint_handler(signum, frame):
    tornado.ioloop.IOLoop.current().add_callback(stop)

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        URLSpec(r"/book", BookHandler, name="book"),
        URLSpec(r"/buy", OrderHandler, name="buy"),
        URLSpec(r"/sell", OrderHandler, name="sell"),
    ])
    http_server = HTTPServer(application)
    http_server.listen(options.port)
    signal.signal(signal.SIGINT, sigint_handler)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
