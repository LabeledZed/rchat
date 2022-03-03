import random
import socket
import sys
import os
import threading
import time
import tkinter.scrolledtext as st
from tkinter import *
import psutil
from pypresence import Presence

# os.chdir(sys._MEIPASS) - Remove the comment when compiling

win = Tk()
win.config(bg="#1a1a1a")
win.title("rChat Beta Client")
win.resizable(False, False)


def disable_event():
    pass


hostb = "localip"

win.protocol("WM_DELETE_WINDOW", disable_event)


def cpr(p):
    for proc in psutil.process_iter():
        try:
            if p.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
    RPC = Presence(948257405169446952)
    try:
        RPC.connect()
    except:
        sys.exit()

    RPC.update(details="In the main menu",
               large_image='http://cdn.discordapp.com/attachments/879417908281901146/948264378002735185/rcc.png',
               large_text="rChat Client v1.02-beta", start=int(time.time()))

# Choosing Nickname
lbl0 = Label(win, text="rChat Beta Client v1.02", bg="#1a1a1a", fg="#8cb8ff", font=("Arial", 16))
lbl = Label(win, text="Nickname:", bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
ent = Entry(win, bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
lbl2 = Label(win, text="Server IP (blank for default):", bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
ent2 = Entry(win, bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
lbl3 = Label(win, text="Server Port (blank for default):", bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
ent3 = Entry(win, bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
lbl0.grid(column=0, row=0)
lbl.grid(column=0, row=1)
ent.grid(column=0, row=2)
lbl2.grid(column=0, row=3)
ent2.grid(column=0, row=4)
lbl3.grid(column=0, row=6)
ent3.grid(column=0, row=7)


def lip():
    global hostb

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

    hostb = (extract_ip())
    ent2.delete(0, END)
    ent2.insert(0, hostb)


btn5 = Button(win, text="Fill with Local IP", command=lip, bg="#1a1a1a", fg="#00ff00", font=("Arial", 13))
if cpr('rserver.exe'):
    btn5.grid(column=0, row=5)
ent.focus()


def exittt():
    if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
        global RPC
        RPC.close()
    sys.exit()


btn3 = Button(win, text="Exit", command=exittt, bg="#1a1a1a", fg="#ff0000", font=("Arial", 13))
btn3.grid(column=0, row=9)


def yesont(event):
    connectdef()


win.bind("<Return>", yesont)


def connectdef():
    global client
    global win
    global hostb
    if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
        global RPC
    if ent.get() == "":
        nickname = "User" + str(random.randint(100, 999))
    else:
        nickname = ent.get()

    if ent2.get() == "":
        host = "labeledzed.ddns.net"
    else:
        host = ent2.get()

    if ent3.get() == "":
        port = 64738
    else:
        port = int(ent3.get())

    btn3.grid_forget()
    lbl.grid_forget()
    ent.grid_forget()
    lbl2.grid_forget()
    ent2.grid_forget()
    lbl3.grid_forget()
    ent3.grid_forget()
    btn.grid_forget()
    btn5.grid_forget()
    cht = st.ScrolledText(win, width=60, height=20, font=("Arial", 11), bg="#1a1a1a", fg="#ffffff")
    cht.config(state="disabled")
    cht.grid(column=0, row=0, columnspan=4)
    if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
        RPC.update(details="Chatting as " + nickname,
                   large_image="http://cdn.discordapp.com/attachments/879417908281901146/948264378002735185/rcc.png",
                   large_text="rChat Client v1.02-beta", start=int(time.time()))

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Listening to Server and Sending Nickname
    def receive():
        global client
        time.sleep(0.01)
        while True:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = client.recv(1024).decode('ascii')
                if message == 'NICK':
                    client.send(nickname.encode('ascii'))
                else:
                    cht.config(state="normal")
                    cht.insert(INSERT, "\n" + message)
                    cht.see(END)
                    cht.config(state="disabled")
            except:
                # Close Connection When Error
                print("An error occured!")
                client.close()
                break

    # Sending Messages To Server
    def write():
        ent4 = Entry(win, width=60, bg="#1a1a1a", fg="#ffffff", font=("Arial", 10))
        ent4.grid(column=0, row=1)
        ent4.focus()
        btn2 = Button(win, text="Send", command=None, bg="#1a1a1a", fg="#ffffff", font=("Arial", 10))
        btn2.grid(column=1, row=1)
        win.bind()

        def sendd():
            client.send(message.encode('ascii'))
            ent4.delete(0, END)

        def senddd(event):
            client.send(message.encode('ascii'))
            ent4.delete(0, END)

        win.bind("<Return>", senddd)
        btn2.config(command=sendd)
        while True:
            time.sleep(0.01)
            message = '{}: {}'.format(nickname, ent4.get())

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

    win.title("rChat - Connected to " + host + ":" + str(port) + " as " + nickname)

    def exitt():
        global client
        client.close()
        if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
            global RPC
            RPC.close()
        try:
            client.send("".encode('ascii'))
        except:
            if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
                RPC.close()
            sys.exit()

    btn3.config(font=("Arial", 10), command=exitt)
    btn3.grid(column=2, row=1)


btn = Button(win, text="Connect", command=connectdef, bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
btn.grid(column=0, row=8)
win.mainloop()
