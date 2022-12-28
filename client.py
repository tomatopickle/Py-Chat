import socket
import threading
from termcolor import colored
import random
import pickle
import traceback
import logging
from pyfiglet import Figlet

f = Figlet(font='larry3d')
print (f.renderText('Py Chat Client'))

nickname = input("Choose your nickname: ")
room = input("Room Id: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.50', 7976))

colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

color = colors[random.randrange(len(colors))]


def receive():
    while True:
        try:
            message = pickle.loads(client.recv(1024))
            if message.get('type') == 'server':
                client.send(pickle.dumps({'name': nickname, 'roomId': room}))
            else:
                if (message['roomId'] == room):
                    print(message['msg'])
        except Exception as e:
            print("An error occured!")
            logging.error(traceback.format_exc())

            client.close()
            break


def write():
    while True:
        message = {'msg': colored(nickname, color) +
                   ': ' + input(''), "roomId": room}
        client.send(pickle.dumps(message))


receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()
