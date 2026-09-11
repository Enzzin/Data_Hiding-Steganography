import socket
import struct
import os

FORMATO = "!BBHHH"

#Definindo as variaveis globais

MAGIC_NIBBLE = 0x0B #Numero magico para bytes de controle

# Bit 7: pacote é de DADOS ou de CONTROLE
CTX_DATA = 0  # Pacote de dados 
CTX_CTRL = 1  # Pacote de controle

# Bit 6: comando de stat ou stop
CMD_START = 0 # comando inicio
CMD_END = 1 # comando fim

# Bit 5: nibble
PART_HIGH = 0 #Nibble alto
PART_LOW = 1 #Nibble baixo

# Bit 5: Controle
SUB_TAMANHO = 0 # Tamanho do arquivo
SUB_EXTENSAO = 0 # Extensão do arquivo

#Colocar quando eu criar os containers
ORIGEM  = "127.0.0.1"
DESTINO = "127.0.0.1"


mensagem = (
    b"\b\t\n\v\f\r\016\017\020\021\022\023\024\025\026\027\030\031\032\033\034\035\036\037 !\"#$%&'()*+,-./01234567"
)
#Evitar Congestinamento (Menu para selecionar)
PAUSA_ENTRE_PACOTES = 0.005

#Montar pacotes de dados
def monta_byte_dados():
    byte_montado = 0
    return byte_montado

# Motar pacotes de controle
def monta_byte_controle():
    byte_montado = 0
    return byte_montado

def cria_icmp(payload: bytearray, sequence: int) -> bytearray:
    tipo = 8 
    codigo = 0
    checksum = 0

    identifier = os.getpid() % 65535

    cabecalho = struct.pack(FORMATO, tipo, codigo, checksum, identifier, sequence)

    pacote = cabecalho + payload
    tamanho_pacote = len(pacote)
    n = 2

    if tamanho_pacote % 2:
        pacote += b"\x00"

    for i in range(0, tamanho_pacote, n):
        palavra = pacote[i:i + n]

        checksum += int.from_bytes(palavra, byteorder="big")

    while checksum >> 16:
        checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = (~checksum) & 0xFFFF

    cabecalho = struct.pack(FORMATO, tipo, codigo, checksum, identifier, sequence)
    pacote = cabecalho + payload
    return pacote

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as s:
    s.bind((ORIGEM, 0))

    for sequence, payload_oculto in enumerate(pacotes_enviados, start=1):
        print("Payload alterado (repr):", repr(payload_oculto))
        print("Payload original (hex):", mensagem.hex())
        pacote = cria_icmp(bytearray(payload_oculto), sequence)
        s.sendto(pacote, (DESTINO, 0))