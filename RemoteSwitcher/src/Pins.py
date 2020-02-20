from enum import Enum
#import RPi.GPIO as GPIO

class PinType(Enum):
    INPUT = 1
    OUTPUT = 2

class Pin:  # Base class for output pin
    __pinName = None
    _pinNumber = None
    _pinState = None
    __pinType = None
    __pinGroup=None


    def __init__(self, pinName, pinNumber, pinType, pinGroup):
        self.__pinName = pinName
        self._pinNumber = pinNumber
        self.__pinType = pinType
        self.__pinGroup = pinGroup

    def getPinName(self):
        return self.__pinName

    def getPinNumber(self):
        return self._pinNumber

    def getPinState(self):
        return self._pinState

    def getPinType(self):
        if self.__pinType == PinType.INPUT:
            return 0
        if self.__pinType == PinType.OUTPUT:
            return 1

    def getPinGroup(self):
        return self.__pinGroup

class InputPin(Pin):

    def __init__(self, pinName, pinNumber, pinGroup):
       print('InputPin ', pinName, 'number ', pinNumber)
       super(InputPin, self).__init__(pinName, pinNumber, PinType.INPUT, pinGroup)
#       GPIO.setmode(GPIO.BCM)
#       GPIO.setup(int(pinNumber), GPIO.IN)

    def updatePinState(self):
        self._pinState = 1
#        self._pinState = GPIO.input(int(self._pinNumber))

class OutputPin(Pin):

    __autoOffTime = 0
    __timeLeft = 0
    __defaultState = 0;
    __inversion = False;

    def __init__(self, pinName, pinNumber, pinGroup, autoOffTime=0, pinState=False, inversion=False):
        print('OutputPin ', pinName, 'number ', pinNumber, "autoOffTime", autoOffTime)
        super(OutputPin, self).__init__(pinName, pinNumber, PinType.OUTPUT, pinGroup)
        self.__autoOffTime = autoOffTime
        self.__inversion = inversion
        if inversion:
            self.__defaultState = not pinState
        else:
            self.__defaultState = pinState
        self.__setState(pinState)

    def getPinState(self):
        if self.__inversion:
            return not super(OutputPin, self).getPinState()
        else:
            return super(OutputPin, self).getPinState()

    def setPinState(self, state):
        log.debug('old state %s new state %s',  self.getPinState(), state)
        self.__timeLeft = 1
        self. __setState(state)


    def __setState(self, state):
        try:
#            GPIO.setwarnings(False)
#            GPIO.setmode(GPIO.BCM)
#            GPIO.setup(int(self._pinNumber), GPIO.OUT)

            if self.__inversion:
                self._pinState = not state
            else:
                self._pinState = state
#            GPIO.output(int(self._pinNumber), self._pinState)
            log.debug('New statete for OutputPin %s number %s state %s', self.getPinName(), self.getPinNumber(), self.getPinState() )
        except Exception:
            log.critical('Error: output pin state NOT changed')

    def updateAutoOffstate(self, checkInterval):
        if self.__autoOffTime == 0:
            return
        if self.__timeLeft == 0:
            return
        if self.__timeLeft >= self.__autoOffTime:
            self.__setState(self.__defaultState) #set default pin state after time
            self.__timeLeft = 0
        else:
            self.__timeLeft += checkInterval
            log.debug('Auto change state OutputPin %s number %s state %s time %s', self.getPinName(), self.getPinNumber(), self.getPinState(), self.__timeLeft)
