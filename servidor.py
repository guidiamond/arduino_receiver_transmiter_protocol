#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import filedialog, Tk
import time
from enlace import *
print("comecou")


# Serial Com Port
serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    # repare que o metodo construtor recebe um string (nome)
    com = enlace(serialName)
    # Ativa comunicacao
    com.enable()
    time.sleep(0.1)
    com.fisica.flush()

    def message_analyzer(message, header):
        EOP = bytearray([0xF1, 0xF2, 0xF3, 0xF4])
        eop_index = message.find(EOP)
        print("header size: {0} mensagem: {1}".format(header, len(message)))
        if eop_index == -1:
            message_code = 1
            eop_index = 0
            byte_output = message_code.to_bytes(
                2, byteorder='big') + eop_index.to_bytes(3, byteorder='big')
            return byte_output  # nao encontrado
        if (header == len(message)-len(EOP)):
            print(
                "eop_index: {0} len(message - 4): {1}".format(eop_index, len(message)-len(EOP)))

            if (eop_index == len(message)-len(EOP)):
                message_code = 0
                byte_output = message_code.to_bytes(
                    2, byteorder='big') + eop_index.to_bytes(3, byteorder='big')

                return byte_output  # encontrado na posicao
            else:
                message_code = 2
                byte_output = message_code.to_bytes(
                    2, byteorder='big') + eop_index.to_bytes(3, byteorder='big')

                return byte_output  # eop fora de lugar
        else:
            message_code = 3
            byte_output = message_code.to_bytes(
                2, byteorder='big') + eop_index.to_bytes(3, byteorder='big')
            return byte_output  # tamanho diferente

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
    
    image = bytearray()
    
    e = 1
    
    while True:
        header = com.getData(10)[0]
        num_pacotes = header[1]
        print(header)
        
        if header != None and header != '':

            pkg_size = int.from_bytes(header[2:], "big")
            data_bs = com.getData(pkg_size)[0]
            data = undo_byte_stuffing(data_bs)
            payload = data[:-4]
            
            print(len(payload))

            image += payload

            print(" ")

            message_status = message_analyzer(data, header)
            bs_payload_send = byte_stuffing(message_status)

            if header[0] == header[1]:
                print(" ")
                print("chegou no ultimo pacote")

                data_send = add_header_eop(bs_payload_send, e, num_pacotes)
                com.sendData(data_send)

                open("toad.png", "wb").write(image)
                
                print("-------------------------")
                print("Comunicação encerrada")
                print("-------------------------")
                com.disable()
                return

            else:
                data_send = add_header_eop(bs_payload_send, e, num_pacotes)
                com.sendData(data_send)
                e += 1

#so roda o main quando for executado do terminal ... se for chamado dentro de outro modb

if __name__ == "__main__":
    main()
