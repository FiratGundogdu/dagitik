__author__ = 'firatlepirate'


import socket
import threading,sys



class readThread (threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            data = self.socket.recv(1024)
            if data:
                print '<Server>:', data


class writeThread (threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
    def run(self):
        exit_flag = 1
        while exit_flag:
            message = raw_input()
            self.socket.send(message)
            if message == "exit":
                exit_flag = 0
                self.socket.close()
                sys.exit(0)



s = socket.socket()
host = "127.0.0.1"
port = 12345
s.connect((host, port))

rThread = readThread(s)
rThread.start()
wThread = writeThread(s)
wThread.start()
