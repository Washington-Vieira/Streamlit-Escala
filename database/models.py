from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date, datetime
from pydantic import validator

class EmpresaBase(SQLModel):
    nome: str = Field(unique=True, index=True)

class Empresa(EmpresaBase, table=True):
    __tablename__ = "empresas"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relacionamentos
    funcionarios: List["Funcionario"] = Relationship(back_populates="empresa")
    folguistas: List["Folguista"] = Relationship(back_populates="empresa")

class FuncionarioBase(SQLModel):
    nome: str = Field(index=True)
    funcao: str
    familia_letras: str
    horario_turno: str
    data_inicio: date
    turno: str
    empresa_id: int = Field(foreign_key="empresas.id")
    em_ferias: bool = Field(default=False)

    @validator('data_inicio', pre=True)
    def parse_data_inicio(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v

class Funcionario(FuncionarioBase, table=True):
    __tablename__ = "funcionarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relacionamentos
    empresa: Optional[Empresa] = Relationship(back_populates="funcionarios")
    ferias: List["Ferias"] = Relationship(back_populates="funcionario")
    atestados: List["Atestado"] = Relationship(back_populates="funcionario")

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'funcao': self.funcao,
            'familia_letras': self.familia_letras,
            'horario_turno': self.horario_turno,
            'data_inicio': self.data_inicio.strftime('%Y-%m-%d'),
            'turno': self.turno,
            'em_ferias': self.em_ferias
        }

class Folguista(FuncionarioBase, table=True):
    __tablename__ = "folguistas"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relacionamentos
    empresa: Optional[Empresa] = Relationship(back_populates="folguistas")
    escalas: List["EscalaFolguista"] = Relationship(back_populates="folguista")

class Ferias(SQLModel, table=True):
    __tablename__ = "ferias"
    id: Optional[int] = Field(default=None, primary_key=True)
    funcionario_id: int = Field(foreign_key="funcionarios.id")
    data_inicio: date
    data_fim: date
    ativa: bool = Field(default=True)
    
    # Relacionamento
    funcionario: Funcionario = Relationship(back_populates="ferias")

    @validator('data_inicio', 'data_fim', pre=True)
    def parse_dates(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v

class EscalaFolguista(SQLModel, table=True):
    __tablename__ = "escala_folguistas"
    id: Optional[int] = Field(default=None, primary_key=True)
    folguista_id: int = Field(foreign_key="folguistas.id")
    empresa_id: int = Field(foreign_key="empresas.id")
    data: date
    turno: str
    local: str

    # Relacionamentos
    folguista: Folguista = Relationship(back_populates="escalas")

class Atestado(SQLModel, table=True):
    __tablename__ = "atestados"
    id: Optional[int] = Field(default=None, primary_key=True)
    funcionario_id: int = Field(foreign_key="funcionarios.id")
    data_inicio: date
    data_fim: date
    motivo: str
    dias: int
    ativo: bool = Field(default=True)
    
    # Relacionamento
    funcionario: Funcionario = Relationship(back_populates="atestados")

    @validator('data_inicio', 'data_fim', pre=True)
    def parse_dates(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, '%Y-%m-%d').date()
        return v