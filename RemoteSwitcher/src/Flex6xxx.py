import socket
import threading
from time import sleep

FLEX_IP = "192.168.16.246"
FLEX_PORT = 4992

LIST = b'C41|slice list\r\n'
SUB_SCU = b'C21|sub scu all\r\n'
SUB_SLICE = b'C21|sub slice all\r\n'

class Flex6xxx(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while(True):
            try:
                sock.connect((FLEX_IP, FLEX_PORT))
                self.__communicateWithRadio(sock)
            except Exception:
                print("socket error ")
                sock.close()
            sleep(2)

    def __communicateWithRadio(self, sock):
        sock.settimeout(2)
        sock.sendall(SUB_SLICE)
        while(True):
            try:
                data = sock.recv(1024)
                sleep(0.1)
                # sock.sendall(SUB_SCU)
                print(data)
            except socket.timeout:
                print ("timeout")
                sleep(1)
            except Exception:
                sock.close()





