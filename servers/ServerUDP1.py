import SocketServer
from time import sleep
import Image
import socket
import sys

sys.path.append('../messages')
import ProtocolMessages

class ServerUDP (SocketServer.BaseRequestHandler):
    changeReceived = False
    pointX = 0
    pointY = 0

    def __init__(self):
        self.img = Image.new('RGB', (255, 255), "black")
        self.pixels = self.img.load()

    def handle(self):
        self.data = self.request[0].strip()
        socket = self.request[1]

        self.manageMessages(data, socket)

    def manageMessages(self, data, socket):
        print "Recebi um  " + data + " do cliente: " + self.client_address[0]

        if (data == ProtocolMessages.Messages.CHANGE):
            if (not ServerUDP.changeReceived):
                ServerUDP.changeReceived = True
                print "Enviando um " + ProtocolMessages.Messages.OK + " para o cliente"
                ok_message = ProtocolMessages.Messages.OK + "\n"
                socket.sendto(ok_message, self.client_address)

            else:
                print "Enviando um " + ProtocolMessages.Messages.NOK + " para o cliente"
                nok_message = ProtocolMessages.Messages.NOK + "\n"
                socket.sendto(nok_message.upper(), self.client_address)

        elif (data == ProtocolMessages.Messages.COMMIT):
            self.commitDataModification()
            ServerUDP.changeReceived = False

        elif (data == ProtocolMessages.Messages.ABORT):
            ServerUDP.changeReceived = False

    def commitDataModification(self):
        # A mensagem COMMIT padrão tem valor 5. Quando um servidor recebe uma
        # mensagem maior do que 5, ele sabe que acabou de receber um commit.
        # A diferença entre o valor da mensagem recebida e o valor padrão para
        # a mensagem commit representa a cor do pixel que será alterado por
        # aquele cliente. Desta forma, o valor da cor pega carona com a mensagem
        # COMMIT.
        ServerUDP.pixels[ServerUDP.pointX, ServerUDP.pointY] = (ServerUDP.pointX, ServerUDP.pointY, this.data - ProtocolMessages.Messages.COMMIT)
        ServerUDP.pointX = ServerUDP.pointX + 1
        ServerUDP.pointY = ServerUDP.pointY + 1
        print "Entrei no commitDataModification"

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.UDPServer((HOST, PORT), ServerUDP)
    server.serve_forever()

#socket.sendto(data.upper(), self.client_address)
