import socket
import threading
import sys

class Server:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.s.bind(('0.0.0.0', 5000))
        print("Server is running")
        self.s.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c, a = self.s.accept()
            conThread = threading.Thread(target = self.handler, args = (c, a))
            conThread.daemon = True
            conThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]), "connected")


class Client:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    name = ""

    def sendMsg(self):
        while True:
            self.s.send(bytes(self.name + ": " + input(""),'utf-8'))

    def __init__(self,address):
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.s.connect((address,5000))

        self.name = input("What's your name? ")
        print("You've logged in as", self.name)
        infThread = threading.Thread(target = self.sendMsg)
        infThread.daemon = True
        infThread.start()

        while True:
            data = self.s.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))

if (len(sys.argv) > 1):
    client = Client(sys.argv[1])
else:
     server = Server()
     server.run()
