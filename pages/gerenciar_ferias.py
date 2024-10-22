import streamlit as st
from datetime import datetime, timedelta
from data_manager import salvar_empresas

def app():
    st.title('Gerenciar Férias de Funcionários')
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(st.session_state.empresas.keys()))
    
    if empresa_selecionada:
        empresa = st.session_state.empresas[empresa_selecionada]
        funcionarios = []
        for turno in empresa.funcionarios.values():
            funcionarios.extend(turno)
        
        st.subheader('Registrar Férias')
        funcionario_selecionado = st.selectbox('Selecione o Funcionário', options=[f.nome for f in funcionarios])
        data_inicio_ferias = st.date_input('Data de Início das Férias', value=datetime.today())
        duracao_ferias = st.number_input('Duração das Férias (em dias)', min_value=1, max_value=30, value=30)
        
        if st.button('Registrar Férias'):
            for funcionario in funcionarios:
                if funcionario.nome == funcionario_selecionado:
                    data_fim_ferias = data_inicio_ferias + timedelta(days=duracao_ferias)
                    funcionario.registrar_ferias(data_inicio_ferias, data_fim_ferias)
                    
                    # Remover funcionário da escala de trabalho
                    empresa.remover_funcionario_da_escala(funcionario)
                    
                    salvar_empresas(st.session_state.empresas)
                    st.success(f'Férias registradas para {funcionario_selecionado} de {data_inicio_ferias} a {data_fim_ferias}. Funcionário removido da escala de trabalho.')
                    break
        
        st.subheader('Funcionários em Férias')
        funcionarios_em_ferias = [f for f in funcionarios if f.em_ferias()]
        for funcionario in funcionarios_em_ferias:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{funcionario.nome}: {funcionario.ferias['inicio']} a {funcionario.ferias['fim']}")
            with col2:
                if st.button('Retornar ao Trabalho', key=f'retorno_{funcionario.nome}'):
                    funcionario.encerrar_ferias()
                    empresa.adicionar_funcionario_a_escala(funcionario)
                    salvar_empresas(st.session_state.empresas)
                    st.success(f'{funcionario.nome} retornou ao trabalho e foi reintegrado à escala.')
                    st.rerun()
