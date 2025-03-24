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
    """
    Função que recebe um código MiniJava e retorna uma lista de tokens.
    """
    tokens = []
    codigo_fonte = codigo_fonte.strip()  # Remove espaços extras no começo e fim

    while codigo_fonte:
        codigo_fonte = codigo_fonte.lstrip()  # Remove espaços no início

        token_encontrado = False
        for pattern, tipo in TOKEN_REGEX:
            regex = re.match(pattern, codigo_fonte)
            if regex:
                valor = regex.group(0)
                if tipo != 'COMENTARIO':  # Ignorar comentários
                    tokens.append((tipo, valor))
                codigo_fonte = codigo_fonte[len(valor):]  # Remove o token do código-fonte
                token_encontrado = True
                break

        if not token_encontrado:
            if codigo_fonte.strip():  # Apenas lança erro se houver caracteres não reconhecidos
                raise SyntaxError(f"Erro Léxico: Token inválido encontrado: {codigo_fonte[:10]}")
            else:
                break  # Evita erro de lista vazia e encerra a análise

    return tokens

# Testando o léxico com o código MiniJava fornecido
with open("mini-java.java", "r", encoding="utf-8") as f:
    codigo = f.read().strip()  # Remove espaços e quebras de linha extras

tokens = tokenizer(codigo)
for token in tokens:
    print(token)