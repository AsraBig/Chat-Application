from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk


clients = {}
addresses = {}

HOST = "127.0.0.1"
PORT = 1234
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def accept_users():


    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the Chatroom", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):


    name = client.recv(BUFSIZ).decode("utf8")
 #  clinetName = SERVER.recv(1024).decode("utf-8")
    welcome = 'Welcome %s! if you Leave the chatroom anytime by typing {quit} to exit.' %name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name


    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""): 


    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


window = tk.Tk()
window.title("Server")

top_frame = tk.Frame(window)

label1 = tk.Label(top_frame, text="Names")
label2 = tk.Label(top_frame, text="Addresses")
add_button = tk.Button(top_frame, text="Connect")
label1.pack(side=tk.LEFT, padx=1)
label2.pack()
add_button.pack()
top_frame.pack(side=tk.TOP, pady=4)

message_frame = tk.Frame(window, width= 70, height=30, bd=2, bg="blue")
scrollbar = tk.Scrollbar(message_frame)
msg_list = tk.Listbox(message_frame, width=70, height=20, yscrollcommand=scrollbar.set)


tkDisplay = tk.Text(msg_list, height=20, width=40)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=5)

tkDisplay.insert(tk.END, "Waiting for Connection...\n")
tkDisplay.insert(tk.END, "User 1 => 127.0.0.1 : 3351\n")
tkDisplay.insert(tk.END, "User 2 => 127.0.0.1 : 6311\n")
tkDisplay.insert(tk.END, "User 3 => 127.0.0.1 : 9780\n")

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack()
message_frame.pack()


def receiver():
    while True:
        try:
         for i in addresses: 
            tkDisplay.insert(tk.END, "User => %s" %i)
        except OSError:
         break



if __name__ == "__main__":
    SERVER.listen(10)
    print("Waiting for Connection...")
    ACCEPT_THREAD = Thread(target=accept_users)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()  
    tk.mainloop()


 


