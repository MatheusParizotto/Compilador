import re

# Definição dos tokens e padrões
TOKEN_REGEX = [
    (r'public', 'PUBLIC'),
    (r'class', 'CLASS'),
    (r'static', 'STATIC'),
    (r'void', 'VOID'),
    (r'main', 'MAIN'),
    (r'String', 'STRING'),
    (r'double', 'DOUBLE'),
    (r'if', 'IF'),
    (r'else', 'ELSE'),
    (r'while', 'WHILE'),
    (r'system\.out\.println', 'PRINTLN'),
    (r'lerDouble', 'LERDOUBLE'),
    (r'==', 'IGUAL'),
    (r'!=', 'DIFERENTE'),
    (r'>=', 'MAIOR_IGUAL'),
    (r'<=', 'MENOR_IGUAL'),
    (r'>', 'MAIOR'),
    (r'<', 'MENOR'),
    (r'=', 'ATRIB'),
    (r'\+', 'SOMA'),
    (r'-', 'SUB'),
    (r'\*', 'MULT'),
    (r'/', 'DIV'),
    (r'\(', 'PARENTESE_ESQ'),
    (r'\)', 'PARENTESE_DIR'),
    (r'\{', 'ABRE_CHAVE'),
    (r'\}', 'FECHA_CHAVE'),
    (r'\[', 'ABRE_COLCHETE'),
    (r'\]', 'FECHA_COLCHETE'),
    (r';', 'PONTO_VIRGULA'),
    (r',', 'VIRGULA'),
    (r'\.', 'PONTO'),
    (r'[0-9]+\.[0-9]+', 'NUMERO_REAL'),
    (r'[0-9]+', 'NUMERO_INTEIRO'),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),
    (r'//.*', 'COMENTARIO')
]

def tokenizer(codigo_fonte):
   
    # Função que recebe um código MiniJava e retorna uma lista de tokens.
    
    tokens = []
    # Remove espaços extras no começo e fim
    codigo_fonte = codigo_fonte.strip()  
    # Divide em linhas para melhor depuração
    linhas = codigo_fonte.split("\n")  

    while codigo_fonte:
        # Remove espaços no início
        codigo_fonte = codigo_fonte.lstrip()  

        token_encontrado = False
        for pattern, tipo in TOKEN_REGEX:
            regex = re.match(pattern, codigo_fonte)
            if regex:
                valor = regex.group(0)

                # Erro para números mal formatados 
                if tipo == 'NUMERO_REAL' and valor.count('.') > 1:
                    raise SyntaxError(f"Erro Léxico: Número mal formatado '{valor}'")

                # Ignora os comentários
                if tipo != 'COMENTARIO': 
                    tokens.append((tipo, valor))

                # Remove o token do código-fonte
                codigo_fonte = codigo_fonte[len(valor):]  
                token_encontrado = True
                break

        if not token_encontrado:
            # Mostrar a linha do erro
            for linha in linhas:
                if codigo_fonte.strip() and codigo_fonte.strip() in linha:
                    linha_do_erro = linha.strip()
                    break
            else:
                linha_do_erro = f"(Trecho inválido: {codigo_fonte[:15]})"

            raise SyntaxError(f"Erro Léxico: Token inválido encontrado na linha -> {linha_do_erro}")

    return tokens

# Testando o léxico com o mini java
with open("mini-java.java", "r", encoding="utf-8") as f:
    # Remove espaços e quebras de linha extras
    codigo = f.read().strip()  

tokens = tokenizer(codigo)
for token in tokens:
    print(token)