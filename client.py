import socket
import threading
from tkinter import *
import tkinter.scrolledtext as st
import random
import time
import sys
import psutil

win = Tk()
win.config(bg="#1a1a1a")
win.title("rChat Client")
win.resizable(False, False)


def disable_event():
    pass


lipp = False
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


# Choosing Nickname
lbl0 = Label(win, text="rText Client v1.01", bg="#1a1a1a", fg="#8cb8ff", font=("Arial", 16))
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
    global lipp

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
    lipp = True
    ent2.delete(0, END)
    ent2.insert(0, hostb)


btn5 = Button(win, text="Fill with Local IP", command=lip, bg="#1a1a1a", fg="#00ff00", font=("Arial", 13))
if cpr('rserver.exe'):
    btn5.grid(column=0, row=5)
ent.focus()


def exitt():
    sys.exit()


btn3 = Button(win, text="Exit", command=exitt, bg="#1a1a1a", fg="#ff0000", font=("Arial", 13))
btn3.grid(column=0, row=9)


def yesont(event):
    connectdef()


win.bind("<Return>", yesont)


def connectdef():
    global win
    global hostb
    global lipp
    if ent.get() == "":
        nickname = "User" + str(random.randint(100, 999))
    else:
        nickname = ent.get()

    if lipp:
        host = hostb
    else:
        if ent2.get() == "":
            host = "labeledzed.ddns.net"
        else:
            host = ent2.get()

    if ent3.get() == "":
        port = 64738
    else:
        port = int(ent3.get())

    btn3.grid_forget()
    btn3.config(font=("Arial", 10))
    btn3.grid(column=2, row=1)

    lbl.grid_forget()
    ent.grid_forget()
    lbl2.grid_forget()
    ent2.grid_forget()
    lbl3.grid_forget()
    ent3.grid_forget()
    btn.grid_forget()
    cht = st.ScrolledText(win, width=60, height=20, font=("Arial", 11), bg="#1a1a1a", fg="#ffffff")
    cht.config(state="disabled")
    cht.grid(column=0, row=0, columnspan=4)

    # Connecting To Server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Listening to Server and Sending Nickname
    def receive():
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


btn = Button(win, text="Connect", command=connectdef, bg="#1a1a1a", fg="#ffffff", font=("Arial", 13))
btn.grid(column=0, row=8)
win.mainloop()
