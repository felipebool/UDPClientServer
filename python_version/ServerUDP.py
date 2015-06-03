import SocketServer
from time import sleep
import ProtocolMessages
import Image
import socket
import sys

class ServerUDP (SocketServer.BaseRequestHandler):
    changeReceived = False

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]

    #    print "{} wrote:".format(self.client_address[0])
    #    print data
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
            print "Entrei no commitDataModification"

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.UDPServer((HOST, PORT), ServerUDP)
    server.serve_forever()

#socket.sendto(data.upper(), self.client_address)