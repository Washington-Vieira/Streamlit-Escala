from datetime import datetime, date

class Funcionario:
    def __init__(self, nome, funcao, familia_letras, horario_turno, data_inicio, turno):
        self.nome = nome
        self.funcao = funcao
        self.familia_letras = familia_letras
        self.horario_turno = horario_turno
        self.data_inicio = data_inicio
        self.turno = turno
        self.ferias_atual = None
        self.historico_ferias = []

    def registrar_ferias(self, data_inicio, data_fim):
        self.ferias_atual = {'inicio': data_inicio, 'fim': data_fim}
        self.historico_ferias.append(self.ferias_atual)

    def encerrar_ferias(self):
        if self.ferias_atual:
            self.ferias_atual = None

    def em_ferias(self):
        if self.ferias_atual is None:
            return False
        hoje = datetime.now().date()
        return self.ferias_atual['inicio'] <= hoje <= self.ferias_atual['fim']

class Empresa:
    def __init__(self, nome):
        self.nome = nome
        self.funcionarios = {'Turno 1': [], 'Turno 2': [], 'Turno 3': []}
        self.funcionarios_em_ferias = []
        self.folguistas = []
        self.folguistas_escala = None

    def adicionar_funcionario(self, funcionario):
        self.funcionarios[funcionario.turno].append(funcionario)

    def adicionar_folguista(self, nome):
        self.folguistas.append(nome)

    def remover_funcionario_da_escala(self, funcionario):
        for turno, lista_funcionarios in self.funcionarios.items():
            if funcionario in lista_funcionarios:
                lista_funcionarios.remove(funcionario)
                self.funcionarios_em_ferias.append(funcionario)
                break

    def adicionar_funcionario_a_escala(self, funcionario):
        if funcionario in self.funcionarios_em_ferias:
            self.funcionarios_em_ferias.remove(funcionario)
        self.funcionarios[funcionario.turno].append(funcionario)
