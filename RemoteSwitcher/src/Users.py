class Users:
    __userList = None

    def __init__(self):
        self.__userList = []
        with open('/home/pi/RemoteSwitcher/RemoteSwitcher/res/users') as f:
        #with open('../res/users') as f:
            for line in f:
                line = line.rstrip("\n")
                if len(line) > 2 :
                    self.__userList.append(line)

    def checkUser(self, pair):
        result = False
        for el in self.__userList:
            if el == pair:
                result = True
                break
        return result
