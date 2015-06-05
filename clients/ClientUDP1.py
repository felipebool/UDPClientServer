import sys
import socket
from time import sleep
sys.path.append('../messages')
import ProtocolMessages
from random import randint

class ClientUDP():
    hostname = "localhost"
    okResponse = 0
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, port1, port2, port3):
        self.delay = float(randint(3, 5))

        self.serverPort1 = port1
        self.serverPort2 = port2
        self.serverPort3 = port3

    def sendChangeMessage(self, message, port, sock):
        sock.sendto(message, (self.hostname, port))
        received = sock.recv(1024)
        self.manageMessages(received, sock, port)

    def manageMessages(self, data, sock, port):
        if (data == ProtocolMessages.Messages.OK):
            print "Recebi um OK do servidor/porta: " + str(port)
            self.okResponse = self.okResponse + 1

        elif (data == ProtocolMessages.Messages.NOK):
            print "Recebi um NOK do servidor/porta: " + str(port) + " -> Enviando ABORT"
            sock.sendto(ProtocolMessages.Messages.ABORT, (self.hostname, self.serverPort1))
            sock.sendto(ProtocolMessages.Messages.ABORT, (self.hostname, self.serverPort2))
            sock.sendto(ProtocolMessages.Messages.ABORT, (self.hostname, self.serverPort3))

    def checkOkAnswers(self, sock):
        if (self.okResponse == 3):
            print "Recebi OK de todos os servidores -> Enviando COMMIT"
            self.okResponse = 0
            sleep(self.delay)
            sock.sendto(ProtocolMessages.Messages.COMMIT, (self.hostname, self.serverPort1))
            sock.sendto(ProtocolMessages.Messages.COMMIT, (self.hostname, self.serverPort2))
            sock.sendto(ProtocolMessages.Messages.COMMIT, (self.hostname, self.serverPort3))

    def endCommunication(self, sock):
        sock.sendto(ProtocolMessages.Messages.END_COMMUNICATION, (self.hostname, self.serverPort1))
        sock.sendto(ProtocolMessages.Messages.END_COMMUNICATION, (self.hostname, self.serverPort2))
        sock.sendto(ProtocolMessages.Messages.END_COMMUNICATION, (self.hostname, self.serverPort3))

if __name__ == "__main__":
    client1 = ClientUDP(9999, 9998, 9997)

    for i in range(30):
        #1 SERVER
        client1.sendChangeMessage(ProtocolMessages.Messages.CHANGE, 9999, client1.serverSocket)
        sleep(client1.delay)
        #2 SERVER
        client1.sendChangeMessage(ProtocolMessages.Messages.CHANGE, 9998, client1.serverSocket)
        sleep(client1.delay)
        #3 SERVER
        client1.sendChangeMessage(ProtocolMessages.Messages.CHANGE, 9997, client1.serverSocket)
        sleep(client1.delay)
        client1.checkOkAnswers(client1.serverSocket)

    client1.endCommunication(client1.serverSocket)
