from time import sleep
import ProtocolMessages
import socket
import sys

class ClientUDP():
    hostname = "localhost"

    def sendMessage(self, message, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message + "\n", (self.hostname, port))

        received = sock.recv(1024)
        self.manageMessages(received, sock, port)

    def manageMessages(self, data, socket, port):
        if (data.rstrip() == ProtocolMessages.Messages.OK):
            print "Recebi um OK do servidor"
            commit_message = ProtocolMessages.Messages.COMMIT + "\n"
            socket.sendto(commit_message, (self.hostname, port))
        elif (data.rstrip() == ProtocolMessages.Messages.NOK):
            print "Recebi um NOK do servidor"

if __name__ == "__main__":
    client1 = ClientUDP()
    print "Enviei um " + ProtocolMessages.Messages.CHANGE + " para o servidor"
    client1.sendMessage(ProtocolMessages.Messages.CHANGE, 9999)