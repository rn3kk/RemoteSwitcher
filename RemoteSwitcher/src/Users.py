import logging

log = logging.getLogger('root')
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
        if result is True:
            log.info('Loggin is OK')
        else:
            log.critical('Fail login')
        return result
