import socket
import struct
import os

FORMATO = "!BBHHH"

MAGIC_NUMBER   = "NM"
COMANDO_INICIO = "NM Juta"
COMANDO_FIM    = "NM Afta"

#Colocar quando eu criar os containers
ORIGEM  = "10.0.1.3"
DESTINO = "10.0.1.2"

mensagens_escondidas = [
    "Nada",
    "NM Juta",
    "NM oi",
    "oi sem",
    "NM Afta",
    "NM MACACO"
]

mensagem = (
    b"\b\t\n\v\f\r\016\017\020\021\022\023\024\025\026\027\030\031\032\033\034\035\036\037 !\"#$%&'()*+,-./01234567"
)

capacidade_por_pacote = len(mensagem) // 4

pacotes_enviados = []

for msg in mensagens_escondidas:
    frase_bytes = msg.encode("utf-8")

    if len(frase_bytes) > capacidade_por_pacote:
        print("Mensagem grande demais por pacote")
        continue

    mensagem_oculta = bytearray(mensagem)

    for indice, byte_frase in enumerate(frase_bytes):
        inicio = indice * 4
        for word in range(4):
            bits = byte_frase & 0b11
            mensagem_oculta[inicio + word] &= 0b11111100
            mensagem_oculta[inicio + word] |= bits
            byte_frase >>= 2

    pacotes_enviados.append(bytes(mensagem_oculta))

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