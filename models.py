from datetime import datetime

class Funcionario:
    def __init__(self, nome, funcao, familia_letras, horario_turno, data_inicio, turno):
        self.nome = nome
        self.funcao = funcao
        self.familia_letras = familia_letras
        self.horario_turno = horario_turno
        self.data_inicio = data_inicio
        self.turno = turno
        self.ferias = None

    def registrar_ferias(self, data_inicio, data_fim):
        self.ferias = {
            'inicio': data_inicio,
            'fim': data_fim
        }

    def encerrar_ferias(self):
        self.ferias = None

    def em_ferias(self):
        if self.ferias is None:
            return False
        hoje = datetime.now().date()
        return self.ferias['inicio'] <= hoje <= self.ferias['fim']

class Empresa:
    def __init__(self, nome):
        self.nome = nome
        self.funcionarios = {'Turno 1': [], 'Turno 2': [], 'Turno 3': []}
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
                break

    def adicionar_funcionario_a_escala(self, funcionario):
        self.funcionarios[funcionario.turno].append(funcionario)
