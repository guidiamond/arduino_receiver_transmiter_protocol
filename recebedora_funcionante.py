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
    # if header[1] == len(payload):
    #         return 0

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

    def add_header_eop(bs_payload):
        # header
        payload_size = len(bs_payload).to_bytes(10, byteorder='big')
        # eop
        EOP = bytearray([0xF1, 0xF2, 0xF3, 0xF4])

        return (payload_size + bs_payload + EOP)
    
    image = bytearray()
    while True:
        header = com.getData(10)[0]
        if header != None and header != '':
            payload_size = int.from_bytes(header, "big")
            bs_payload_with_eop = com.getData(payload_size + 4)[0]
            bs_payload = bs_payload_with_eop[:-4]
            message_status = message_analyzer(bs_payload_with_eop, payload_size)
            payload = undo_byte_stuffing(bs_payload)
            payload = payload[:-4]

            bs_payload_send = byte_stuffing(message_status)

            data_send = add_header_eop(bs_payload_send)

            com.sendData(data_send)
            image += (payload)
            print(len(image))
            open("toad.png", 'wb').write(image)

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada Garai")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modb'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13\x0f\x10\x10\x10\xff\xdb\x00C\x01\x03\x03\x03\x04\x03\x04\x08\x04\x04\x08\x10\x0b\t\x0b\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\xff\xc0\x00\x11\x08\x00\x80\x00\x80\x03\x01"\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x1d\x00\x01\x00\x02\x02\x03\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\t\x06\x07\x02\x03\n\x04\x01\xff\xc4\x00A\x10\x00\x00\x05\x02\x04\x03\x03\x07\t\x06\x07\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x11\x12\t!a\x13"1\x148AQu\x92\xb4\x15\x16\x172Rs\x81\x91\xb3$36BDq7Ubdrt\xa1\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?\x00\xb3\xd0\x00\x00\x00\x00\x11\xc77\x99\xdd\xc3\xfc\xa5\xc5\xa5\xd2\xeat9\xf7=\xdb_B\x9d\xa6P\xa0\xac\x9b5\xb6J\xdb\xda\xba\xe9\x91\xf6h5\xf7KD\xa9J=tI\x91\x19\x94y\x8bY\xe2\xcf\x98\xc7\x95T\xa0\xc4\xb70J\xdb\x94\x926\x1b\x9e\xd3h\x90\xa6\xcf\xed\x13\x8d\xbf(\x97\xa1\xf8\xech\x8f\xd0E\xccD.)8\x87.\xe1\xce\x8dq4\xca\x83\xcd\xaa\xcd\x85M\xa4\xc3\x90\xcb\x86\x85\xb4\xe2\x1a)*4(\xb9\xa5IzB\xf9\x9724\x8e8U\xc5K6xk\x19\xaauZ\xe2\xa5_\x10ZI!\r\xdcp\xcd\xd7\x92\x92\xff\x00p\xca\x9buj\xea\xe2\x96\x02d\xa7\x86\xcec\xefuyv0g\xb2\xf1\x97!_\xd2\xc0)n\xb2\x8d|v\x9b\x92P\x92.\x84\xd1\x0eG\xc1\xe6\xc7\xa9\x7f\x14f\x1b\x10j\x9a\xfdo\xdc\xa7_\x7fx\xd7\xb6\xb7\x1be\x13$\xd5\xed\x97\xf2S\xa4\\\xdf\xa5W\xf6\xa5G\xf7N2f^\xf9\x8c\xde\x9f\xc6\xab\x05\x9c\xd3\xe5\\!\xbd\xa3\xfa\xfc\x9d\xd8\x8fi\xef8\x80\x1fYpy\xb1\xe9\xbf\xc2\xf9\x86\xc4\x1a^\x9fW\xf7*\xd3\xdc\xd8?\x0f\x86\xcec\xac\x85yv\x10g\xb2\xf1\x86\xfa\x7f\xa6\x9eR\x9aezxn6\xe4\xad&]\r\xb3\x1f-C\x8dV\x0b7\xaf\xc9XC{H\xf5yC\xb1\x19\xd7\xddqc\x07\xba\xb8\xda\xac\xd96\xac\x8c\xbf\xa5\x0e\x99r~\xab^\xdc\x92?\xbai\x923\xf7\xc8\x06x\xf5K\x8bF^\x1fMJ\xb3\x1e\xd9\xc6\xfbv2L\xdff\x0bm\xaaI6_d\x90\xdb\x12T\xe6\x9e\xa4<]\x0cH<\xa4gf\xc3\xcds5z4+~\xa3j\xde6\xeaIuj\x05@\xf7\xad\xb4n\xd8n6\xe1\x12w\xa4\x97\xdcV\xe4\xa1IV\x9a\xa4\xb5#:\xb4\xc5\x9e)y\xb3\xc4\xf8\xae\xd3)\xd756\xc8\xa7\xbc\x93B\xda\xb6\xa2\x1b\x0f-\'\xeb\x90\xea\x9cy\'\xd5\xb5 vp\xb2\xbf\xdf\xb63\x9b@bl\xc7\x0c\xae\xf8\x15\x1a<\x97\\Y\x99\xadKh\xe4\'q\x9f35;\x1d\xb2\xfe\xe6@/L\x00\x00\x00\x00\x00\x00\x00\x00\x06\xb9\xcc}\xef\xf4o\x808\x87|\xa1\xee\xc9\xea=\xb5P\x91\x19Z\xe9\xfbG`\xa2d\xbf\x17\r\x05\xf8\x80\xf3\xdd\x8f\x17\xbf\xd2V6_\x97\xf2^\xed\x1a\xaf\xdcU\t\xec\x1e\xba\x912\xb7\xd6m$\xba\x126\x91t!\x82\x00\x00\x00\x00\x00\x00\x00\x0c\xeb\x02/\x7f\xa3\\k\xb1/\xe3{\xb3n\x81qS\xe7\xbez\xe8F\xcbo\xa0\xdcI\xf44n#\xe8c\x05\x00\x1e\xa4\xbc@k\x8c\xb7^\xff\x00I\x18\x01\x87w\xca\xde\xed_\xac[T\xf7\xe4\xab]\x7fi\xec\x12\x97\x8b^\x8e\x12\xcb\xf0\x1b\x1c\x00\x00\x00\x00\x00\x00C\x8e,w\xbf\xcd,\x9fU\xa8\xed\xbd\xb1\xdb\xb6\xb3N\xa3\'C\xef\x1aI\xc3\x94\xbd:\x1ab\x99\x1fC\xd3\xd2&8\xabn6W\xbf\xf8a\x86\xec=\xfea\\\x96\xde\xbfv\xcb\x07\xf1\x00*\xd8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xe4\xf0\x9a\xbd\xfevd\xfe\x95Eq\xed\xee\xda5\x9a\x8d\x19Z\x9fx\x92\xa7\nR?\r\xb2\x88\x8b\xfe:z\x04\xc9\x15i\xc16\xf7\xd1\xccO\xc3w\xde\xf1*}r#z\xfa\xbbF_?\xfd\x8e-,\x00\x00\x00\x00\x00\x00Q\xaf\x16K\xdf\xe7npj\xd4d=\xbd\xabJ\x8dN\xa3\'C\xee\x92\x8d\xb3\x94\xbd:\x92\xa5\x19\x1fR\xd3\xd0/(S7\x14\x8c\xa5b-\xab\x8c\xd5\xdc}\xb7(\x13*\xf6e\xd4m\xcb\x99&\x1bKx\xe9R\x90\xca\x10\xe9H"#\xd8\xda\xcd\x1b\xd2\xb3\xee\xf7\x8d<\x8c\x8bP\x80\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00&7\t\xeb\xdf\xe6\x96p\xa8\xf4\x85\xbd\xd9\xb3v\xd1\xea4U\xea|\x8c\xc9\xb2\x94\x82>\xa6\xa8\xa9"\xea}E\xe6\nf\xe1o\x94\xacE\xba\xb1\x9a\x85\x8f\xb7%\xbf2\x93fZ\x86\xe4\xc8rf4\xb6N\xab)l\xad\r\x14r2-\xed\xa0\xd7\xbdK.\xeft\x93\xcc\xcc\xf4\xb9\x90\x00\x00\x00\x00\x00\x00RR\xa4\x9aTDde\xa1\x91\xf8\x19\x00\x00\xd75L\xb7e\xe2\xb7<\xaa\x95\x9c\x07\xc3\xc9\xd3\x08\xcd]\xbc\x9bb\x13\x8e\x19\xfa\xcdJl\xcc\xc6\x1d\x98\xac\x98\xe0\xaec0\xfa-\x8d[\xb7\xe3\xd0\x1d\xa3\x91\x9d\x0e\xa5F\x8a\xd3\x0fS\x0c\xfcR\x84\x92v\xa9\xa5h[\x9b2\xd0\xf9\x19mQ\x12\x8b{\x80\n:\xc6\x1e\x14Y\xa3\xc3\xa9\xf2\x9d\xb2\xa9\x10q\x02\x8a\xd1\x9a\x9a\x97J\x90\xdb2M\x1e\x8d\xf1^Q,\x95\xfe\x96\xcd\xcf\xee#\x95g/X\xf9n)i\xaf\xe0\x95\xfbN\xec\xcc\xc9G&\xdc\x98\xd9r\xeam\xe8e\xd4zR\x1a\xc73X\xa9Y\xc1\x1c\x07\xbc\xb1Z\xde\xa7\xc2\x9dQ\xb6\xe0\x14\xb8\xf1\xe6\x92\xcd\x87\x15\xda!\x1a/a\xa5Zh\xa3\xf02\x01\xe7\xea\x8b\x97\xbcz\xb9\x1cm\xaa\x06\t\xdfu\x03t\xc8\x92q\xad\xd9n\'\x9fRoB.\xa7\xc8H\xfc\x1d\xe1E\x9a,F\x9e\xc3\x97\xb5*\x16\x1e\xd1W\xa2\x9c\x97V}\xb7\xe4\x9a==\x9cVTj\xdd\xd1\xc3l\xba\x8bt\xcb\x16+V\xb1\xc3\x01l\xecW\xb8\xa9\xd0\xa0\xd4n8*\x95"<"Y0\xda\x89\xd5\xa3DoR\x95\xa6\x88/\x131\xb4\x00@[c\'\x989\x96\xec\xc2e\xea\xc2\xb7h\x8dVWZ\x81x\xaa\xbfQ\xaa\xb0\x87\x9c\xab8\x881v\xf6\x8824%\xb4\xef^\xc6\xc8\xb4N\xe3\xfa\xca5(\xe5\xad3-\xf9x\xa2\xcf:\xad\x1f\x01\xf0\xf2\x0c\xc5\x19+\xca#\xdb\x10\x9bs_Y)-\x91\x90\xd7\x98\xcd\xe7\x91\x97\x0f\xfa7\xb7\xc1D\x12 \x01)JRII\x11\x11\x16\x84E\xe0D\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02>q\x02\xf36\xc5?c\'\xf5\xda\x12\x0cG\xce ^f\xd8\xa7\xecd\xfe\xbb@8p\xf9\xf34\xc2\xcfd9\xf1.\x89\x0c#\xcf\x0f\x9f3L,\xf6C\x9f\x12\xe8\x90\xc0*\x0b:\xf8\x85\x9c\xfavz\xe0\xb9eSnD=n\xc9CV\x04x4\xf3z3\xb1\xa42\xd2^4\xf76\xbb\xdb)&N\xef3\xdb\xa6\xd32$\x16\x96\xf1\x11rW\x11\x95\xcdi\rHSi7[B\xb7%\x0b\xd3\xbcD~\x92#\xd7\x98\xed\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\xf3\x88\x17\x99\xb6)\xfb\x19?\xae\xd0\x90b>q\x02\xf36\xc5?c\'\xf5\xda\x01\xc3\x87\xcf\x99\xa6\x16{!\xcf\x89tHa\x1ex|\xf9\x9aag\xb2\x1c\xf8\x97D\x86\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11\xef1\xf8\xe5\x99\x0c-\xa8\xa2\x1e\x0f\xe5Zv!\xd3\xd6\xc18\xaa\xbbU\xc6[J\x1c\xf4\xb7\xe4\x89J\x9eV\x9c\xbb\xdd\xd2?F\xa2\xbd\xb3\x1b\x9b\x0e#X\xa5Iv\xcew\x04\xef,9\xa5\xa8\xcc\xa5&\x83m\xd4\xd8\x93)\x07\xfc\x8b\x92\xb25l\xe8\xde\xc2Q\x19\x92\xb7\x17 \x17\x11&\\Hm\xf6\xb3%4\xc2>\xd3\x8b$\x97\xe6b3\xe7\xf6\xf7\xb3\x1f\xca.\'R\x98\xbb\xa8\xaeM\x91HJ\x1a\x8c\x89\xed\x1b\xae+\xb7l\xf4J\tZ\x99\xf2>DB\x8ekX{\x8b\xaeJrm\xc5c\xdd\xeb\x90\xb3\xd5\xc7\xa6\xd3%\x1a\xd4}T\xb4\xeac\x1d\x97D\xadS\xf5\xf2\xfaD\xd8\xdax\xf6\xd1\xd6\x8d?2\x01|\xbc?\xafk1\x8c\xa1\xe1\x95%\xfb\xba\x8a\xdc\xe8\xf4\xa5\xa1\xd8\xcb\x9e\xd1:\xda\xbc\xa1\xd3\xd1H5jG\xcc\xbcHI\xb8\xd2\xe2Lo\xb5\x87)\x97\xd1\xf6\x9bY(\xbf2\x1e_\xe2Q+U\r<\x82\x916N\xbe\x1d\x8cu\xaf_\xc8\x86EE\xc3\xdc]jSsm\xdb\x1e\xefD\x84\x1e\xad\xbd\n\x99(\x96\x93\xe8\xa4\'R\x01\xe9\x8c\x058\xe5\xcb6<F\xf0\xb6\x92\xd5\x9c\xd6\n^X\x8dKI\x91EEz\xdb\xa9\xbf&2\x0b\xf9Q%\x04J\xd9\xd1\xcd\xe4\x92"$\xed.B\xc2\xf2\xdf\x8eY\x90\xc5*\x82\xe2c\x0eU\xa7\xe1\xe4\x040n&\xae\xedq\x97\x12\xe3\x9e\x86\xfc\x91iK\xc9\xd7\x9f{\xbcE\xe9\xd0\x04\x83\x00\x00\x00\x00\x01\xff\xd9'


if __name__ == "__main__":
    main()
