import threading
import random
import string

flag = 1
data = ''
i = 0

def file_create():
    file = open('data.txt', 'w')
    n = random.randint(10, 20)
    res = ''.join(random.choices(string.ascii_uppercase, k=n))
    res = res + '1'
    file.write(res)
    print("Message File Created with data",res)

def sender(a):
    global flag
    global data
    global i
    while(True):
        if data[i] == '1':
            break
        if flag == 1:
            print("Sending  : ", data[i])
            i += 1
            flag = 0

def receiver(a):
    global flag
    global i
    while(True):
        if flag == 0:
            print("Recieved : ", data[i-1])
            flag = 1
            if data[i] == '1':
                break

if __name__ == "__main__":    
    file_create()
    file = open("data.txt", "r")
    data = file.readline()
    print("The data is : ", data)
    a = 0
    t1 = threading.Thread(target=sender, args=(a,))
    t2 = threading.Thread(target=receiver, args=(a,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Done!")
