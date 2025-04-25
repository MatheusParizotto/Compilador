class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.tabela_simbolos = {}        
        self.endereco_memoria = 0        
        self.codigo_objeto = []           
        self.rotulo = 0                   

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
        self.codigo_objeto.append("INPP")  

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

        self.codigo_objeto.append("PARA") 

        # Salva em arquivo
        with open("codigo-objeto.txt", "w") as arquivo:
            for instrucao in self.codigo_objeto:
                arquivo.write(instrucao + "\n")
        print("Código objeto gerado com sucesso em 'codigo-objeto.txt'")

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
        # Verificação manual de System.out.println
        if self.verificar('ID') and self.token_atual()[1] == 'System':
            # Checar se vem . out . println 
            self.consumir('ID')          
            self.consumir('PONTO')       
            self.consumir('ID')          
            self.consumir('PONTO')       
            self.consumir('ID')          
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
            var_nome = self.tokens[self.posicao - 2][1]

            if var_nome not in self.tabela_simbolos:
                raise Exception(f"Erro Semântico: Variável '{var_nome}' usada sem declaração.")

            self.exp_ident()

            endereco = self.tabela_simbolos[var_nome]
            self.codigo_objeto.append(f"ARMZ {endereco}")

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
            nome_var = self.token_atual()[1]
            if nome_var not in self.tabela_simbolos:
                raise Exception(f"Erro Semântico: Variável '{nome_var}' usada sem declaração.")
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
        if self.verificar('ID'):
            nome_var = self.token_atual()[1]
            
            if nome_var in self.tabela_simbolos:
                raise Exception(f"Erro Semântico: Variável '{nome_var}' já declarada.")

            self.tabela_simbolos[nome_var] = self.endereco_memoria
            self.codigo_objeto.append("ALME 1")  
            self.endereco_memoria += 1

            self.consumir('ID')
            self.mais_var()
        else:
            raise SyntaxError(f"Esperado identificador após tipo, encontrado: {self.token_atual()}")

    def mais_var(self):
        if self.verificar('VIRGULA'):
            self.consumir('VIRGULA')
            self.vars()  

    def mais_comandos(self):
        if self.verificar('PONTO_VIRGULA'):
            self.avancar()
            self.comandos()
