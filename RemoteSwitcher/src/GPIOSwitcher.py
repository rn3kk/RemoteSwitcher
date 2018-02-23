import json

from enum import Enum

__metaclass__ = type

class PinType(Enum):
    input=1
    output=2


class Pin: #Base class for output pin
    __pinName = None
    __pinNumber = None

    def __init__(self, pinName, pinNumber):
        self.__pinName = pinName
        self.__pinNumber = pinNumber

    def getPinName(self):
        return self.__pinName

    def getPinNumber(self):
        return self.__pinNumber


class OutputPin(Pin):
    __autoOffTime = 0
    def __init__(self, pinName, pinNumber, autoOffTime = 0):
        super(OutputPin, self).__init__(pinName, pinNumber)
        self.__autoOffTime = autoOffTime




class GPIOSwitcher:
    __outputPinsList = None
    __inputPinsList = None

    def __init__(self):
        print("Load pins from file ../res/pins")
        self.__outputPinsList = list()
        self.__inputPinsList = list()
        file = open("../res/pins")
        data = file.read()
        file.close()
        jsonPins = json.loads(data)

        outputPinsList = jsonPins["pins_output"]
        for pin in outputPinsList: #load output pins
            name = pin.get("name")
            gpio_number = pin.get("gpio_number")
            autoOff = pin.get("auto_off")
            if autoOff is None:
                autoOff = 0
            self.__outputPinsList.append(OutputPin(name, gpio_number, autoOff))

        inputPinsList = jsonPins["pins_input"]
        for pin in outputPinsList:  # load output pins
            name = pin.get("name")
            gpio_number = pin.get("gpio_number")
            self.__outputPinsList.append(Pin(name, gpio_number))

    def getGpioState(self):
        return 0
