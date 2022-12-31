import socket
import threading
import pickle
from termcolor import colored
from pyfiglet import Figlet

# Choosing an unreserved port
port = 7976

# Create a socket and bind it to the host and port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), port))
server.listen()


# Create lists to store connected clients and their data
clients = []
clientData = []

# Print an ASCII art banner with the text "Py Chat Server Running"
f = Figlet(font='larry3d')
print(f.renderText('Py Chat Server Running'))

# Print the hostname and port that the server is listening on
print('Listening at port 7976, hostname:', socket.gethostname())

def broadcast(message):
    """Broadcast a message to all connected clients"""
    for client in clients:
        client.send(message)


def handle(client):
    """Receive and broadcast messages from a single client"""
    while True:
        try:
            # Receive a message from the client
            message = client.recv(1024)
            # Broadcast the message to all other clients
            broadcast(message)
        except:
            # If an error occurs, remove the client and close the connection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            # Remove the client's data from the list
            data = clientData[index]
            nickname = data['name']
            # Broadcast a message to all other clients that the client has left
            broadcast(pickle.dumps({'msg': colored(nickname + ' left', 'red'),
                                   "roomId": data['roomId']}))
            print(nickname + ' left!')
            clientData.remove(data)
            break


def receive():
    """Accept new client connections and start a thread for each one"""
    while True:
        # Accept a new connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        # Send a message to the client asking for their data
        client.send(pickle.dumps({'type': 'server', 'q': 'data'}))
        # Receive the client's data
        msg = client.recv(1024)
        data = pickle.loads(msg)
        # Add the client's data to the list
        clientData.append(data)
        clients.append(client)
        print("Nickname is {}".format(data['name']))
        # Broadcast a message to all other clients that the new client has joined
        broadcast(pickle.dumps(
            {"msg": colored("{} joined!".format(data['name']), 'green'), "roomId": data['roomId']}))
        # Send a message to the new client with the room id
        client.send(pickle.dumps(
            {"msg": f"Connected to Sever! Room ID:{data['roomId']}", "roomId": data['roomId']}))
        # Start a new thread to handle the new client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
