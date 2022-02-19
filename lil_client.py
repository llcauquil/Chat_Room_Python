# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)

import socket
import random
from threading import Thread
from datetime import datetime
import tkinter
from tkinter.simpledialog import askstring
from tkinter import *

# init colors
app_color = "#063646" 
colors = ["Red", "Blue", "Green"]
client_color = random.choice(colors)

# networking constants
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))# how you talk to other computers

# setting name of client
name = askstring("login", f"Connected to:\n{SERVER_HOST}:{SERVER_PORT}\nWhat's ur name?")

def send_message():
    to_send = str(text_entry.get())
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"[{date_now}] {name}{separator_token}{to_send}"
    
    # finally, send the message
    s.send(to_send.encode())
    text_entry.delete(0, END)

c = 50 #scalar to multiply screen size by hard coded 16:9 phone screen ratio, for UI design
WIDTH = 9*c
HEIGHT = 16*c

#UI display made from standard lib tkinter
window = tkinter.Tk()
window.title(f"Lil'Client ~{name}~")
window.resizable(width=False, height=False)
window.config(height=HEIGHT, width=WIDTH,  bg=app_color)

# canvas = Canvas(bg="Black", height=16*c, width=9*c, highlightthickness=0)
# canvas.config(scrollregion=canvas.bbox("all"))
# canvas.grid(column=0, row=2)

textCons = Text(            window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)

textCons.place(             relheight = 0.90,
							relwidth = 1,
							rely = 0.01)

textCons.config(cursor = "arrow")

scrollbar = Scrollbar(textCons)
scrollbar.place(relheight=1, relx=0.974)
scrollbar.config(command=textCons.yview)

text_entry = Entry(width=50, bg="white")
text_entry.focus()
text_entry.place(rely = 0.9, relwidth=1)

send_button = Button(text="Send", command=send_message)
send_button.place(relx=0.92, rely=0.9)

textCons.config(state=DISABLED)


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        textCons.config(state=NORMAL)
        textCons.insert(END, message+"\n")
        textCons.config(state = DISABLED)
        textCons.see(END)


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

window.mainloop()
s.close()