class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def token_atual(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None
    
    def consumir(self, tipo_esperado):
        token = self.token_atual()
        if token and token[0] == tipo_esperado:
            self.posicao += 1
        else:
            raise SyntaxError(f"Erro Sintático: Esperado '{tipo_esperado}', encontrado '{token}'")

    def analisar(self):
        self.programa()
        print("Análise sintática concluída com sucesso!")

    def programa(self):
        self.consumir('PUBLIC')
        self.consumir('CLASS')
        self.consumir('ID')
        self.consumir('ABRE_CHAVE')
        self.consumir('PUBLIC')
        self.consumir('STATIC')
        self.consumir('VOID')
        self.consumir('MAIN')
        self.consumir('PARENTESE_ESQ')
        self.consumir('STRING')
        self.consumir('ABRE_COLCHETE')
        self.consumir('FECHA_COLCHETE')
        self.consumir('ID')
        self.consumir('PARENTESE_DIR')
        self.consumir('ABRE_CHAVE')
        self.comandos()
        self.consumir('FECHA_CHAVE')
        self.consumir('FECHA_CHAVE')

    def comandos(self):
        pass

    def comando_condicional(self):
        if self.token_atual[0] == 'IF':
            self.consome('IF')
            self.consome('PARENTESE_ESQ')
            self.condicao()
            self.consome('PARENTESE_DIR')
            self.consome('ABRE_CHAVE')
            self.comandos()
            self.consome('FECHA_CHAVE')
            self.parte_falsa()
        else:
            raise SyntaxError(f"Esperado 'if', mas encontrado: {self.token_atual}")
    
    def parte_falsa(self):
        if self.token_atual[0] == 'ELSE':
            self.consome('ELSE')
            self.consome('ABRE_CHAVE')
            self.comandos()
            self.consome('FECHA_CHAVE')
        # Se não tiver else é vazio, então não faz nada

    def condicao(self):
        self.expressao()
        if self.token_atual[0] in ['IGUAL', 'DIFERENTE', 'MAIOR_IGUAL', 'MENOR_IGUAL', 'MAIOR', 'MENOR']:
            self.consome(self.token_atual[0])
        else:
            raise SyntaxError(f"Operador relacional esperado, mas encontrado: {self.token_atual}")
        self.expressao()