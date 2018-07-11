import json
import time
from enum import Enum
from Bmz import Bmz

#import RPi.GPIO as GPIO
from threading import Thread

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
CHANGE_BMZ = "changeBmz"
BMZ_NUMBER = "bmzNumber"
REQUEST_RESULT = "result"
TRUE = "true"
FALSE = "false"

class PinType(Enum):
    INPUT=1
    OUTPUT=2


class Pin: #Base class for output pin
    __pinName = None
    _pinNumber = None
    _pinState = None
    __pinType = None

    def __init__(self, pinName, pinNumber, pinType):
        self.__pinName = pinName
        self._pinNumber = pinNumber
        self.__pinType = pinType
        #GPIO.setup(pinNumber, GPIO.IN)

    def getPinName(self):
        return self.__pinName

    def getPinNumber(self):
        return self._pinNumber

    def getPinState(self):
        return self._pinState

    def getPinType(self):
        return self.__pinType


class InputPin(Pin):

    def __init__(self, pinName, pinNumber, pinType):
        super(InputPin, self).__init__(pinName, pinNumber, PinType.input)

    def updatePinState(self):
        self._pinState = 1
        #self._pinState = GPIO.input(self._pinNumber)

class OutputPin(Pin):
    __autoOffTime = 0
    __timeLeft = 0

    def __init__(self, pinName, pinNumber, pinType, autoOffTime = 0, pinState = False):
        super(OutputPin, self).__init__(pinName, pinNumber, PinType.output)
        self.__autoOffTime = autoOffTime
        self.setPinNewState(pinState)
        #GPIO.setup(pinNumber, GPIO.OUT)

    def setPinNewState(self, state):
        self._pinState = state
        #GPIO.setup(self._pinNumber, state)

class GPIOController(Thread):
    __instance = None
    __outputPinsList = None
    __inputPinsList = None
    __bmz = None

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


        #GPIO.setmode(GPIO.BOARD)
        outputPinsList = jsonPins[PINS_OUTPUT]

        #load bmz pins
        bit1 = None
        bit2 = None
        bit3 = None
        bit4 = None
        for pin in outputPinsList: #load output pins
            name = pin.get(NAME)
            gpio_number = pin.get(GPIO_NUMBER)
            autoOff = pin.get(AUTO_OFF)
            if autoOff is None:
                autoOff = 0
            state = pin.get(STATE)
            type = pin.get(TYPE)
            self.__outputPinsList.append(OutputPin(name, gpio_number, autoOff, state))
            if type == "bmz":
                if name == "bit1" :
                    bit1 = gpio_number
                if name == "bit2":
                    bit2 = gpio_number
                if name == "bit3":
                    bit3 = gpio_number
                if name =="bit4":
                    bit4 = gpio_number
        if not (bit1 is None) and not (bit2 is None) and not (bit3 is None) and not (bit4 is None):
            self.__bmz = Bmz()

        inputPinsList = jsonPins[PINS_INPUT]
        for pin in inputPinsList:  # load input pins
            name = pin.get(NAME)
            gpio_number = pin.get(GPIO_NUMBER)
            type = pin.get(TYPE)
            self.__inputPinsList.append(InputPin(name, gpio_number))

    def run(self):
        while False:
           time.sleep(1)
        for pin in self.__inputPinsList:
            InputPin(pin).updatePinState()
        #GPIO.cleanup()

    def getGpioState(self):
        input, output = [], []
        for outputPin in self.__outputPinsList:
            str = {NAME:outputPin.getPinName(), STATE:outputPin.getPinState(), TYPE:outputPin.getPinType()}
            output.append(str)
        for inputPin in self.__inputPinsList:
            str = {NAME: inputPin.getPinName(), STATE: inputPin.getPinState(), TYPE:inputPin.getPinType()}
            input.append(str)

        response = {}
        response[TYPE] = GET_GPIO_STATE
        response[REQUEST_RESULT] = TRUE
        response[PINS_OUTPUT] = output
        response[PINS_INPUT] = input
        response = json.dumps(response)
        return response

    def changePinState(self, pinName):
        for pin in self.__outputPinsList:
            if pin.getPinName() == pinName:
                pin.setPinNewState(not pin.getPinState())
        response = {}
        response[TYPE] = CHANGE_GPIO_STATE
        response[REQUEST_RESULT] = TRUE
        response = json.dumps(response)
        return response

    def changeBmz(self, bmzNumber):
        if not (self.__bmz is None):
            result = FALSE
        else:
            result = TRUE
            self.__bmz.setActiveBMZ(bmzNumber)
        response = {}
        response[TYPE] = CHANGE_BMZ
        response[REQUEST_RESULT] = result
        response = json.dumps(response)
        return response

    def setPinToState(self,gpioPin, state):
        return 0
