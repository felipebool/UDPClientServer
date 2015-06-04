from time import sleep
from random import randint

import socket
import sys

sys.path.append('../messages')
import ProtocolMessages

class ClientUDP():
    hostname = "localhost"
    delay = 0

    okFromServer1 = False
    okFromServer2 = False
    okFromServer3 = False

    # Construtor da classe, inicializa atributo delay. O delay determina o
    # tempo que o cliente irá esperar para enviar a mensagem commit para o
    # servidor, o valor deste atributo varia de 0 a 5 segundos.
    def __init__(self):
        self.delay = float(random.randint(0,5))

    def sendMessage(self, message, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message + "\n", (self.hostname, port))

        received = sock.recv(1024)
        self.manageMessages(received, sock, port)

    def manageMessages(self, data, socket, port):
        if (data.rstrip() == ProtocolMessages.Messages.OK):
            print "Recebi um OK do servidor"

            sleep(self.delay)
            commit_message = ProtocolMessages.Messages.COMMIT + "\n"
            socket.sendto(commit_message, (self.hostname, port))
        elif (data.rstrip() == ProtocolMessages.Messages.NOK):
            print "Recebi um NOK do servidor"

if __name__ == "__main__":
    client1 = ClientUDP()

    for i in range(0, )
    #1 SERVER
	client1.sendMessage(ProtocolMessages.Messages.CHANGE, 9999)

    #2 SERVER
    client1.sendMessage(ProtocolMessages.Messages.CHANGE, 9998)

    #3 SERVER
    client1.sendMessage(ProtocolMessages.Messages.CHANGE, 9997)
