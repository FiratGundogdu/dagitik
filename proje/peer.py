__author__ = 'firatlepirate'

import socket
import threading
import errno
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
from random import randint
import random
import ip


class ClientReadThread (threading.Thread):
    def __init__(self, name, cSocket,list_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.list_queue=list_queue
        self.count=0
        self.connect_point_temp={}
        self.count2=0

    def parser(self,data):
         global count
         global command
         global connect_point_list

         if data[0:5]=="REGOK":

              if len(data)>6:
                   if count==0:
                        print("REGOK")
                        self.cSocket.close()
                        self.check_comman=0
                        time.sleep(1)
                        #Negatorun ip ve port bilgisi
                        server_host="127.0.0.1"
                        server_port=12345
                        #Peerin clienti ilk olarak negotiatora baglaniyor
                        se=socket.socket()
                        se.connect((server_host,server_port))

                        se.send("REGME "+peer_host+":"+str(peer_port))
                        command="GETNL"
                        time.sleep(0.3)

                        count=1
                         #Peerin client tarafinin okumasi
                        client_read=ClientReadThread("PeerServerReadThread",se,self.list_queue)
                        client_read.start()

              else:
                   print(command)
                   try:
                        self.cSocket.send(command)
                   except socket.error:
                         self.cSocket.close()

         elif data[0:5]=="REGER":
              print("REGER")

         elif data[0:11]=="NLIST BEGIN":
              connect_point_list=data.split("\n")
              connect_point_list=connect_point_list[1:-1]
              print(connect_point_list)
              for  i  in connect_point_list:
                   tempdiz=i.split(":")
                   connect_point_temp_list[tempdiz[0]+tempdiz[1]]="True"
              self.cSocket.close()
              print("gunceli peerden aldim")

    def run(self):
         while True:
              try:
                    incoming_data=self.cSocket.recv(4096)
              except socket.error ,e:
                   err=e.args[0]
                   if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        time.sleep(1)
                        print 'No data available'
                        continue


              if str(incoming_data[0:11])=="NLIST BEGIN":
                   break

              if str(incoming_data[0:5])=="REGOK":
                   if len(incoming_data)>5:
                        break







#Bu thread diger  peerlerden   guncel olan listeyi  istiyor
class ClientGetUpdateList (threading.Thread):
    def __init__(self, name,list_queue):
        threading.Thread.__init__(self)
        self.name = name
        self.list_queue=list_queue
    def run(self):
         global command
         global UPDATE_INTERVAL
         while True:
              time.sleep(UPDATE_INTERVAL)
              number= random.randint(1, 2)
              if number==1:
                   command="GETNL "+"5"
              else:
                   command="GETNL "

              for  connection in connect_point_list:
                   connection=connection.split(":")
                   per_ip=connection[0]
                   per_port=connection[1]
                   print(per_port)
                   if  per_port!=str(peer_port):
                        print("Guncel listeyi peer")
                        s=socket.socket()
                        s.connect((per_ip,int(per_port)))
                        s.send("REGME "+peer_host+":"+str(peer_port))
                        client_read=ClientReadThread("PeerServerReadThread",s,self.list_queue)
                        client_read.start()


UPDATE_INTERVAL=600

dictionary="peer"

connect_point_list=[]
connect_point_temp_list={}

command=""
temp=""
#Bu degisken negotiator a  kayit  isleminde  bayrak olarak kullanilmaktadir.
count=0

list_queue=Queue.Queue()
q=Queue.Queue()


peer_host="127.0.0.1"
peer_port=12331


#Negotiatorun ip ve port bilgisi
server_host="127.0.0.1"
server_port=12345


server_peer=ServerThread("ServerThread",peer_host,peer_port)
server_peer.start()

s=socket.socket()
s.connect((server_host,server_port))


#Peer  negotiatora  baglandiktan sonra  otomatik olarak ilk REGME  kaydolma istegini  gonderiyor  daha sonra 2 saniye sonrada  GETNL  istegi yapiyor
s.send("REGME "+peer_host+":"+str(peer_port))


client_read=ClientReadThread("PeerServerReadThread",s,list_queue)
client_read.start()
