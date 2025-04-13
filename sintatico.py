class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0

    def token_atual(self):
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None

    def consumir(self, tipo_esperado, mensagem=None):
        token = self.token_atual()
        if token and token[0] == tipo_esperado:
            self.posicao += 1
        else:
            erro = mensagem if mensagem else f"Erro Sintático: Esperado '{tipo_esperado}', encontrado '{token}'"
            raise SyntaxError(erro)

    def verificar(self, tipo):
        token = self.token_atual()
        return token and token[0] == tipo

    def avancar(self):
        self.posicao += 1

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
        token = self.token_atual()
        if token is None or token[0] == 'FECHA_CHAVE':
            return  # Vazio 

        if token[0] == 'IF' or token[0] == 'WHILE':
            self.comando_condicional()
            self.comandos()
        elif token[0] == 'SYSTEM' or token[0] == 'ID':
            self.comando()
            self.consumir('PONTO_VIRGULA')
            self.comandos()
        elif token[0] == 'DOUBLE':
            self.declaracao_variaveis()
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

    def comando_condicional(self):
        if self.verificar('IF'):
            self.consumir('IF')
            self.consumir('PARENTESE_ESQ')
            self.condicao()
            self.consumir('PARENTESE_DIR')
            self.consumir('ABRE_CHAVE')
            self.comandos()
            self.consumir('FECHA_CHAVE')
            self.parte_falsa()
        elif self.verificar('WHILE'):
            self.consumir('WHILE')
            self.consumir('PARENTESE_ESQ')
            self.condicao()
            self.consumir('PARENTESE_DIR')
            self.consumir('ABRE_CHAVE')
            self.comandos()
            self.consumir('FECHA_CHAVE')
        else:
            raise SyntaxError(f"Esperado 'if' ou 'while', mas encontrado: {self.token_atual()}")

    def parte_falsa(self):
        if self.verificar('ELSE'):
            self.consumir('ELSE')
            self.consumir('ABRE_CHAVE')
            self.comandos()
            self.consumir('FECHA_CHAVE')

    def condicao(self):
        self.expressao()
        if self.verificar('IGUAL') or self.verificar('DIFERENTE') or self.verificar('MAIOR_IGUAL') or \
           self.verificar('MENOR_IGUAL') or self.verificar('MAIOR') or self.verificar('MENOR'):
            self.avancar()
        else:
            raise SyntaxError(f"Esperado operador relacional, encontrado: {self.token_atual()}")
        self.expressao()

    def resto_ident(self):
        token = self.token_atual()
        if token[0] == 'ATRIB': 
            self.consumir('ATRIB')
            self.exp_ident()
        elif token[0] == 'PARENTESE_ESQ':
            self.consumir('PARENTESE_ESQ')
            self.lista_arg()
            self.consumir('PARENTESE_DIR')
        else:
            raise SyntaxError(f"Esperado '=' ou '(', encontrado: {token}")

    def exp_ident(self):
        if self.verificar('LERDOUBLE'):
            self.consumir('LERDOUBLE')
            self.consumir('PARENTESE_ESQ')
            self.consumir('PARENTESE_DIR')
        else:
            self.expressao()

    def lista_arg(self):
        if self.verificar('ID'):
            self.argumentos()

    def argumentos(self):
        self.consumir('ID')
        self.mais_ident()

    def mais_ident(self):
        if self.verificar('VIRGULA'):
            self.consumir('VIRGULA')
            self.argumentos()

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
        elif self.verificar('NUMERO_REAL') or self.verificar('NUMERO_INTEIRO'):
            self.avancar()
        elif self.verificar('PARENTESE_ESQ'):
            self.avancar()
            self.expressao()
            self.consumir('PARENTESE_DIR', "Esperado ')' ao final da expressão.")
        else:
            raise SyntaxError(f"Esperado ID, número ou '(', mas encontrado: {self.token_atual()}")

    def outros_termos(self):
        while self.verificar('SOMA') or self.verificar('SUB'):
            self.avancar()
            self.termo()

    def mais_fatores(self):
        while self.verificar('MULT') or self.verificar('DIV'):
            self.avancar()
            self.fator()

    def declaracao_variaveis(self):
        self.var()
        self.mais_comandos()

    def var(self):
        self.tipo()
        self.vars()

    def tipo(self):
        if self.verificar('DOUBLE'):
            self.avancar()
        else:
            raise SyntaxError(f"Esperado tipo 'double', mas encontrado: {self.token_atual()}")

    def vars(self):
        self.consumir('ID')
        self.mais_var()

    def mais_var(self):
        if self.verificar('VIRGULA'):
            self.avancar()
            self.vars()

    def mais_comandos(self):
        if self.verificar('PONTO_VIRGULA'):
            self.avancar()
            self.comandos()
