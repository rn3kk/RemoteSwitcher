from GPIOController import GPIOController

class Bmz:
    __bit0Pin = None
    __bit1Pin = None
    __bit2Pin = None
    __bit3Pin = None
    __gpioConroller = None


    def __int__(self, bit0, bit1, bit2, bit3):
        self.__bit0Pin = bit0
        self.__bit1Pin = bit1
        self.__bit2Pin = bit2
        self.__bit3Pin = bit3
        self.__gpioConroller = GPIOController.getInstace()

    def getActiveBMZ(self):
        return 1;

    def setActiveBMZ(self, activeBMZ):
        bitfield = list(bin(activeBMZ))[2:]
        b = "{0:b}".format(activeBMZ)
        self.__gpioConroller.setPinToState(self.__bit1Pin, bitfield[0])
        self.__gpioConroller.setPinToState(self.__bit2Pin, bitfield[1])
        self.__gpioConroller.setPinToState(self.__bit3Pin, bitfield[2])
        self.__gpioConroller.setPinToState(self.__bit4Pin, bitfield[3])



