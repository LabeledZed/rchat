import random
import socket
import os
from sys import exit
import threading
import time
import tkinter.scrolledtext as st
from tkinter import *
import psutil
from pypresence import Presence

win = Tk()
win.config(bg="#1a1a1a")
win.title("rChat Beta Client")
win.iconbitmap("rccc.ico")
win.resizable(False, False)
untrue = True
setup1 = True
client = None
receive_thread = None
write_thread = None
RPC = None

completeName = 'C:\\Users\\' + os.getlogin() + '\\AppData\\Roaming\\rChat'
if not os.path.exists(completeName):
    os.mkdir(completeName)

if not os.path.isfile(os.path.join(completeName, 'darkmode.ak47')):
    unu = open(os.path.join(completeName, 'darkmode.ak47'), "x")
    with open(os.path.join(completeName, 'darkmode.ak47'), 'w', encoding='utf-8') as f:
        f.write('0')
    with open(os.path.join(completeName, 'darkmode.ak47'), encoding='utf-8') as f:
        pred = int(f.read())

else:
    with open(os.path.join(completeName, 'darkmode.ak47'), encoding='utf-8') as f:
        pred = int(f.read())

if not os.path.isfile(os.path.join(completeName, 'username.ak47')):
    unu = open(os.path.join(completeName, 'username.ak47'), "x")


def disable_event():
    """Handle window close button"""
    on_exit()


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
    except Exception as e:
        print(f"Discord RPC connection failed: {e}")
        RPC = None

    if RPC:
        RPC.update(details="In the main menu",
                   large_image='http://cdn.discordapp.com/attachments/879417908281901146/948264378002735185/rcc.png',
                   large_text="rChat Client v1.10-beta", start=int(time.time()))

# Choosing Nickname
lbl0 = Label(win, text="rChat Beta Client v1.10", bg="#1a1a1a", fg="#8cb8ff", font=("Arial", 16))
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

with open(os.path.join(completeName, 'username.ak47'), encoding='utf-8') as f:
    usern = f.read().strip('\n')
ent.insert(INSERT, usern)


def lip():
    global hostb

    def extract_ip():
        sot = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sot.connect(('10.255.255.255', 1))
            IP = sot.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            sot.close()
        return IP

    hostb = (extract_ip())
    ent2.delete(0, END)
    ent2.insert(0, hostb)


btn5 = Button(win, text="Fill with Local IP", command=lip, bg="#1a1a1a", fg="#00ff00", font=("Arial", 13))
if cpr('rserver.exe'):
    btn5.grid(column=0, row=5)
ent.focus()


def on_exit():
    """Properly cleanup and exit the application"""
    global client
    global untrue
    global RPC
    global receive_thread
    global write_thread
    
    try:
        untrue = False
        
        # Close client socket if connected
        if client:
            try:
                client.close()
            except Exception as e:
                print(f"Error closing client socket: {e}")
        
        # Close Discord RPC
        if RPC:
            try:
                RPC.close()
            except Exception as e:
                print(f"Error closing Discord RPC: {e}")
        
        # Give threads a moment to finish
        if receive_thread and receive_thread.is_alive():
            receive_thread.join(timeout=1.0)
        if write_thread and write_thread.is_alive():
            write_thread.join(timeout=1.0)
        
        # Destroy the window
        win.destroy()
    except Exception as e:
        print(f"Error during exit: {e}")
        exit()


def yesont(event):
    connectdef()


win.bind("<Return>", yesont)


def connectdef():
    global client
    global untrue
    global win
    global cht
    global hostb
    global pred
    global RPC
    global receive_thread
    global write_thread
    
    if ent.get() == "":
        nickname = "User" + str(random.randint(100, 999))
    else:
        nickname = ent.get()
        with open(os.path.join(completeName, 'username.ak47'), 'w', encoding='utf-8') as f:
            f.write(nickname)

    if ent2.get() == "":
        host = "labeledzed.ddns.net"
    else:
        host = ent2.get()

    if ent3.get() == "":
        port = 64738
    else:
        port = int(ent3.get())

    lbl.grid_forget()
    ent.grid_forget()
    lbl2.grid_forget()
    ent2.grid_forget()
    lbl3.grid_forget()
    ent3.grid_forget()
    btn.grid_forget()
    btn5.grid_forget()

    cht.grid(column=0, row=0, columnspan=4)
    if RPC:
        try:
            RPC.update(details="Chatting as " + nickname,
                       large_image="http://cdn.discordapp.com/attachments/879417908281901146/948264378002735185/rcc.png",
                       large_text="rChat Client v1.10-beta", start=int(time.time()))
        except Exception as e:
            print(f"Error updating Discord RPC: {e}")

    # Connecting To Server
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # Listening to Server and Sending Nickname
    def receive():
        global client
        global untrue
        time.sleep(0.01)
        while untrue and client:
            try:
                # Receive Message From Server
                # If 'NICK' Send Nickname
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                if message == 'NICK':
                    try:
                        client.send(nickname.encode('utf-8'))
                    except Exception as e:
                        print(f"Error sending nickname: {e}")
                        break
                else:
                    try:
                        cht.config(state="normal")
                        cht.insert(INSERT, "\n" + message)
                        cht.see(END)
                        cht.config(state="disabled")
                    except Exception as e:
                        print(f"Error updating chat: {e}")
                        break
            except Exception as e:
                print(f"Receive error: {e}")
                break

    # Sending Messages To Server
    def write():
        global untrue
        ent4.grid(column=0, row=1)
        btn2.grid(column=1, row=1)
        ent4.focus()

        def sendd():
            global client
            msg_text = ent4.get()
            if msg_text.strip() and client:  # Only send non-empty messages
                try:
                    client.send(msg_text.encode('utf-8'))
                    ent4.delete(0, END)
                except Exception as e:
                    print(f"Error sending message: {e}")

        def senddd(event):
            global client
            msg_text = ent4.get()
            if msg_text.strip() and client:  # Only send non-empty messages
                try:
                    client.send(msg_text.encode('utf-8'))
                    ent4.delete(0, END)
                except Exception as e:
                    print(f"Error sending message: {e}")

        win.bind("<Return>", senddd)
        btn2.config(command=sendd)
        while untrue:
            time.sleep(0.01)

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive, daemon=True)
    receive_thread.start()

    write_thread = threading.Thread(target=write, daemon=True)
    write_thread.start()

    win.title("rChat - Connected to " + host + ":" + str(port) + " as " + nickname)

    def exitt():
        on_exit()

    menubar.delete("Exit")
    menubar.add_command(label="Exit", command=exitt)


