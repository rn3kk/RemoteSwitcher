from threading import Thread
from GPIOController import GPIOController
import socket
import json

import eventlet
from eventlet import wsgi
from eventlet import websocket
from eventlet.support import six

# demo app
import os

REQUEST = "request"
GET_GPIO_STATE = "getGpioState"

class RequestType:
    REQUEST_IS_UNKNOWN=0
    REQUEST_GET_INDEX_PAGE=1
    REQUEST_GET_PIN_STATE=2
    REQUEST_SET_PIN_STATE=3


SEC_WEBSOCKET_KEY = "Sec-WebSocket-Key:"
SEC_KEY_SUFFIX = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
SEC_WEBSOCKET_EXTENSION = "Sec-WebSocket-Extensions"

class HttpRequestHandler(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        sock = socket.socket()
        sock.bind(('', 80))
        sock.listen(1)
        print 'waite connection to port 80'

        while True:
            conn, addr = sock.accept()
            print 'connected:', addr
            req = conn.recv(1024)
            if not req:
                break
            requestType = self.__getRequestType(req)
            conn.send(self.getIndexPage())
            conn.close()
        conn.close()

    def getIndexPage(self):
        file = open("../res/index.html")
        data = file.read()
        file.close()
        return data

    def __getRequestType(self, request):
        if "GET" in request:
            return RequestType.REQUEST_GET_INDEX_PAGE;

@websocket.WebSocketWSGI
def handle(ws):
    while True:
        m = ws.wait()
        if m is None:
            print ("WebSocket client is disconected!")
            break
        print(m);
        jsonReq = json.loads(m)
        request = jsonReq[REQUEST]
        if request == GET_GPIO_STATE:
            state = GPIOController.getInstance().getGpioState()
            ws.send(state)
        eventlet.sleep(0.1)

def dispatch(environ, start_response):
    if environ['PATH_INFO'] == '/data':
        return handle(environ, start_response)
    else:
        start_response('200 OK', [('content-type', 'text/html')])
        return [open(os.path.join(
                     os.path.dirname(__file__),
                     'websocket.html')).read()]

class WebSocketHandler(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        listener = eventlet.listen(('127.0.0.1', 8080))
        print("\nVisit http://localhost:8080/ in your websocket-capable browser.\n")
        wsgi.server(listener, dispatch)