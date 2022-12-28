import socket
import threading
import pickle
from termcolor import colored
from pyfiglet import Figlet

host = '192.168.1.50'  # LocalHost
port = 7976  # Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), port))  # binding host and port to socket
server.listen()

print('Listening at port 7976, hostname:', socket.gethostname())

clients = []
clientData = []

f = Figlet(font='larry3d')
print(f.renderText('Py Chat Server Running'))


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            data = clientData[index]
            nickname = data['name']
            broadcast(pickle.dumps({'msg': colored(nickname + ' left', 'red'),
                      "roomId": data['roomId']}))
            print(nickname+' left!')
            clientData.remove(data)
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        client.send(pickle.dumps({'type': 'server', 'q': 'data'}))
        msg = client.recv(1024)
        data = pickle.loads(msg)
        clientData.append(data)
        clients.append(client)
        print("Nickname is {}".format(data['name']))
        broadcast(pickle.dumps(
            {"msg": colored("{} joined!".format(data['name']), 'green'), "roomId": data['roomId']}))
        client.send(pickle.dumps(
            {"msg": f"Connected to Sever! Room ID:{data['roomId']}", "roomId": data['roomId']}))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
