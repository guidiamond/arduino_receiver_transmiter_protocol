#!/usr/bin/env python3
# -- coding: utf-8 --
from tkinter import filedialog, Tk
import time
from enlace import *
print("comecou")


# Serial Com Port
serialName = "/dev/ttyACM0"  # Ubuntu (variacao de)


def main():
    # Inicializa enlace
    com = enlace(serialName)
    # Ativa comunicacao
    com.enable()

    # tk = Tk()
    # tk.withdraw
    # file_name = filedialog.askopenfilename()

    with open("batata.png", "rb") as foto:
        txBuffer = foto.read()

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

    def add_header_eop(bs_payload):
        # header
        payload_size = len(bs_payload).to_bytes(10, byteorder='big')
        # eop
        EOP = bytearray([0xF1, 0xF2, 0xF3, 0xF4])

        return (payload_size + bs_payload + EOP)

    def message_verifier(message_status):
        message_code = int.from_bytes(message_status[:2], "big")
        eop_position = int.from_bytes(message_status[2:], "big")
        if message_code == 0:  # EOP ENCONTRADO
            print("---------")
            print("EOP ENCONTRADO na posicao {0}" .format(eop_position))
            print("---------")

            return [1, message_status]

        elif message_code == 1:  # EOP NAO ENCONTRADO
            print("---------")
            print("EOP NAO ENCONTRADO (CORNO DETECTADO!)")
            print("---------")

            return [1, 0]
        elif message_code == 2:  # EOP FORA DE LUGAR
            print("---------")
            print("EOP FORA DE LUGAR")
            print("---------")

            return [0, 1]
        elif message_code == 3:  # BYTES DIFERENTE DO HEAD
            print("---------")
            print("QUANTIDADE DE BYTES DIFERENTE DO HEAD!")
            print("---------")

            return [1, 1]

    bs_payload = byte_stuffing(txBuffer)

    data = add_header_eop(bs_payload)
    com.sendData(data)
    message_status_head = com.getData(10)[0]

    message_status = com.getData(message_status_head)[0]

    message_verifier(message_status)

    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


if __name__ == "__main__":
    main()
