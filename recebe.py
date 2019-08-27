from PIL import Image
import time
from enlace import *
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
serialName = "/dev/ttyACM1"
# serialName = "COM8"


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)
    # Ativa comunicacao
    com.enable()

    # Log
    print("-------------------------")
    print("Inicializando comunicação")
    print("porta : {}".format(com.fisica.name))
    print("-------------------------")

    rxBuffer, rxLen = com.getData(8)
    
    # Transmite dado
    print("Transmitindo {} bytes".format(rxLen))
    com.sendData(rxLen)

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        txSize = com.tx.getStatus()
        print("Transmitido       {} bytes ".format(txSize))

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
