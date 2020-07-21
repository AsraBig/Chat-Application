from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import messagebox
#
#from tkinter import colorchooser
#

PORT = 1234
BUFSIZ = 1024
ADDR = ("127.0.0.1", PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

Username = input('Enter Your name: ')
#print("Welcome to the Server, " + Username)
#client_socket.send(bytes(Username, 'utf-8'))
#print(client_socket.send(bytes(Username, 'utf-8'))

#def popup():
#    messagebox.showinfo("Information", "Username: "+ Username)

#def color():
#    my_color = colorchooser.askcolor()

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:
           break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def close(event=None):
    my_msg.set("{quit}")
    send()

def clear():
    entry_field.delete(0, 'end')

top = tk.Tk()
top.title(Username)

messages_frame = tk.Frame(top, width= 150, height=190, bd=3, bg="purple")

#messages_frame.grid(row=1, column=1 ,columnspan=6, padx=20, pady=20)
my_msg = tk.StringVar()
my_msg.set("Type Your Username for Chatroom")
scrollbar = tk.Scrollbar(messages_frame)


msg_list = tk.Listbox(messages_frame, height=15, width=60, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
#msg_list.pack()
messages_frame.pack()


field_frame = tk.Frame(top, width= 30, height=60, bd=3, bg="purple")
entry_field = tk.Entry(field_frame, textvariable=my_msg, width=60)
entry_field.bind("<Return>", send)
entry_field.pack(pady=2)
send_button = tk.Button(field_frame, text="Send", command=send, bg="#006400", fg="white", width=26, height=2)
clear_button = tk.Button(field_frame, text="Clear", command=clear, bg="#DC143C", fg="white", width=26, height=2)
#pop_button = tk.Button(top, text="Username", command=popup)
#pop_button.pack(pady=10)
#color_button = tk.Button(top, text="Change Color", command=color)
#color_button.pack(pady=5)
send_button.pack(side=tk.LEFT)
clear_button.pack(side=tk.LEFT)
field_frame.pack()
#top.protocol("WM_DELETE_WINDOW", close)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()
