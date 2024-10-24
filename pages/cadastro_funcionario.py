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

    # Adicionar funcionalidade de exclusão de funcionário
    st.subheader('Excluir Funcionário')
    if empresa_selecionada:
        funcionarios = st.session_state.empresas[empresa_selecionada].funcionarios
        todos_funcionarios = [func for turno in funcionarios.values() for func in turno]
        funcionario_para_excluir = st.selectbox('Selecione o Funcionário para Excluir', options=[f.nome for f in todos_funcionarios])

        if st.button('Excluir Funcionário'):
            for turno, lista_funcionarios in funcionarios.items():
                for func in lista_funcionarios:
                    if func.nome == funcionario_para_excluir:
                        lista_funcionarios.remove(func)
                        # Remover o funcionário da escala
                        st.session_state.empresas[empresa_selecionada].remover_funcionario_da_escala(func)
                        salvar_empresas(st.session_state.empresas)
                        st.success(f'Funcionário {funcionario_para_excluir} excluído com sucesso!')
                        st.rerun()
