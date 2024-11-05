from sqlmodel import Session, select
from typing import List, Optional
from .models import Empresa, Funcionario, Ferias, Atestado

class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def criar_empresa(self, empresa: Empresa) -> Empresa:
        self.session.add(empresa)
        self.session.commit()
        self.session.refresh(empresa)
        return empresa

    def obter_empresa_por_nome(self, nome: str) -> Optional[Empresa]:
        statement = select(Empresa).where(Empresa.nome == nome)
        return self.session.exec(statement).first()

    def listar_empresas(self) -> List[Empresa]:
        statement = select(Empresa)
        return self.session.exec(statement).all()

    def criar_funcionario(self, funcionario: Funcionario) -> Funcionario:
        self.session.add(funcionario)
        self.session.commit()
        self.session.refresh(funcionario)
        return funcionario

    def listar_funcionarios_por_empresa(self, empresa_id: int) -> List[Funcionario]:
        statement = select(Funcionario).where(Funcionario.empresa_id == empresa_id)
        return self.session.exec(statement).all()

    def criar_atestado(self, atestado: Atestado) -> Atestado:
        self.session.add(atestado)
        self.session.commit()
        self.session.refresh(atestado)
        return atestado

    def listar_atestados_ativos(self, empresa_id: int) -> List[Atestado]:
        statement = (
            select(Atestado)
            .join(Funcionario)
            .where(
                Funcionario.empresa_id == empresa_id,
                Atestado.ativo == True
            )
        )
        return self.session.exec(statement).all()

    def encerrar_atestado(self, atestado_id: int):
        atestado = self.session.get(Atestado, atestado_id)
        if atestado:
            atestado.ativo = False
            self.session.commit()

    def listar_funcionarios_folguistas_por_empresa(self, empresa_id: int) -> List[Funcionario]:
        statement = select(Funcionario).where(
            Funcionario.empresa_id == empresa_id,
            Funcionario.is_folguista == True  # Filtra apenas os folguistas
        )
        return self.session.exec(statement).all()

    def listar_funcionarios(self) -> List[Funcionario]:
        """Retorna uma lista de todos os funcionários."""
        statement = select(Funcionario)
        return self.session.exec(statement).all()

    def listar_folguistas_por_empresa(self, empresa_id):
        """Retorna a lista de folguistas para uma empresa específica."""
        return self.session.query(Funcionario).filter(
            Funcionario.empresa_id == empresa_id,
            Funcionario.is_folguista == True
        ).all()