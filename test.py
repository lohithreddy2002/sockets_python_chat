    # noinspection PyInterpreter
from client import Client
import time
from threading import Thread

c1 = Client("lohith")
def update_messages():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update evfery 1/10 of a second
        new_messages = c1.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        for msg in new_messages:  # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break


def start():

    connected = True
    while connected:
        msg = input()
        if msg == 'quit':
            c1.disconnect()
            connected = False
        else:
            c1.send_msg(msg)

if __name__ == "__main__":
    name = input()
    c1 = Client(name)
    start()
    Thread(target=update_messages).start()


