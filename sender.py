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

    tk = Tk()
    tk.withdraw
    file_name = filedialog.askopenfilename()
    # head_type = cria_header(file_name)

    with open(file_name, "rb") as foto:
        txBuffer = foto.read()
    file_size = txBuffer.size()
    txLen = len(txBuffer)
    txLen_bytes = txLen.to_bytes(5, byteorder='big')
    tempo_inicial = time.time()

    com.sendData(txLen_bytes)
    tempo_final = time.time()

    checkDataLen, a = com.getData(5)
    
    if checkDataLen == txLen_bytes:
        com.sendData(txBuffer)
        check2DataLen, a2 = com.getData(5)
        print("envio foi um sucesso")
        print("-------------------------")
        print("Tempo de execução: ")
        tempo = tempo_final - tempo_inicial
        transmissao = str(txLen/(tempo*1000))
        print(transmissao + "kb/s")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
        
    else:
        print("erro no envio da imagem")
        
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()

def header_first(file_name):
    file_type = file_name[-3:]
    if file_type == "png":
        head_type = "1"
    elif file_type == "jpeg":
        head_type = "2"
    elif file_type == "jpg":
        head_type = "3"
    elif file_type == "gif":
        head_type = "4"
    return head_type

def header_generator(head_type, header_size):
    header = head_type + header_size
    return header