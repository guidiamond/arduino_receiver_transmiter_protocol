#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("comecou")

from enlace import *
import time
from PIL import Image

# Serial Com Port
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

    s_or_r = None

    while s_or_r not in ("s", "r"):
        s_or_r = input("Sender or Receiver? (s | r) ")
    
    if s_or_r == "s":
        txBuffer = open("26102.png", "rb").read()
        txLen = len(txBuffer)
        com.sendData(txLen)
        # checkDataLen, a = com.getData(64)
        # print("---------------")
        # print(type(checkDataLen))
        # print("---------------")
        # if checkDataLen.decode() == txLen:
        #     com.sendData(txBuffer)
        # else:
        #     print("erro no envio da imagem")

        # # espera o fim da transmissão
        # while(com.tx.getIsBussy()):
        #    print("enviando...")

    if s_or_r == "r":
        dataLen, _ = com.getData(64)
        com.sendData(dataLen)
        image, imageLen = com.getData(dataLen)


    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()
    print ("Transmitido       {} bytes ".format(txSize))

    #repare que o tamanho da mensagem a ser lida é conhecida!     
    rxBuffer, nRx = com.getData(txLen)

    # log
    print ("Lido              {} bytes ".format(nRx))
    print (rxBuffer)

    txSize = com.tx.getStatus()
    print ("Transmitido       {} bytes ".format(txSize))

    final = open("batata.png","wb").write(rxBuffer)

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
