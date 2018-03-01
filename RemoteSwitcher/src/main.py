from Handlers import HttpRequestHandler
from Handlers import WebSocketHandler
from GPIOController import GPIOController

class App:
    __httpIndexHandler = None
    __webSocketHandler = None

    def run(self):
        print "Start server"
        self.__runHandlers()

    def __runHandlers(self):
        gpioController = GPIOController.getInstance()
        gpioController.setName('controller')


        self.__httpIndexHandler = HttpRequestHandler()
        self.__httpIndexHandler.setName('index handler')
        self.__webSocketHandler = WebSocketHandler();
        self.__webSocketHandler.setName('websocket handler')

        gpioController.start()
        self.__httpIndexHandler.start()
        self.__webSocketHandler.start()

        gpioController.join()
        self.__httpIndexHandler.join()
        self.__webSocketHandler.join()


if __name__ == '__main__':
     App().run()