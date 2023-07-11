import threading
import _thread
import random
import string


received = []
data = []
data_send = ""
window = 5
i = 0
flag = 0
h = 0


class all_not_received(Exception):
    pass


def sender(lock):
    global i
    global data_send
    global flag
    while(True):
        if not lock.locked():
            data_send = data[i: i + window]
            i += window
            if data_send[-1] == "1":
                data_send = data_send[:-1]
            if len(data_send) == 0:
                break
            print("Sending : ", *data_send, sep=" ")
            lock.acquire()
            flag = 0
            if i >= len(data):
                break


def ack(lock):
    global received
    global h
    global i
    global send_data
    try:
        print("Received : ", "".join(received))
        if "".join(received) != data_send:
            raise all_not_received()
        print("Send_data : ", data_send)
        print("Acknowledgement for  : ", received[-1])
    except all_not_received:
        if len(received) != 0:
            print("Error at : ", received[-1])
            i -= (len(send_data) - len(received))
        else:
            print("Nothing received")
            i -= window
    finally:
        lock.release()
        h = 1


def receiver(lock):
    global received
    global flag
    global h
    while(True):
        if lock.locked() and flag == 0:
            timer = threading.Timer(0.00000000000000000000000001, ack, args=(lock,))
            h = 0
            received = []
            timer.start()
            for _ in data_send:
                received.append(_)
            flag = 1
            if i >= len(data):
                break
        if h == 1 or len(data_send) == 0:
            timer.cancel()
        if len(data_send) == 0:
            break


def file_create():
    file = open('prac4_input_gbn.txt', 'w')
    n = random.randint(10, 30)
    res = ''.join(random.choices(string.ascii_uppercase, k=n))
    res = res + '1'
    file.write(res)


if __name__ == '__main__':
    send_data=""
    file_create()
    file = open("Prac4_input_gbn.txt", "r")
    data = file.readline()
    print("The data is : ", data)
    # a = 0
    # t1 = threading.Thread(target=sender, args=(a,))
    # t2 = threading.Thread(target=receiver, args=(a,))
    lock = _thread.allocate_lock()
    t1 = _thread.start_new_thread(sender, (lock,))
    t2 = _thread.start_new_thread(receiver, (lock,))