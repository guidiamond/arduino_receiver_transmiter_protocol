#!/usr/bin/env python3
# -*- coding: utf-8 -*-
print("comecou")

from enlace import *
import time
from tkinter import filedialog, Tk

# Serial Com Port
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

    # if s_or_r == "r":
    dataLen, aa_ = com.getData(5)
    # print(int.from_bytes(dataLen, "big"))
    com.sendData(dataLen)

    dataLen_int = int.from_bytes(dataLen, "big")
    print(dataLen_int)
    image, imageLen = com.getData(dataLen_int)
    imageLen_bytes = imageLen.to_bytes(5, "big")
    com.sendData(imageLen_bytes)

    with open("ULTRAbatata.jpg", "wb") as foto:
    	foto.write(image)



    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
