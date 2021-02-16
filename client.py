from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    HOST = '172.23.192.1'
    PORT = 1010
    ADDR = (HOST, PORT)
    BUFF_SIZE = 512

    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        recieve_thread = Thread(target=self.recieve_msg)
        recieve_thread.start()
        self.send_msg(name)
        self.lock = Lock()

    def recieve_msg(self):

        while True:
            try:
                msg = self.client_socket.recv(self.BUFF_SIZE).decode()
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()


            except Exception as e:
                print('[ECEPTION]', e)
                break

    def send_msg(self, msg):
        try:
            self.client_socket.send(bytes(msg, 'utf-8'))
            if msg == '{quit}':
                self.client_socket.close()
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        msg_copy = self.messages[:]
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return msg_copy

    def disconnect(self):
        self.send_msg('{quit}')
