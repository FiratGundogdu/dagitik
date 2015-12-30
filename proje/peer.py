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



class  ServerThread(threading.Thread):
     def __init__(self, name, peer_ip, peer_port):
        threading.Thread.__init__(self)
        self.name = name
        self.peer_ip=peer_ip
        self. peer_port=peer_port


     def run(self):
          peer_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          peer_socket.bind(( self.peer_ip,self. peer_port))
          peer_socket.listen(5)
          threadCounter=0
          while True:
              cPeer,addrPeer=peer_socket.accept()
              threadCounter += 1
              threadPeer = ServerReadThread("ServerReadThread"+str(threadCounter), cPeer, addrPeer)
              threadPeer.start()

class ServerReadThread (threading.Thread):
    def __init__(self, name, cSocket, address):
        threading.Thread.__init__(self)
        self.name = name
        self.cSocket = cSocket
        self.address = address
        self.peer_ip=""
        self.peer_port=""
        self.connect_point={}
        self.check_command_nummber=""
        self.msg_list=""
        self.file_name_list=""
        self.user_add=""
        self.running=True

    def parser(self,data) :
         global connect_point_list
         global connect_point_temp_list


         if data[0:5]=="HELLO" :
              response = "SALUT"
              self.cSocket.send(response)
         elif data[0:5]=="CLOSE":
              response = "BUBYE"
              self.cSocket.send(response)
              self.cSocket.close()
         elif data[0:5]=="REGME":
              self.peer_ip=str(data[6:data.index(":")])
              self.peer_port=data[data.index(":")+1:]


              if  self.peer_ip+str(self.peer_port)  in connect_point_temp_list.keys():
                   response = "REGOK"

                   try:
                        self.cSocket.send(response)
                   except socket.error:
                        self.cSocket.close()
                   self.check_command_nummber=2

              else:
                   t=time.ctime()
                   self.connect_point["time"]=t
                   self.connect_point["peer_port"]= self.peer_port
                   self.connect_point["peer_ip"]=self.peer_ip
                   self.user_add=self.peer_ip+":"+str(self.peer_port)+":"+str(t)
                   connect_point_list.append(self.user_add)
                   connect_point_temp_list[self.peer_ip+str(self.peer_port)]="True"
                   try:
                        self.cSocket.send("REGWA")
                   except socket.error:
                        self.cSocket.close()
                   time.sleep(0.4)
                   try:
                        self.cSocket.send("REGOK "+str(t))
                   except socket.error:
                        self.cSocket.close()
                   self.check_command_nummber=1
                   self.cSocket.close()
              print(connect_point_list)

         elif data[0:5]=="GETNL":
              if len(data)>5:
                   if len(connect_point_list)>5:
                        size_list=5
                   else:
                        size_list=len(connect_point_list)

              else:
                   size_list=len(connect_point_list)

              for  user  in  connect_point_list[0: size_list] :
                   self.msg_list=self.msg_list+user+"\n"
              self.cSocket.send("NLIST BEGIN"+"\n"+self.msg_list+"NLIST END")
              self.cSocket.close()
              print("NLIST BEGIN"+"\n"+self.msg_list+"NLIST END")
              print(self.msg_list)
              print("Listeyi gonderdim")

         elif data[0:11]=="NLIST BEGIN":
              print("GELEN"+data)
              connect_point_list=[]
              connect_point_list=data.split("\n")
              connect_point_list=connect_point_list[1:-1]
              print(connect_point_list)
              connect_point_temp_list.clear()
              for  i  in connect_point_list:
                   tempdiz=i.split(":")
                   connect_point_temp_list[tempdiz[0]+tempdiz[1]]="True"
              self.cSocket.close()
              print("Guncel listeyi aldim")

         else:
              response = "REGER"
              try:
                   self.cSocket.send(response)
                   self.cSocket.close()
              except socket.error:
                   self.cSocket.close()



    def run(self):
         while self.running:
              try:
                    incoming_data=self.cSocket.recv()

              except socket.error ,e:
                   err=e.args[0]
                   if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                      time.sleep(1)
                      print 'No data available'
                      continue
              self.parser(incoming_data)

              if incoming_data=="CLOSE":
                   break
              if incoming_data[0:5]=="REGME":
                   if   self.check_command_nummber==1:
                        break
              elif incoming_data[0:5]=="GETNL":
                   if   self.check_command_nummber==2:
                        break
              elif incoming_data[0:11]=="NLIST BEGIN":
                   break

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
