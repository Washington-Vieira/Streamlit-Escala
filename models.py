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
        if isinstance(data_inicio, str):
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if isinstance(data_fim, str):
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
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

    def to_dict(self):
        return {
            'nome': self.nome,
            'funcao': self.funcao,
            'familia_letras': self.familia_letras,
            'horario_turno': self.horario_turno,
            'data_inicio': self.data_inicio.strftime('%Y-%m-%d') if isinstance(self.data_inicio, date) else self.data_inicio,
            'turno': self.turno,
            'ferias_atual': self.ferias_atual_to_dict(),
            'historico_ferias': self.historico_ferias_to_dict()
        }

    def ferias_atual_to_dict(self):
        if self.ferias_atual:
            return {
                'inicio': self.ferias_atual['inicio'].strftime('%Y-%m-%d'),
                'fim': self.ferias_atual['fim'].strftime('%Y-%m-%d')
            }
        return None

    def historico_ferias_to_dict(self):
        return [
            {
                'inicio': ferias['inicio'].strftime('%Y-%m-%d'),
                'fim': ferias['fim'].strftime('%Y-%m-%d')
            }
            for ferias in self.historico_ferias
        ]

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
