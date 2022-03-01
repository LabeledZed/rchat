import threading
import socket
import time
import os
from contextlib import redirect_stdout
import shutil
from datetime import datetime


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


host = (extract_ip())

# Connection Data
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
print("rChat Server has started on port " + str(port))
now = datetime.now()
if not os.path.exists(os.getcwd() + "\\chatlogs"):
    os.mkdir(os.getcwd() + "\\chatlogs")
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
src = os.getcwd() + "\\chatlog.ak47"
dst = os.getcwd() + "\\chatlogs\\chatlog-" + dt_string + ".ak47"
shutil.copy2(src, dst)
os.remove(os.getcwd() + "\\chatlog.ak47")
with open('chatlog.ak47', 'a') as f:
    f.write("\n\nrChat (Version 1.01-beta) - " + time.ctime() + "\n")
# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
msg = ""
# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    global msg
    for client in clients:
        client.send(message)
    with open('chatlog.ak47', 'a') as f:
        g = str(message).replace("b'", "")
        g = g.replace("'", "")
        f.write("\n" + g)


# Handling Messages From Clients
def handle(client):
    while True:
        time.sleep(0.01)
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
            broadcast('{} disconnected!'.format(nickname).encode('ascii'))
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
        if not nickname[0] == "G" and not nickname[1] == "E" and not nickname[2] == "T":
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