btn = Button(win, text="Connect", command=connectdef, bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
btn.grid(column=0, row=8)

cht = st.ScrolledText(win, width=60, height=20, font=("Arial", 11), bg="#1a1a1a", fg="#ffffff")
cht.config(state="disabled")

ent4 = Entry(win, width=65, bg="#1a1a1a", fg="#ffffff", font=("Arial", 10))
btn2 = Button(win, text="Send", command=None, bg="#1a1a1a", fg="#ffffff", font=("Arial", 10))


def dark():
    lbl0.config(bg="#1a1a1a", fg="#8cb8ff")
    lbl.config(bg="#1a1a1a", fg="#ffffff")
    ent.config(bg="#1a1a1a", fg="#ffffff")
    lbl2.config(bg="#1a1a1a", fg="#ffffff")
    ent2.config(bg="#1a1a1a", fg="#ffffff")
    lbl3.config(bg="#1a1a1a", fg="#ffffff")
    ent3.config(bg="#1a1a1a", fg="#ffffff")
    btn.config(bg="#1a1a1a", fg="#ffffff")
    btn5.config(bg="#1a1a1a", fg="#00ff00")
    cht.config(bg="#1a1a1a", fg="#ffffff")
    win.config(bg="#1a1a1a")
    btn2.config(bg="#1a1a1a", fg="#ffffff")
    ent4.config(bg="#1a1a1a", fg="#ffffff")


def light():
    lbl0.config(bg="#ffffff", fg="#2e7eff")
    lbl.config(bg="#ffffff", fg="#000000")
    ent.config(bg="#cccccc", fg="#000000")
    lbl2.config(bg="#ffffff", fg="#000000")
    ent2.config(bg="#cccccc", fg="#000000")
    lbl3.config(bg="#ffffff", fg="#000000")
    ent3.config(bg="#cccccc", fg="#000000")
    btn.config(bg="#cccccc", fg="#000000")
    btn5.config(bg="#cccccc", fg="#006900")
    cht.config(bg="#ffffff", fg="#000000")
    win.config(bg="#ffffff")
    btn2.config(bg="#cccccc", fg="#000000")
    ent4.config(bg="#cccccc", fg="#000000")


def darkmode():
    global pred
    global cht
    global btn2
    global ent4
    if pred == 0:
        if darkmodee.get() == 0:
            dark()
            cht.config(state="normal")
            chttemp = cht.get(1.0, END)[:-1]
            cht.delete(1.0, END)
            cht.insert(INSERT, chttemp)
            cht.see(END)
            cht.config(state="disabled")
            with open(os.path.join(completeName, 'darkmode.ak47'), 'w', encoding='utf-8') as f:
                f.write('0')
        elif darkmodee.get() == 1:
            light()
            cht.config(state="normal")
            chttemp = cht.get(1.0, END)[:-1]
            cht.delete(1.0, END)
            cht.insert(INSERT, chttemp)
            cht.see(END)
            cht.config(state="disabled")
            with open(os.path.join(completeName, 'darkmode.ak47'), 'w', encoding='utf-8') as f:
                f.write('1')
    else:
        if darkmodee.get() == 1:
            dark()
            cht.config(state="normal")
            chttemp = cht.get(1.0, END)[:-1]
            cht.delete(1.0, END)
            cht.insert(INSERT, chttemp)
            cht.see(END)
            cht.config(state="disabled")
            with open(os.path.join(completeName, 'darkmode.ak47'), 'w', encoding='utf-8') as f:
                f.write('0')
        elif darkmodee.get() == 0:
            light()
            cht.config(state="normal")
            chttemp = cht.get(1.0, END)[:-1]
            cht.delete(1.0, END)
            cht.insert(INSERT, chttemp)
            cht.see(END)
            cht.config(state="disabled")
            with open(os.path.join(completeName, 'darkmode.ak47'), 'w', encoding='utf-8') as f:
                f.write('1')


menubar = Menu(win)
viewmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
darkmodee = IntVar()
win.config(menu=menubar)
menubar.add_command(label="Exit", command=on_exit)
if setup1:
    if pred == 0:
        dark()
        viewmenu.add_checkbutton(label="Darkmode", onvalue=0, offvalue=1, variable=darkmodee, command=darkmode)
        setup1 = False
    else:
        light()
        viewmenu.add_checkbutton(label="Darkmode", onvalue=1, offvalue=0, variable=darkmodee, command=darkmode)
        setup1 = False

win.mainloop()
