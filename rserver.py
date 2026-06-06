import os
import shutil
import socket
import threading
import time
from contextlib import redirect_stdout
from datetime import datetime
import json

os.chdir(sys._MEIPASS)

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

completeName = 'C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\rChat'
if not os.path.exists(completeName):
    os.mkdir(completeName)

# Connection Data
if not os.path.isfile(completeName + '\\port.ak47'):
    unu = open(completeName + "\\port.ak47", "x")
    with open(completeName + '\\port.ak47', 'w') as f:
        with redirect_stdout(f):
            print(8080)
    portb = 8080
else:
    with open(completeName + '\\port.ak47') as f:
        portb = f.read()
    if portb == "":
        with open(completeName + '\\port.ak47', 'w') as f:
            with redirect_stdout(f):
                print(8080)
        portb = 8080
q1 = input("Do you want to use the most recent port used (" + str(int(portb)) + ")? (Y/N): ")
if q1 == "y" or q1 == "Y":
    with open(completeName + '\\port.ak47') as f:
        port = int(f.read())
elif q1 == "n" or q1 == "N":
    port = int(input("Port: "))
    q2 = input("Do you want to use " + str(port) + " as the most recent port used? (Y): ")
    if q2 == "y" or q2 == "Y":
        with open(completeName + '\\port.ak47', 'w') as f:
            with redirect_stdout(f):
                print(port)
else:
    exit("Program expected Y/N, got OTHER instead")
print("rChat Server has started on port " + str(port))
now = datetime.now().astimezone()
if os.path.isfile(os.getcwd() + "\\chatlog.ak47"):
    if not os.path.exists(os.getcwd() + "\\chatlogs"):
        os.mkdir(os.getcwd() + "\\chatlogs")
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    src = os.getcwd() + "\\chatlog.ak47"
    dst = os.getcwd() + "\\chatlogs\\chatlog-" + dt_string + ".ak47"
    shutil.copy2(src, dst)
    os.remove(os.getcwd() + "\\chatlog.ak47")
else:
    dvar = open("chatlog.ak47", "x")
tm = now.strftime("%A, %d %B %Y")
tm2 = now.strftime("%I:%M:%S %p (%Z)")
with open('chatlog.ak47', 'a', encoding='utf-8') as f:
    f.write("\n\nrChat Server (Version 1.10-beta)\n" + tm + "\nServer is online since " + tm2 + "\n")
# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
msg = ""
# Lists For Clients and Their Nicknames
clients = []
nicknames = []
clients_lock = threading.Lock()


# Logging function
def log_message(message):
    with open('chatlog.ak47', 'a', encoding='utf-8') as f:
        f.write("\n" + message)


# Broadcasting function - sends to all clients except sender
def broadcast(message, sender_client=None):
    with clients_lock:
        for client in clients:
            if client != sender_client:
                try:
                    client.send(message)
                except:
                    pass


# System broadcast - sends to all clients
def broadcast_system(message):
    with clients_lock:
        for client in clients:
            try:
                client.send(message)
            except:
                pass


# Handling Messages From Clients
def handle(client, nickname):
    while True:
        time.sleep(0.01)
        try:
            # Receive message from client
            message = client.recv(1024)
            if not message:
                break
            
            # Decode message
            if isinstance(message, bytes):
                msg_text = message.decode('utf-8')
            else:
                msg_text = str(message)
            
            # Log the message
            log_entry = f"{nickname}: {msg_text}"
            log_message(log_entry)
            
            # Broadcast to other clients (NOT back to sender)
            broadcast_message = f"{nickname}: {msg_text}".encode('utf-8')
            broadcast(broadcast_message, sender_client=client)
            
        except Exception as e:
            break
    
    # Client disconnected
    with clients_lock:
        if client in clients:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            if index < len(nicknames):
                disconnected_nickname = nicknames[index]
                nicknames.pop(index)
            else:
                disconnected_nickname = nickname
    
    disconnect_msg = f"{disconnected_nickname} disconnected!".encode('utf-8')
    log_message(disconnect_msg.decode('utf-8'))
    broadcast_system(disconnect_msg)


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8').strip()
        
        # Validate nickname (reject GET requests)
        if len(nickname) >= 3 and nickname[0] == "G" and nickname[1] == "E" and nickname[2] == "T":
            client.close()
            continue
        
        with clients_lock:
            nicknames.append(nickname)
            clients.append(client)
        
        print("Nickname is {}".format(nickname))
        
        # Send welcome message to the new client
        client.send('Connected to server!'.encode('utf-8'))
        
        # Send chat history to new client
        try:
            with open('chatlog.ak47', 'r', encoding='utf-8') as f:
                history = f.read()
                client.send(history.encode('utf-8'))
        except:
            pass
        
        # Broadcast join message to other clients
        join_msg = "{} joined!".format(nickname).encode('utf-8')
        log_message(join_msg.decode('utf-8'))
        broadcast(join_msg, sender_client=client)

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client, nickname))
        thread.daemon = True
        thread.start()


receive()
