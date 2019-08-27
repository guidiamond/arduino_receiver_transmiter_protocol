from PIL import Image
import time
from enlace import *
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
serialName = "/dev/ttyACM0"
# serialName = "COM8"

def main():
    # Inicia enlance
    com = enlace(serialName)
    # Ativa comunicacao
    com.enable()

    # Log
    print("-------------------------")
    print("Inicializando comunicação")
    print("porta : {}".format(com.fisica.name))
    print("-------------------------")
    tempo_inicial = time.time()

    # Carregamento da imagem
    txBuffer = open("26102.png", "rb").read()
    txLen = len(txBuffer)

    # Transmite dado
    print("Transmitindo {} bytes".format(txLen))
    com.sendData(txBuffer)

    # espera o fim da transmissão
    while(com.tx.getIsBussy()):
        txSize = com.tx.getStatus()
        print("Transmitido       {} bytes ".format(txSize))

    try:
        txReceived, tx_received_len = com.getData(10)
        tempo_final = time.time()
        if txReceived.decode('utf-8') == txLen:
            tempo = tempo_final - tempo_inicial
            print(tempo)
            print("Sucesso no Envio!")
    except:
        print("erro na transmissão")
        
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
