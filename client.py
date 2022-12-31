import socket
import threading
from termcolor import colored
import random
import pickle
import traceback
import logging
from pyfiglet import Figlet

# Create a Figlet object with the 'larry3d' font
f = Figlet(font='larry3d')

# Print an ASCII art banner
print(f.renderText('Py Chat Client'))

# Prompt the user to choose a nickname
nickname = input("Choose your nickname: ")

# Prompt the user to enter a room id
room = input("Room Id: ")

# Create a socket and connect to the server at the specified IP and port
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.50', 7976))

# Create a list of colors that can be applied to messages
colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

# Randomly select a color from the list to apply to the user's messages
color = colors[random.randrange(len(colors))]


def receive():
    # Continuously receive messages from the server
    while True:
        try:
            # Deserialize the message received from the server
            message = pickle.loads(client.recv(1024))

            # If the message is from the server, send a message back with the user's nickname and room id
            if message.get('type') == 'server':
                client.send(pickle.dumps({'name': nickname, 'roomId': room}))
            else:
                # If the message is from another client and is intended for the current room, print it to the console
                if (message['roomId'] == room):
                    print(message['msg'])
        except Exception as e:
            # If an error occurs, print a message, log the error, close the socket, and break out of the loop
            print("An error occured!")
            logging.error(traceback.format_exc())
            client.close()
            break


def write():
    # Continuously prompt the user for input and send it as a message to the server
    while True:
        message = {'msg': colored(nickname, color) +
                   ': ' + input(''), "roomId": room}
        client.send(pickle.dumps(message))

# Create a thread to run the receive function
receive_thread = threading.Thread(target=receive)

# Start the receive thread
receive_thread.start()

# Create a thread to run the write function
write_thread = threading.Thread(target=write)

# Start the write thread
write_thread.start()
