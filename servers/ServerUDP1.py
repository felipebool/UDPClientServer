import SocketServer
from time import sleep
import Image
import socket
import sys
from random import randint

sys.path.append('../messages')
import ProtocolMessages

class ServerUDP(SocketServer.BaseRequestHandler):
    changeReceived = False
    endCommunication = 0
    messageReceived = 0
    importantData = ""

    def createFile(self, dataName):
        ServerUDP.importantData = open(dataName, 'w')
        ServerUDP.importantData.write('0')

    def handle(self):
        self.data = self.request[0]
        socket = self.request[1]

        self.manageMessages(self.data, socket)
        ServerUDP.messageReceived = ServerUDP.messageReceived + 1

    def manageMessages(self, data, socket):
        if (ServerUDP.messageReceived == 1):
            self.createFile("./importantData" + str(randint(200, 1000)))

        if (data == ProtocolMessages.Messages.CHANGE):
            if (not ServerUDP.changeReceived):
                print "recebi um change and changeReceived == false"
                ServerUDP.changeReceived = True
                socket.sendto(ProtocolMessages.Messages.OK, self.client_address)
            else:
                print "recebi um change and changeReceived == true"
                socket.sendto(ProtocolMessages.Messages.NOK, self.client_address)

        elif (self.data == ProtocolMessages.Messages.COMMIT and ServerUDP.changeReceived):
            print "recebi um commit"
            self.commitDataModification()
            ServerUDP.changeReceived = False

        elif (self.data == ProtocolMessages.Messages.ABORT):
            print "recebi um abort"
            ServerUDP.changeReceived = False

        elif (self.data == ProtocolMessages.Messages.END_COMMUNICATION):
            print "recebi um end_communication"
            ServerUDP.endCommunication = ServerUDP.endCommunication + 1
            if (ServerUDP.endCommunication == 3):
                print "entrei no checkEndOfCommunication e vou matar o servidor!"
                ServerUDP.finish(self)

    # A mensagem COMMIT padrao tem valor 5. Quando um servidor recebe uma
    # mensagem maior do que 5, ele sabe que acabou de receber um commit.
    # A diferenca entre o valor da mensagem recebida e o valor padrao para
    # a mensagem commit representa a cor do pixel que sera alterado por
    # aquele cliente. Desta forma, o valor da cor pega carona com a mensagem
    # COMMIT.
    def commitDataModification(self):
        valorAtual = int(ServerUDP.importantData.read(1))
        novoValor = valorAtual + 1
        ServerUDP.seek(0)
        ServerUDP.importantData.write(novoValor)
        ServerUDP.truncate()
        print "commitDataModification"

if __name__ == "__main__":
    HOST, PORT = "localhost", int(sys.argv[1])

    server = SocketServer.UDPServer((HOST, PORT), ServerUDP)
    server.serve_forever()

