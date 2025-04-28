class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicao = 0
        self.tabela_simbolos = {}        # Guarda variáveis declaradas
        self.endereco_memoria = 0         # Endereço atual para armazenar variáveis
        self.codigo_objeto = []           # Lista de instruções geradas

    def token_atual(self):
        # Retorna o token atual
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None

    def consumir(self, tipo_esperado, mensagem=None):
        # Consome o token se for do tipo esperado
        token = self.token_atual()
        if token and token[0] == tipo_esperado:
            self.posicao += 1
        else:
            erro = mensagem if mensagem else f"Erro Sintático: Esperado '{tipo_esperado}', encontrado '{token}'"
            raise SyntaxError(erro)

    def verificar(self, tipo):
        # Verifica se o token atual é do tipo indicado
        token = self.token_atual()
        return token and token[0] == tipo

    def avancar(self):
        # Avança um token
        self.posicao += 1

    def analisar(self):
        # Inicia a análise sintática
        self.programa()
        print("Análise sintática concluída com sucesso!")

    def programa(self):
        # Reconhece a estrutura principal do programa
        self.codigo_objeto.append("INPP")  # Início do programa

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

        self.codigo_objeto.append("PARA")  # Fim do programa

        # Salva o código objeto
        with open("codigo-objeto.txt", "w") as arquivo:
            for instrucao in self.codigo_objeto:
                arquivo.write(instrucao + "\n")
        print("Código objeto gerado com sucesso em 'codigo-objeto.txt'")

    def comandos(self):
        # Analisa vários comandos
        token = self.token_atual()
        if token is None or token[0] == 'FECHA_CHAVE':
            return  # Não há mais comandos

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
        # Trata comando de atribuição ou impressão
        token = self.token_atual()

        if token[0] == 'ID' and token[1] == 'System':
            # Trata impressão System.out.println()
            self.consumir('ID')  
            self.consumir('PONTO')
            if self.token_atual()[1] != 'out':
                raise SyntaxError(f"Esperado 'out' após 'System.', encontrado: {self.token_atual()}")
            self.consumir('ID')  
            self.consumir('PONTO')
            if self.token_atual()[1] != 'println':
                raise SyntaxError(f"Esperado 'println' após 'System.out.', encontrado: {self.token_atual()}")
            self.consumir('ID')  
            self.consumir('PARENTESE_ESQ')

            var_token = self.token_atual()
            if var_token[0] == 'ID':
                var_nome = var_token[1]
                if var_nome not in self.tabela_simbolos:
                    raise Exception(f"Erro Semântico: Variável '{var_nome}' usada sem declaração.")
                endereco = self.tabela_simbolos[var_nome]
                self.consumir('ID')
                self.codigo_objeto.append(f"CRVL {endereco}")
                self.codigo_objeto.append("IMPR")
            else:
                raise SyntaxError(f"Esperado uma variável para imprimir, encontrado: {var_token}")

            self.consumir('PARENTESE_DIR')

        elif token[0] == 'ID':
            # Trata atribuição
            nome_var = token[1]
            if nome_var not in self.tabela_simbolos:
                raise Exception(f"Erro Semântico: Variável '{nome_var}' usada sem declaração.")
            self.consumir('ID')
            self.resto_ident()

        else:
            raise SyntaxError(f"Comando inválido iniciado por: {token}")

    def comando_condicional(self):
        # Trata IF e WHILE
        if self.verificar('IF'):
            self.avancar()
            self.consumir('PARENTESE_ESQ')
            self.condicao()
            self.consumir('PARENTESE_DIR')
            self.consumir('ABRE_CHAVE')

            endereco_dsvf = len(self.codigo_objeto)
            self.codigo_objeto.append('DSVF ??')  # Reserva espaço para salto

            self.comandos()
            self.consumir('FECHA_CHAVE')

            if self.verificar('ELSE'):
                endereco_dsvf_final = len(self.codigo_objeto)
                self.codigo_objeto.append('DSVI ??')  # Salta após o ELSE

                self.codigo_objeto[endereco_dsvf] = f'DSVF {len(self.codigo_objeto)}'

                self.avancar()
                self.consumir('ABRE_CHAVE')
                self.comandos()
                self.consumir('FECHA_CHAVE')

                self.codigo_objeto[endereco_dsvf_final] = f'DSVI {len(self.codigo_objeto)}'
            else:
                self.codigo_objeto[endereco_dsvf] = f'DSVF {len(self.codigo_objeto)}'

        elif self.verificar('WHILE'):
            self.avancar()
            self.consumir('PARENTESE_ESQ')

            inicio_while = len(self.codigo_objeto)

            self.condicao()

            self.consumir('PARENTESE_DIR')
            self.consumir('ABRE_CHAVE')

            endereco_dsvf = len(self.codigo_objeto)
            self.codigo_objeto.append('DSVF ??')

            self.comandos()

            self.consumir('FECHA_CHAVE')

            self.codigo_objeto.append(f'DSVI {inicio_while}')
            self.codigo_objeto[endereco_dsvf] = f'DSVF {len(self.codigo_objeto)}'

    def condicao(self):
        # Trata uma condição relacional
        self.expressao()

        operador = self.token_atual()
        if operador[0] in ['IGUAL', 'DIFERENTE', 'MAIOR', 'MENOR', 'MAIOR_IGUAL', 'MENOR_IGUAL']:
            self.avancar()
        else:
            raise SyntaxError(f"Operador relacional esperado, mas encontrado: {operador}")

        self.expressao()

        if operador[0] == 'MAIOR':
            self.codigo_objeto.append("CPMA")
        elif operador[0] == 'MENOR':
            self.codigo_objeto.append("CPME")
        elif operador[0] == 'IGUAL':
            self.codigo_objeto.append("CPIG")
        elif operador[0] == 'DIFERENTE':
            self.codigo_objeto.append("CDES")
        elif operador[0] == 'MAIOR_IGUAL':
            self.codigo_objeto.append("CMEI")  
        elif operador[0] == 'MENOR_IGUAL':
            self.codigo_objeto.append("CMEG")  

    def resto_ident(self):
        # Continua analisando após um identificador
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
        # Expressão de atribuição
        token = self.token_atual()
        if token[0] == 'LERDOUBLE':
            self.consumir('LERDOUBLE')
            self.consumir('PARENTESE_ESQ')
            self.consumir('PARENTESE_DIR')
            self.codigo_objeto.append("LEIT")
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
        token = self.token_atual()

        if self.verificar('ID'):
            nome = token[1]
            if nome not in self.tabela_simbolos:
                raise Exception(f"Erro Semântico: Variável '{nome}' usada sem declaração.")
            endereco = self.tabela_simbolos[nome]
            self.avancar()
            self.codigo_objeto.append(f"CRVL {endereco}")

        elif self.verificar('NUMERO_INTEIRO') or self.verificar('NUMERO_REAL'):
            valor = token[1]
            self.avancar()
            self.codigo_objeto.append(f"CRCT {valor}")

        elif self.verificar('PARENTESE_ESQ'):
            self.avancar()
            self.expressao()
            self.consumir('PARENTESE_DIR')

        else:
            raise SyntaxError(f"Esperado identificador, número ou '(', mas encontrado: {token}")

    def outros_termos(self):
        while self.verificar('SOMA') or self.verificar('SUB'):
            operador = self.token_atual()[0]
            self.avancar()
            self.termo()
            if operador == 'SOMA':
                self.codigo_objeto.append("SOMA")
            elif operador == 'SUB':
                self.codigo_objeto.append("SUBT")

    def mais_fatores(self):
        while self.verificar('MULT') or self.verificar('DIV'):
            operador = self.token_atual()[0]
            self.avancar()
            self.fator()
            if operador == 'MULT':
                self.codigo_objeto.append("MULT")
            elif operador == 'DIV':
                self.codigo_objeto.append("DIVI")

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