__author__ = 'firatlepirate'

import threading, socket
import random , time,datetime

class myThread (threading.Thread):

    def __init__(self, threadID, clientSocket, clientAddr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
    def run(self):
        print "Starting Thread-" + str(self.threadID)
        exit_flag = 1
        while exit_flag:

            data = self.clientSocket.recv(1024)

            if data != "" and data != "exit":
                 self.clientSocket.send("Peki <%s>" %str(self.clientAddr))

            elif data == "exit":
                self.clientSocket.close()
                exit_flag = 0

            '''wait_secs = random.randint(1,10)
            time.sleep(wait_secs)
            self.clientSocket.send("Merhaba saat su an: %s:%s:%s" % (str(datetime.datetime.now().hour),str(datetime.datetime.now().minute),str(datetime.datetime.now().second)))
            '''

            
        print "Ending Thread-" + str(self.threadID)


s = socket.socket()
host = "0.0.0.0"
port = 12345
s.bind((host, port))
s.listen(5)

threadCounter = 0


while True:
    print "Waiting for connection"
    c, addr = s.accept()
    print 'Got a connection from ', addr
    threadCounter += 1
    thread = myThread(threadCounter, c, addr)
    thread.start()
