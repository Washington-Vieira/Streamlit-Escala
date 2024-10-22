import streamlit as st
from datetime import datetime
from data_manager import salvar_empresas
from models import Funcionario
from utils import funcoes_familias, turnos_funcionarios

def app():
    st.title('Cadastro de Funcionários')
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(st.session_state.empresas.keys()))
    nome_funcionario = st.text_input('Nome do Funcionário')
    turno_funcionario = st.selectbox('Selecione o Turno', options=turnos_funcionarios)
    funcao_funcionario = st.selectbox('Selecione a Função', options=list(funcoes_familias.keys()))
    familia_letras = funcoes_familias[funcao_funcionario]
    hora_inicio = st.time_input('Hora de Início do Turno', value=datetime.strptime("06:00", "%H:%M").time())
    hora_fim = st.time_input('Hora de Fim do Turno', value=datetime.strptime("14:00", "%H:%M").time())
    data_inicio = st.date_input('Data de Início', value=datetime.today())

    if st.button('Cadastrar Funcionário'):
        if all([nome_funcionario, funcao_funcionario, familia_letras, hora_inicio.strftime('%H:%M'), hora_fim.strftime('%H:%M'), data_inicio.strftime('%Y-%m-%d'), turno_funcionario, empresa_selecionada]):
            data_inicio_datetime = datetime.combine(data_inicio, datetime.min.time())
            novo_funcionario = Funcionario(
                nome_funcionario,
                funcao_funcionario,
                familia_letras,
                f"{hora_inicio.strftime('%H:%M')} as {hora_fim.strftime('%H:%M')}",
                data_inicio_datetime,
                turno_funcionario
            )
            st.session_state.empresas[empresa_selecionada].adicionar_funcionario(novo_funcionario)
            salvar_empresas(st.session_state.empresas)
            st.success(f'Funcionário {nome_funcionario} cadastrado com sucesso na empresa {empresa_selecionada}!')
        else:
            st.error('Por favor, preencha todos os campos.')
