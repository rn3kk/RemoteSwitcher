import json
import time
from threading import Thread

from enum import Enum

__metaclass__ = type

PINS_OUTPUT = "pinsOutput"
PINS_INPUT = "pinsInput"
NAME = "name"
GPIO_NUMBER = "gpioNumber"
AUTO_OFF = "auto_off"
STATE = "state"
TYPE = "type"
REQUEST = "request"
GET_GPIO_STATE = "getGpioState"
CHANGE_GPIO_STATE = "changeGpioState"
REQUEST_RESULT = "result"
TRUE = "true"
FALSE = "false"

class PinType(Enum):
    input=1
    output=2


class Pin: #Base class for output pin
    __pinName = None
    __pinNumber = None
    __pinState = None

    def __init__(self, pinName, pinNumber):
        self.__pinName = pinName
        self.__pinNumber = pinNumber
        self.__pinState = False

    def getPinName(self):
        return self.__pinName

    def getPinNumber(self):
        return self.__pinNumber

    def getPinState(self):
        return self.__pinState

    def setPinNewState(self, state):
        self.__pinState = state


class OutputPin(Pin):
    __autoOffTime = 0
    __timeLeft = 0

    def __init__(self, pinName, pinNumber, autoOffTime = 0, pinState = False):
        super(OutputPin, self).__init__(pinName, pinNumber)
        self.__autoOffTime = autoOffTime
        self.setPinNewState(pinState)


class GPIOController(Thread):
    __instance = None
    __outputPinsList = None
    __inputPinsList = None

    @staticmethod
    def getInstance():
        if GPIOController.__instance == None:
            GPIOController.__instance = GPIOController()
        return GPIOController.__instance

    def __init__(self):
        Thread.__init__(self)

        print("Load pins from file ../res/pins")
        self.__outputPinsList = list()
        self.__inputPinsList = list()
        file = open("../res/pins")
        data = file.read()
        file.close()
        jsonPins = json.loads(data)

        outputPinsList = jsonPins[PINS_OUTPUT]
        for pin in outputPinsList: #load output pins
            name = pin.get(NAME)
            gpio_number = pin.get(GPIO_NUMBER)
            autoOff = pin.get(AUTO_OFF)
            if autoOff is None:
                autoOff = 0
            state = pin.get(STATE)
            self.__outputPinsList.append(OutputPin(name, gpio_number, autoOff, state))

        inputPinsList = jsonPins[PINS_INPUT]
        for pin in inputPinsList:  # load output pins
            name = pin.get(NAME)
            gpio_number = pin.get(GPIO_NUMBER)
            self.__inputPinsList.append(Pin(name, gpio_number))

    def run(self):
        while False:
           time.sleep(1)



    def getGpioState(self):
        input, output = [], []
        for outputPin in self.__outputPinsList:
            str = {NAME:outputPin.getPinName(), STATE:outputPin.getPinState()}
            output.append(str)
        for inputPin in self.__inputPinsList:
            str = {NAME: inputPin.getPinName(), STATE: inputPin.getPinState()}
            input.append(str)

        response = {}
        response[TYPE] = GET_GPIO_STATE
        response[REQUEST_RESULT] = TRUE
        response[PINS_OUTPUT] = output
        response[PINS_INPUT] = input
        response = json.dumps(response)
        return response

    def changePinState(self, pinName):
        response = {}
        response[TYPE] = CHANGE_GPIO_STATE
        response[REQUEST_RESULT] = TRUE
        response = json.dumps(response)
        return response