import socket
import struct

FORMATO = "!BBHHH"

MAGIC_NUMBER   = "NM"
COMANDO_INICIO = "NM Juta"
COMANDO_FIM    = "NM Afta"

#Colocar quando eu criar os containers
ORIGEM = "10.0.1.2"

capacidade_por_pacote = 28 // 4

mensagens_recuperadas = []
salvando = False


with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as s:
    s.bind((ORIGEM, 0))

    while True:
        dados, endereco = s.recvfrom(1024)

        tipo, codigo, checksum, _id, seq = struct.unpack(FORMATO, dados[20:28])
        print(tipo, codigo, checksum, _id, seq)

        pacote = dados[28:]

        mensagem_oculta = bytearray(pacote)
        frase_recuperada = bytearray()

        for indice in range(capacidade_por_pacote):
            inicio = indice * 4
            caracter_recuperado = 0

            for word in range(4):
                bits = mensagem_oculta[inicio + word] & 0b11
                caracter_recuperado |= bits << (word * 2)

            frase_recuperada.append(caracter_recuperado)

        frase_str = frase_recuperada.decode("utf-8", errors="ignore")

        if not frase_str:
            continue

        if frase_str == COMANDO_INICIO:
            salvando = True
            continue

        if frase_str == COMANDO_FIM:
            salvando = False
            break

        if salvando and frase_str.startswith(MAGIC_NUMBER):
            conteudo = frase_str[len(MAGIC_NUMBER):].lstrip()
            mensagens_recuperadas.append(conteudo)

print("Mensagens recuperadas: ", mensagens_recuperadas)