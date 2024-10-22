import json
import os
import streamlit as st
from models import Empresa, Funcionario
from datetime import datetime, date

# Atualize o caminho do arquivo
arquivo_empresas = os.path.join('data', 'empresas.json')

def carregar_empresas():
    try:
        with open('empresa.json', 'r') as f:
            dados = json.load(f)
        
        empresas = {}
        for nome, dados_empresa in dados.items():
            empresa = Empresa(nome)
            for turno, funcionarios in dados_empresa['funcionarios'].items():
                for f in funcionarios:
                    funcionario = criar_funcionario(f)
                    empresa.adicionar_funcionario(funcionario)
            
            for f in dados_empresa.get('funcionarios_em_ferias', []):
                funcionario = criar_funcionario(f)
                empresa.funcionarios_em_ferias.append(funcionario)
            
            empresa.folguistas = dados_empresa['folguistas']
            empresa.folguistas_escala = dados_empresa['folguistas_escala']
            empresas[nome] = empresa
        
        return empresas
    except FileNotFoundError:
        return {}

def salvar_empresas(empresas):
    dados = {}
    for nome, empresa in empresas.items():
        dados[nome] = {
            'nome': empresa.nome,
            'funcionarios': {
                turno: [
                    {
                        'nome': f.nome,
                        'funcao': f.funcao,
                        'familia_letras': f.familia_letras,
                        'horario_turno': f.horario_turno,
                        'data_inicio': f.data_inicio.strftime('%Y-%m-%d') if isinstance(f.data_inicio, (datetime, date)) else f.data_inicio,
                        'turno': f.turno,
                        'ferias_atual': f.ferias_atual,
                        'historico_ferias': [
                            {'inicio': ferias['inicio'].strftime('%Y-%m-%d'), 'fim': ferias['fim'].strftime('%Y-%m-%d')}
                            for ferias in f.historico_ferias
                        ]
                    } for f in funcionarios
                ] for turno, funcionarios in empresa.funcionarios.items()
            },
            'funcionarios_em_ferias': [
                {
                    'nome': f.nome,
                    'funcao': f.funcao,
                    'familia_letras': f.familia_letras,
                    'horario_turno': f.horario_turno,
                    'data_inicio': f.data_inicio.strftime('%Y-%m-%d') if isinstance(f.data_inicio, (datetime, date)) else f.data_inicio,
                    'turno': f.turno,
                    'ferias_atual': f.ferias_atual,
                    'historico_ferias': [
                        {'inicio': ferias['inicio'].strftime('%Y-%m-%d'), 'fim': ferias['fim'].strftime('%Y-%m-%d')}
                        for ferias in f.historico_ferias
                    ]
                } for f in empresa.funcionarios_em_ferias
            ],
            'folguistas': empresa.folguistas,
            'folguistas_escala': empresa.folguistas_escala
        }
    
    with open('empresa.json', 'w') as f:
        json.dump(dados, f, indent=4)

def criar_funcionario(dados):
    funcionario = Funcionario(
        dados['nome'],
        dados['funcao'],
        dados['familia_letras'],
        dados['horario_turno'],
        datetime.strptime(dados['data_inicio'], '%Y-%m-%d'),
        dados['turno']
    )
    funcionario.ferias_atual = dados['ferias_atual']
    if funcionario.ferias_atual:
        funcionario.ferias_atual['inicio'] = datetime.strptime(funcionario.ferias_atual['inicio'], '%Y-%m-%d').date()
        funcionario.ferias_atual['fim'] = datetime.strptime(funcionario.ferias_atual['fim'], '%Y-%m-%d').date()
    funcionario.historico_ferias = [
        {'inicio': datetime.strptime(ferias['inicio'], '%Y-%m-%d').date(),
         'fim': datetime.strptime(ferias['fim'], '%Y-%m-%d').date()}
        for ferias in dados['historico_ferias']
    ]
    return funcionario
