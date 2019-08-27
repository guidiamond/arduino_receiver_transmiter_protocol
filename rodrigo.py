print("comecou")

from enlace import *
import time
from pacote import *


# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "/dev/ttyACM0"                  # Windows(variacao de)
print("abriu com")



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()
    time.sleep(0.1)
    com.fisica.flush()
   
    a=bytes([241])
    b=bytes([242])
    c=bytes([243])
    d=bytes([244])


    h=a+b+c+d
    start=time.time()
    dat=a+c+d+a+c+h+b+a+a+a+h+b+b+h

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    pack=pacote()

    dat_pack=pack.empacotar(dat)


    print(dat)
    print(dat_pack)
    com.sendData(dat_pack)
    # print


    # log
    # print ("Lido              {} bytes ".format(txlen))
    
    # print (rxBuffer2)

    encrypt=dat_pack[12:14]

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
