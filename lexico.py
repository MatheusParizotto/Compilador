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
    (r'system.out.println', 'PRINTLN'),
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
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'ID'),
    (r'//.*', 'COMENTARIO')
]

def tokenizer(codigo_fonte):
    """
    Função que recebe um código MiniJava e retorna uma lista de tokens.
    """
    tokens = []
    while codigo_fonte:
        codigo_fonte = codigo_fonte.lstrip()  # Remove espaços e quebras de linha no início

        token_encontrado = None
        for pattern, tipo in TOKEN_REGEX:
            regex = re.match(pattern, codigo_fonte)
            if regex:
                valor = regex.group(0)
                if tipo != 'COMENTARIO':  # Ignorar comentários
                    tokens.append((tipo, valor))
                codigo_fonte = codigo_fonte[len(valor):]  # Remove o token do código fonte
                token_encontrado = True
                break

        if not token_encontrado:
            raise SyntaxError(f"Erro Léxico: Token inválido encontrado: {codigo_fonte.split()[0]}")

    return tokens

# Testando o léxico com o código MiniJava fornecido
with open("mini-java-examplo.java", "r", encoding="utf-8") as f:
    codigo = f.read()

tokens = tokenizer(codigo)
for token in tokens:
    print(token)
