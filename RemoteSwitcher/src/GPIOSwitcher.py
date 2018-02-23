import json

class Pin:
    __pinName = None
    __pinNumber = None
    __pinState = None
    def __init__(self, pinName, pinNumber):
        self.__pinName = pinName
        self.__pinNumber = pinNumber

    def getPinName(self):
        return self.__pinName

    def getPinNumber(self):
        return self.__pinNumber

    def getPinState(self):
        return self.__pinState

class GPIOSwitcher:
    __pinsList = None

    def __init__(self):
        print("Load pins from file ../res/pins")
        self.__pinsList = list()
        file = open("../res/pins")
        data = file.read()
        file.close()
        jsonPins = json.loads(data)
        pinsList = jsonPins["pins"]
        for pinDict in pinsList:
            name = pinDict.get("name")
            number = pinDict.get("number")
            self.__pinsList.append(Pin(name, number))

    def getGpioState(self):
        return 0
