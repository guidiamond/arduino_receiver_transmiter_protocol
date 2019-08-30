#!/usr/bin/env python3
# -- coding: utf-8 --
from tkinter import filedialog, Tk
import time
from enlace import *
import numpy as np
print("comecou")
from math import floor

# Serial Com Port
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)


def main():
    # Inicializa enlace
    com = enlace(serialName)
    # Ativa comunicacao
    com.enable()

    # tk = Tk()
    # tk.withdraw
    # file_name = filedialog.askopenfilename()

    def file_spliter(raw_file, split_size):
        raw_file_size = len(raw_file)
        n = floor(raw_file_size / split_size)

        l_pacotes = []

        for e in range(0,n):            
            pkg = raw_file[:split_size]
            l_pacotes.append(pkg)

            raw_file = raw_file[split_size:]
            
        l_pacotes.append(raw_file)

        return l_pacotes


    def byte_stuffing(payload):
        EOP = bytearray([0xF1, 0xF2, 0xF3, 0xF4])
        EOP_stuffing = bytearray(
            [0x00, 0xF1, 0x00, 0xF2, 0x00, 0xF3, 0x00, 0xF4])
        payload_stuffed = payload.replace(EOP, EOP_stuffing)

        return payload_stuffed

    def undo_byte_stuffing(message):

        EOP = bytearray([0xF1, 0xF2, 0xF3, 0xF4])
        EOP_stuffing = bytearray(
            [0x00, 0xF1, 0x00, 0xF2, 0x00, 0xF3, 0x00, 0xF4])

        byte_message = message.replace(EOP_stuffing, EOP)

        return byte_message

    def add_header_eop(payload, n, total_pacotes):
        # eop
        EOP = bytearray([0xF1, 0xF2, 0xF3, 0xF5])
        # header
        data_size = (len(payload)+len(EOP)).to_bytes(8, byteorder='big')

        #        num pacote,                      total de pacotes,                            tamanho da mensagem
        header = n.to_bytes(1, byteorder='big') + total_pacotes.to_bytes(1, byteorder='big') + data_size
        
        return (header + payload + EOP)

    def message_verifier(message_status):
        message_code = int.from_bytes(message_status[11:-4], "big")
        if message_code == 0:  # EOP ENCONTRADO
            print("---------")
            print("OK!")
            print("---------")
            return 0
            # return [1, message_status]

        elif message_code == 1:  # EOP NAO ENCONTRADO
            print("---------")
            print("EOP NAO ENCONTRADO")
            print("---------")
            return 1
            # return [1, 0]

        elif message_code == 2:  # EOP FORA DE LUGAR
            print("---------")
            print("EOP FORA DE LUGAR")
            print("---------")
            return 1
            # return [0, 1]
        elif message_code == 3:  # BYTES DIFERENTE DO HEAD
            print("---------")
            print("QUANTIDADE DE BYTES DIFERENTE DO HEAD!")
            print("---------")
            return 1
            # return [1, 1]

    with open("batata.png", "rb") as foto:
        txBuffer = foto.read()

    packages = file_spliter(txBuffer, 128)
    n_pkgs = len(packages)

    e = 1
    for pkg in packages:
        pkg_bs = byte_stuffing(pkg)
        data = add_header_eop(pkg_bs, e, n_pkgs)
        
        com.sendData(data)
        print("enviado pacote num: " + str(e))
        e += 1

        header_ms = com.getData(10)[0]
        
        if header_ms[0] == header_ms[1]:
            print(len(txBuffer))
            print("--------------------")
            print('ACABOU A TRANSMICAO')
            print("--------------------")
            com.disable()
            return 

        else:
            header_ms = int.from_bytes(header_ms[2:], "big")
            message_status = com.getData(header_ms)[0]
            check = message_verifier(message_status)
            if check == 1:
                com.disable()
                return  

        print(" ")
        

if __name__ == "__main__":
    main()
