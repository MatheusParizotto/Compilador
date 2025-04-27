from lexico import tokenizer
from sintatico_e_semantico import AnalisadorSintatico

caminho = "mini-java-teste2.java"

with open(caminho, "r", encoding="utf-8") as arquivo:
    codigo_fonte = arquivo.read()

try:
    # Análise léxica
    tokens = tokenizer(codigo_fonte)
    print("Análise léxica concluída. Tokens gerados:")
    for token in tokens:
        print(token)

    # Análise sintática e semantica
    analisador = AnalisadorSintatico(tokens)
    analisador.analisar()

except SyntaxError as erro:
    print(f"Erro detectado: {erro}")