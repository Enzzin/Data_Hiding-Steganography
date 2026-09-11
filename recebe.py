import socket
import struct

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
ORIGEM = "127.0.0.1"

MAPA_EXTENSAO = {
    0x0: "bin", 0x1: "jpg", "png": 0x2, #Colocar mais depois
}

ORIGEM = "127.0.0.1"

def decodifica_byte(byte_estego: int) -> dict:
    #Tira cada bit usando deslocamento >> e usa & 1 para pegar somente o bit certo em caso de erro de comunicação
    ctx = (byte_estego >> 7) & 1
    seq_cmd = (byte_estego >> 6) & 1
    part_sub = (byte_estego >> 5) & 1
    parity = (byte_estego >> 4) & 1
    nibble = byte_estego & 0x0F

    return {
        "ctx": ctx,
        "seq_cmd": seq_cmd,
        "part_sub": part_sub,
        "parity": parity,
        "nibble": nibble,
    }

def valida_paridade(nibble: int, parity_bit: int) -> bool:
    paridade_esperada = bin(nibble).count("1") % 2
    if paridade_esperada != parity_bit:
        return 0
    else:
        return 1
