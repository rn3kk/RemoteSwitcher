from Handlers import HttpRequestHandler
from Handlers import WebSocketHandler
from GPIOSwitcher import GPIOSwitcher

class App:
    __httpIndexHandler = None
    __webSocketHandler = None
    __gpioSwitcher = None

    def run(self):
        print "Start server"
        __gpioSwitcher = GPIOSwitcher()
        __gpioSwitcher.getGpioState()
        self.__runHandlers()

    def __runHandlers(self):
        self.__httpIndexHandler = HttpRequestHandler()
        self.__httpIndexHandler.setName('index handler')
        self.__webSocketHandler = WebSocketHandler();
        self.__webSocketHandler.setName('websocket handler')

        self.__httpIndexHandler.start()
        self.__webSocketHandler.start()

        self.__httpIndexHandler.join()
        self.__webSocketHandler.join()

if __name__ == '__main__':
     App().run()