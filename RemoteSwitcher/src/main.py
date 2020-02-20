import os
import logging
from Handlers import HttpRequestHandler
from Handlers import WebSocketHandler
from GPIOController import GPIOController
from Flex6xxx import Flex6xxx

class App:
    __httpIndexHandler = None
    __webSocketHandler = None

    def run(self):
        print("Start server")
        flexRadio = Flex6xxx()
        flexRadio.start()
        flexRadio.join()
        #self.__runHandlers()

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
    #log_name = '/var/log/remoteswitcher/all.log'
    log_name = 'C:\\tmp\\log.log'
    directory = os.path.dirname(log_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    log = logging.getLogger('root')
    log.setLevel(logging.DEBUG)
    file_logger = logging.FileHandler(log_name)
    file_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s module:%(module)s lineno:%(lineno)d|%(message)s')
    file_logger.setFormatter(formatter)
    log.addHandler(file_logger)
    log.propagate = True
    log.info('*****4*****Started**********')
    App().run()