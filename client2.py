import socket
import threading
import tkinter as tk


class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Client 1")

        # create label and entry widgets for IP address
        self.label_ip = tk.Label(self.root, text="IP Address:")
        self.label_ip.pack()
        self.entry_ip = tk.Entry(self.root)
        self.entry_ip.pack()

        # create label and entry widgets for port
        self.label_port = tk.Label(self.root, text="Port:")
        self.label_port.pack()
        self.entry_port = tk.Entry(self.root)
        self.entry_port.pack()

        # create button widget to connect to server
        self.button_connect = tk.Button(self.root, text="Connect", command=self.connect)
        self.button_connect.pack()

        # create text widget to display messages
        self.text = tk.Text(self.root)
        self.text.pack()

        # create entry widget and button widget to send messages
        self.entry_message = tk.Entry(self.root)
        self.entry_message.pack()
        self.button_send = tk.Button(self.root, text="Send", command=self.send_message)
        self.button_send.pack()

        # set a protocol for closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    # function to connect to the server
    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.entry_ip.get(), int(self.entry_port.get())))
        # create a thread to receive messages from the server
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    # function to receive messages from the server
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                if message.startswith("Server: "):
                    self.text.insert("end", message)
                else:
                    self.text.insert("end", f"By Server: {message} \n")
            except:
                self.client.close()
                return

    # function to send messages to the server
    def send_message(self):
        message = self.entry_message.get()
        self.client.send(message.encode())
        self.entry_message.delete(0, "end")

    # function to close the window and close the socket connection
    def on_closing(self):
        self.client.close()
        self.root.destroy()


if __name__ == '__main__':
    ClientGUI()
