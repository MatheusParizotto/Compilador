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

    def comandos(self):
        token = self.token_atual()
        if token is None or token[0] == 'FECHA_CHAVE':
            return  # Comando vazio 

        if token[0] == 'IF' or token[0] == 'WHILE':
            self.comando_condicional()
            self.comandos()
        elif token[0] == 'ID' or token[0] == 'SYSTEM':
            self.comando()
            self.consumir('PONTO_VIRGULA')
            self.comandos()
        elif token[0] == 'TIPO':  # Caso precise tratar declarações
            self.dc()
            self.comandos()
        else:
            raise SyntaxError(f"Comando inválido iniciado por: {token}")

    def comando(self):
        token = self.token_atual()
        if token[0] == 'SYSTEM':
            self.consumir('SYSTEM')
            self.consumir('PONTO')
            self.consumir('OUT')
            self.consumir('PONTO')
            self.consumir('PRINTLN')
            self.consumir('PARENTESE_ESQ')
            self.expressao()
            self.consumir('PARENTESE_DIR')
        elif token[0] == 'ID':
            self.consumir('ID')
            self.resto_ident()
        else:
            raise SyntaxError(f"Comando inesperado: {token}")
    
    def resto_ident(self):
        token = self.token_atual()
        if token[0] == 'IGUAL':
            self.consumir('IGUAL')
            self.exp_ident()
        elif token[0] == 'PARENTESE_ESQ':
            self.consumir('PARENTESE_ESQ')
            self.lista_arg()
            self.consumir('PARENTESE_DIR')
        else:
            raise SyntaxError(f"Esperado '=' ou '(', encontrado: {token}")
    
    def exp_ident(self):
        token = self.token_atual()
        if token[0] == 'LERDOUBLE':
            self.consumir('LERDOUBLE')
            self.consumir('PARENTESE_ESQ')
            self.consumir('PARENTESE_DIR')
        else:
            self.expressao()

    
    def lista_arg(self):
        token = self.token_atual()
        if token and token[0] == 'ID':
            self.argumentos()
        # Caso seja vazio não vai fazer nada

    def argumentos(self):
        self.consumir('ID')
        self.mais_ident()

    def mais_ident(self):
        token = self.token_atual()
        if token and token[0] == 'VIRGULA':
            self.consumir('VIRGULA')
            self.argumentos()
        # Se for vazio não faz nada
    
    def expressao(self):
        self.termo()
        self.outros_termos()
    
    def termo(self):
        if self.verificar('SUB'):
            self.avancar()
        self.fator()
        self.mais_fatores()

    def fator(self):
        if self.verificar('ID'):
            self.avancar()
        elif self.verificar('NUMERO_REAL'):
            self.avancar()
        elif self.verificar('PARENTESE_ESQ'):
            self.avancar()
            self.expressao()
            self.consumir('PARENTESE_DIR', "Esperado ')' ao final da expressão.")
        else:
            raise SyntaxError(f"Esperado identificador, número ou '(', mas encontrado: {self.token_atual()}")