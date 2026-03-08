#------------------------------------------------------------------
# CHAT APPLICATION - Client
#------------------------------------------------------------------
import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from tkinter.scrolledtext import ScrolledText

HOST = "localhost"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

root = tk.Tk()
root.withdraw()

name = simpledialog.askstring("Name", "Enter your name")

chat_window = tk.Toplevel(root)
chat_window.title("Chat Application")

chat_area = ScrolledText(chat_window)
chat_area.pack()

message_entry = tk.Entry(chat_window)
message_entry.pack()

def write():
    message = f"{name}: {message_entry.get()}"
    client.send(message.encode())
    message_entry.delete(0, tk.END)

send_button = tk.Button(chat_window, text="Send", command=write)
send_button.pack()

def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "NAME":
                client.send(name.encode())
            else:
                chat_area.insert(tk.END, message + "\n")
                chat_area.yview(tk.END)   # auto scroll

        except:
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

root.mainloop()
