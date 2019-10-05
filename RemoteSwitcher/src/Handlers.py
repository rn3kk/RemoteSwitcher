from threading import Thread, Lock
from GPIOController import GPIOController, REQUEST, GET_GPIO_STATE, CHANGE_GPIO_STATE, NAME, CHANGE_BMZ, BMZ_NUMBER
import socket
import json
import base64
from Users import Users

import eventlet
from eventlet import wsgi
from eventlet import websocket
#from eventlet.support import six

# demo app
import os


class RequestType:
    REQUEST_IS_UNKNOWN = 0
    REQUEST_GET_INDEX_PAGE = 1
    REQUEST_GET_PIN_STATE = 2
    REQUEST_SET_PIN_STATE = 3
    REQUEST_LOGIN = 4
    REQUEST_LOGIN_PAGE = 5
    AUTORISATION = 6


SEC_WEBSOCKET_KEY = "Sec-WebSocket-Key:"
SEC_KEY_SUFFIX = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
SEC_WEBSOCKET_EXTENSION = "Sec-WebSocket-Extensions"
HTTP_RESPONSE = 'HTTP/1.1 200 OK\r\nCache-Control : no-cache, private\r\nContent-Type: text/html\r\nContent-Length : %d\r\nDate : Mon, 24 Nov 2014 12:03:43 GMT\r\n\r\n'
HTTP_RESPONSE2 = 'HTTP/1.1 200 OK\r\nDate : Mon, 24 Nov 2014 12:03:43 GMT\r\nCache-Control : no-cache, private\r\nContent-Length : %d\r\nContent-Type: text/html\r\n'
HTTP_RESPONSE_UNAUTORISE = 'HTTP/1.1 401 Authorization Required\r\nDate: Tue, 01 Mar 2005 11:30:10 GMT\r\nServer: Apache/1.3.33 (Unix)\r\nWWW-Authenticate: Basic realm="How about authorization?"\r\nConnection: close\r\nContent-Type: text/html; charset=iso-8859-1"\r\n\r\n'
HTTP_BA_TAG = 'Authorization: Basic '

LOGIN_REQ = "login="

LOGIN = "rn3kk:admin"

class HttpRequestHandler(Thread):
    __users = None
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.__users = Users()
        port = 81
        sock = socket.socket()
        sock.bind(('', port))
        sock.listen(1)
        print 'waite connection to port '
        print port

        while True:
            conn, addr = sock.accept()
            print 'connected:', addr
            req = conn.recv(1024)
            if not req:
                print("request is empty")
            #   break
            if not self.checkAutorisation(req):
                conn.send(self.getLoginPage())
            else:
                requestType = self.__getRequestType(req)
                if requestType == RequestType.REQUEST_GET_INDEX_PAGE:
                    conn.send(self.getIndexPage())
            conn.close()

        conn.close()

    def checkAutorisation(self, req):
        pos = req.find(HTTP_BA_TAG)

        if pos == -1:
            return False
        pairBase64 = req[pos+len(HTTP_BA_TAG):]
        endPair = pairBase64.find('\r\n')
        pairBase64 = pairBase64[:endPair]
        pair = base64.b64decode(pairBase64).decode('utf-8')
        return self.__users.checkUser(pair)

    def getIndexPage(self):
        file = open("../res/index.html")
        data = file.read()
        file.close()
        content_length = len(data)
        page = (HTTP_RESPONSE % content_length)
        page = page + data
        return page

    def getLoginPage(self):
        return HTTP_RESPONSE_UNAUTORISE

    def __getRequestType(self, request):
        if "GET /" in request:
            return RequestType.REQUEST_GET_INDEX_PAGE

#mutex = Lock()
def sendToWs(ws, text):
#    mutex.acquire()
#    print(text)
    ws.send(text)
#    mutex.release()

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
            response = GPIOController.getInstance().getGpioState()
            sendToWs(ws, response)
        elif request == CHANGE_GPIO_STATE:
            name = jsonReq[NAME]
            response = GPIOController.getInstance().changePinState(name)
            sendToWs(ws, response)
        elif request == CHANGE_BMZ :
            bmzNum = jsonReq[BMZ_NUMBER]
            response = GPIOController.getInstance().changeBmz(bmzNum)
            sendToWs(ws, response)
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
        listener = eventlet.listen(('0.0.0.0', 8081))
        print("\nVisit http://localhost:8080/ in your websocket-capable browser.\n")
        wsgi.server(listener, dispatch)
