caminho_arquivo = "codigo-objeto.txt"

D = []  # Pilha de dados
s = -1  # Topo da pilha
C = []  # Lista de instruções
i = 0   # Contador de instruções

def executar_comando(comando):
    global s, i

    partes = comando.split()
    instrucao = partes[0]

    if instrucao == "INPP":
        s = -1
        D.clear()
    elif instrucao == "ALME":
        m = int(partes[1])
        for _ in range(m):
            D.append(0)
        s += m
    elif instrucao == "CRCT":
        k = int(partes[1])
        s += 1
        D.append(k)
    elif instrucao == "CRVL":
        n = int(partes[1])
        s += 1
        D.append(D[n])
    elif instrucao == "ARMZ":
        n = int(partes[1])
        D[n] = D[s]
        D.pop()
        s -= 1
    elif instrucao == "SOMA":
        D[s-1] = D[s-1] + D[s]
        D.pop()
        s -= 1
    elif instrucao == "SUBT":
        D[s-1] = D[s-1] - D[s]
        D.pop()
        s -= 1
    elif instrucao == "MULT":
        D[s-1] = D[s-1] * D[s]
        D.pop()
        s -= 1
    elif instrucao == "DIVI":
        if D[s] == 0:
            print("Erro: Divisão por zero!")
            exit()
        D[s-1] = D[s-1] / D[s]
        D.pop()
        s -= 1
    elif instrucao == "CPME":
        D[s-1] = 1 if D[s-1] < D[s] else 0
        D.pop()
        s -= 1
    elif instrucao == "CPMA":
        D[s-1] = 1 if D[s-1] > D[s] else 0
        D.pop()
        s -= 1
    elif instrucao == "CPIG":
        D[s-1] = 1 if D[s-1] == D[s] else 0
        D.pop()
        s -= 1
    elif instrucao == "CDES":
        D[s-1] = 1 if D[s-1] != D[s] else 0
        D.pop()
        s -= 1
    elif instrucao == "CMEG":
        D[s-1] = 1 if D[s-1] >= D[s] else 0
        D.pop()
        s -= 1
    elif instrucao == "CMEI":
        D[s-1] = 1 if D[s-1] <= D[s] else 0
        D.pop()
        s -= 1
    elif instrucao == "DSVF":
        p = int(partes[1])
        if D[s] == 0:
            i = p - 1
        D.pop()
        s -= 1
    elif instrucao == "DSVI":
        i = int(partes[1]) - 1
    elif instrucao == "LEIT":
        valor = int(input("Digite um valor: "))
        s += 1
        D.append(valor)
    elif instrucao == "IMPR":
        print(D[s])
        D.pop()
        s -= 1
    elif instrucao == "PARA":
        print("Programa finalizado.")
        exit()
    else:
        print(f"Erro: Instrução desconhecida -> {instrucao}")
        exit()

# Lendo o arquivo de comandos
with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
    C = arquivo.read().splitlines()

# Interpretando as instruções
while i < len(C):
    executar_comando(C[i])
    i += 1