from flask import Flask,render_template,request
from client import Client
import time
from threading import Thread

app = Flask(__name__)
@app.route('/',methods = ['POST',"GET"])
def index():
        #Thread(target=update_messages).start()
        return render_template('home.html')
        if request.method == "POST":
            


c = Client("lohith")
@app.route('/login')
def login():
    return "bye"


def start():
    connected = True
    while connected:
        msg = input('')
        if msg == 'quit':
            c.disconnect()
            connected = False
        else:
            c.send_msg(msg)


def update_messages():
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1)  # update evfery 1/10 of a second
        new_messages = c.get_messages()  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        for msg in new_messages:  # display new messages
            return msg
            #if msg == "{quit}":
             #   run = False
              #  break



if __name__ == "__main__":
    app.run(debug =True)