import threading
import socket
import time
import os
from contextlib import redirect_stdout

# Connection Data
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
host = s.getsockname()[0]
s.close()

if not os.path.isfile('port.ak47'):
    unu = open("port.ak47", "x")
    with open('port.ak47', 'w') as f:
        with redirect_stdout(f):
            print(8080)
    portb = 8080
else:
    with open('port.ak47') as f:
        portb = f.read()
    if portb == "":
        with open('port.ak47', 'w') as f:
            with redirect_stdout(f):
                print(8080)
        portb = 8080

q1 = input("Do you want to use the most recent port used (" + str(int(portb)) + ")? (Y/N): ")
if q1 == "y" or q1 == "Y":
    with open('port.ak47') as f:
        port = int(f.read())
elif q1 == "n" or q1 == "N":
    port = int(input("Port: "))
    q2 = input("Do you want to use " + str(port) + " as the most recent port used? (Y): ")
    if q2 == "y" or q2 == "Y":
        with open('port.ak47', 'w') as f:
            with redirect_stdout(f):
                print(port)
else:
    exit("Program expected Y/N, got OTHER instead")

print("Server started on port " + str(port))
with open('chatlog.ak47', 'a') as f:
    f.write("\n"+time.ctime())
# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
msg=""
# Lists For Clients and Their Nicknames
clients = []
nicknames = []
# Sending Messages To All Connected Clients
def broadcast(message):
    global msg
    for client in clients:
        client.send(message)
    with open('chatlog.ak47', 'a') as f:
        g = str(message).replace("b'","")
        g = g.replace("'","")
        f.write("\n" + g)
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)



        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        with open('chatlog.ak47', 'r') as f:
            client.send(f.read().encode('ascii'))


        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()
broadcast(time.ctime())
