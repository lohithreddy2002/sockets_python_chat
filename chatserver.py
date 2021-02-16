from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time
from person import Person

HOST = '172.23.192.1'  # host name
PORT = 1010  # port number
BUFF_SIZE = 512  # max size of the message
MAX_CONNECTIONS = 10  # max no.of connections
persons = []  # list to maintain the persons in the chat
ADDR = (HOST, PORT)  # addr of host
SERVER = socket(AF_INET, SOCK_STREAM)  # server socket
SERVER.bind(ADDR)  # binding address to server socket


def brodcast(msg, name):  # function to send message to all clients
    for person in persons:
        client = person.client
        try:
            client.send(bytes(name, 'utf-8') + msg)
        except Exception as e:
            print('[EXCEPTION]', e)


def client_communication(person): # function to recieve messages
    client = person.client

    name = client.recv(BUFF_SIZE).decode('utf-8')
    person.set_name(name)
    msg = bytes(f'{name} has joined the chat', 'utf-8')
    brodcast(msg, ' ')
    while True:
        try:
            msg = client.recv(BUFF_SIZE)

            if msg == bytes('{quit}', "utf-8"):
                client.close()
                persons.remove(person)

                brodcast(bytes('{name} has left the chat..', 'utf-8'), '')

                print(f'[Disconnected] {name} disconnected')
                break
            else:
                brodcast(msg, name + ':')
                print(f"{name}: ", msg.decode("utf8"))
        except Exception as e:
            print('[EXCEPTION]', e)
            break


def waiting_connection():
    connected = True
    while connected:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f'[connection]{addr} connected to  the server at {time.time()}')
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print('[EXCEPTION]', e)
            connected = False
    print('server crashed')


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)
    print('server is listening .....')
    thread = Thread(target=waiting_connection)
    thread.start()
    thread.join()
    SERVER.close()
