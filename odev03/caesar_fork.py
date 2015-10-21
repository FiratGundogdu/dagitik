__author__ = 'firatlepirate'

#import Queue
from multiprocessing import Lock, Process, Queue, current_process

alfabe = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Gerekli inputlari istiyoruz
alfabe_key = input("Give me a number to make new alphabet: ")
count_fork = input("Give me a number to define number of threads: ")
count_char = input("Give me a number of characters that threads will work on it: ")

# Sifreleme icin yeni alfabe olusturuyoruz
alfabe_cryt=[0]*26
for i in range(len(alfabe)):
    alfabe_cryt[i]=alfabe[((i-alfabe_key)%26)]
    alfabe_cryt[i]=alfabe_cryt[i].upper()

print (alfabe)
print alfabe_cryt

file1 = open('metin.txt', 'r')
lock = Lock()

exit_flag = 0

# worker larin islerini tanimliyoruz
def worker(read_queue, write_queue):

    while not read_queue.empty():

        lock.acquire()
        text = read_queue.get()

        text=text.lower()

        text_crypt = ""

        for i in range(len(text)):
                if  text[i] in alfabe:
                    text_crypt = text_crypt + alfabe_cryt[alfabe.index(text[i])]
                else:
                    text_crypt = text_crypt + text[i]


        write_queue.put(text_crypt)
        lock.release()
        print text_crypt
        print("yazdim q ya")

def main():

    read_queue = Queue()
    write_queue = Queue()
    processes = []

    # read_queue yu dolduruyoruz
    lock.acquire()
    while 1 :
        c = file1.read(count_char)
        read_queue.put(c)
        if not c:
            break
    lock.release()

    for w in xrange(count_fork):
        p = Process(target=worker, args=(read_queue, write_queue))
        p.start()
        processes.append(p)


    for p in processes:
        p.join()

    # write_queue dan dosyaya yaziyoruz
    while not write_queue.empty():

        file_name= "crypted_<%d>_<%d>_<%d>.txt" %(alfabe_key,count_fork,count_char)
        file = open(file_name,'a')
        crypt = write_queue.get()
        file.write(crypt)
        file.close()
        print("yazdim dosyaya")

if __name__ == '__main__':
    main()


