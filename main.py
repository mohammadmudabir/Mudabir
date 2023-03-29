import socket
import threading
import tkinter as tk

class ServerGUI:
    def __init__(self, server):
        self.server = server
        self.clients = [] # list of connected clients
        self.root = tk.Tk()
        self.root.title("Server")
        self.label = tk.Label(self.root, text="Server is running...")
        self.label.pack()
        self.text = tk.Text(self.root) # textbox to display messages
        self.text.pack()
        self.listbox = tk.Listbox(self.root) # listbox to display connected clients
        self.listbox.pack()
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()
        self.message_label = tk.Label(self.input_frame, text="Message:")
        self.message_label.pack(side="left")
        self.message_entry = tk.Entry(self.input_frame)
        self.message_entry.pack(side="left")
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="left")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        self.root.mainloop()

    def receive(self):
        while True:
            try:
                client, addr = self.server.accept()
                self.clients.append(client)
                self.listbox.insert("end", str(addr)) # add client address to listbox
                self.text.insert("end", f"Connected to {addr}\n")
                client_thread = threading.Thread(target=self.handle_client, args=(client,))
                client_thread.start()
            except:
                break

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024).decode()
                if message:
                    self.text.insert("end", f"{message}\n")
            except:
                client.close()
                self.clients.remove(client)
                self.listbox.delete(0, "end") # remove disconnected client from listbox
                for c in self.clients:
                    self.listbox.insert("end", str(c.getpeername())) # update listbox with remaining clients
                return

    def send_message(self):
        message = self.message_entry.get()
        selected_index = self.listbox.curselection() # get index of selected client in listbox
        if selected_index:
            selected_client = self.clients[selected_index[0]]
            selected_client.send(message.encode())
            self.text.insert("end", f"Server: {message}\n")
        else:
            self.text.insert("end", "No client selected!\n")
        self.message_entry.delete(0, "end")

    def on_closing(self):
        for client in self.clients:
            client.close()
        self.server.close()
        self.root.destroy()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8080))
    server.listen()
    ServerGUI(server)

if __name__ == '__main__':
    start_server()
