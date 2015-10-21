__author__ = 'firatlepirate'

import threading
import Queue


alfabe = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Gerekli inputlari istiyoruz
alfabe_key = input("Give me a number to make new alphabet: ")
count_thread = input("Give me a number to define number of threads: ")
count_work = input("Give me a number of characters that threads will work on it: ")

# Sifreleme icin yeni alfabe olusturuyoruz
alfabe_cryt=[0]*26
for i in range(len(alfabe)):
    alfabe_cryt[i]=alfabe[((i-alfabe_key)%26)]
    alfabe_cryt[i]=alfabe_cryt[i].upper()

print (alfabe)
print alfabe_cryt


# thread ve queue icin gerekli degiskenleri tanimliyoruz
exit_flag = 0
file1 = open('metin.txt', 'r')
readQueue = Queue.Queue()

threadLock = threading.Lock()
threads = []
threadID = 1


# Okuma queue'yu dolduruyoruz
threadLock.acquire()
while 1 :
    c = file1.read(count_work)
    print "q ya yazdim"
    readQueue.put(c)

    if not c:
        break
threadLock.release()



# Threadleri tanimliyoruz
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        cypher_and_write(self.name, self.q)
        print "Exiting " + self.name



# sifrele_yaz fonksiyonu
def cypher_and_write(tName,q):

    while not exit_flag:

        # read_queue'dan okuma yapiyoruz
        threadLock.acquire()
        if not readQueue.empty():

            text = q.get()
            text=text.lower()
            text_crypt = ""

            # Sifreli metni olusturuyoruz
            for i in range(len(text)):
                if  text[i] in alfabe:
                    text_crypt = text_crypt + alfabe_cryt[alfabe.index(text[i])]
                else:
                    text_crypt = text_crypt + text[i]

             # Sifreli metni degisken isimli dosyaya yaziyoruz.
            file_name= "crypted_<%d>_<%d>_<%d>.txt" %(alfabe_key,count_thread,count_work)

            file = open(file_name,'a')
            file.write(text_crypt)
            file.close()
            threadLock.release()

            print " (%s) dosyaya yazdim" %(tName)
        else:
            print "(%s) q bos" %(tName)
            threadLock.release()




# thread leri olusturuyoruz
for i in range (count_thread):
    thread = myThread(threadID,'thread_'+str(threadID), readQueue)
    thread.start()
    threads.append(thread)
    threadID += 1





while not readQueue.empty():
    pass

exit_flag =1


# threadleri birlestiriyoruz
for t in threads:
    t.join()






