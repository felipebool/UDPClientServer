import SocketServer
from time import sleep
import Image
import socket
import sys

sys.path.append('../messages')
import ProtocolMessages

class ServerUDP (SocketServer.BaseRequestHandler):
    changeReceived = False

    def handle(self):
        self.data = self.request[0]
        socket = self.request[1]

        self.manageMessages(self.data, socket)

    def manageMessages(self, data, socket):
        if (data == ProtocolMessages.Messages.CHANGE):
            print "recebi um change "
            if (not ServerUDP.changeReceived):
                ServerUDP.changeReceived = True
                socket.sendto(ProtocolMessages.Messages.OK, self.client_address)
            else:
                socket.sendto(ProtocolMessages.Messages.NOK, self.client_address)

        elif (self.data == ProtocolMessages.Messages.COMMIT and ServerUDP.changeReceived):
            print "recebi um commit"
            self.commitDataModification()
            ServerUDP.changeReceived = False

        elif (self.data == ProtocolMessages.Messages.ABORT):
            print "recebi um abort"
            ServerUDP.changeReceived = False

    # A mensagem COMMIT padrao tem valor 5. Quando um servidor recebe uma
    # mensagem maior do que 5, ele sabe que acabou de receber um commit.
    # A diferenca entre o valor da mensagem recebida e o valor padrao para
    # a mensagem commit representa a cor do pixel que sera alterado por
    # aquele cliente. Desta forma, o valor da cor pega carona com a mensagem
    # COMMIT.
    def commitDataModification(self):
        print "commitDataModification"
        print str(self.server_address[1])

if __name__ == "__main__":
    HOST, PORT = "localhost", int(sys.argv[1])

    server = SocketServer.UDPServer((HOST, PORT), ServerUDP)
    server.serve_forever()

