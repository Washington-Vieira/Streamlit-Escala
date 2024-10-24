import streamlit as st
from datetime import datetime, timedelta
from data_manager import salvar_empresas, carregar_empresas

def app():
    st.title('Gerenciar Férias de Funcionários')
    
    # Carregue as empresas do arquivo JSON
    st.session_state.empresas = carregar_empresas()
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(st.session_state.empresas.keys()))
    
    if empresa_selecionada:
        empresa = st.session_state.empresas[empresa_selecionada]
        funcionarios = []
        for turno in empresa.funcionarios.values():
            funcionarios.extend(turno)
        funcionarios.extend([f for f in empresa.funcionarios_em_ferias if hasattr(f, 'nome')])
        funcionarios.extend([f for f in empresa.folguistas if hasattr(f, 'nome')])

        st.markdown("## Registrar Férias")
        with st.form("registrar_ferias"):
            funcionario_selecionado = st.selectbox('Selecione o Funcionário', options=[f.nome for f in funcionarios])
            col1, col2 = st.columns(2)
            with col1:
                data_inicio_ferias = st.date_input('Data de Início das Férias', value=datetime.today())
            with col2:
                duracao_ferias = st.number_input('Duração das Férias (em dias)', min_value=1, max_value=30, value=30)
            
            submit_button = st.form_submit_button("Registrar Férias")
            
            if submit_button:
                for funcionario in funcionarios:
                    if funcionario.nome == funcionario_selecionado:
                        data_fim_ferias = data_inicio_ferias + timedelta(days=duracao_ferias)
                        funcionario.registrar_ferias(data_inicio_ferias, data_fim_ferias)
                        
                        if funcionario.funcao == "Folguista":
                            empresa.remover_folguista_da_escala(funcionario)
                            st.success(f'Férias registradas para o folguista {funcionario_selecionado} de {data_inicio_ferias} a {data_fim_ferias}. Folguista removido da escala de trabalho.')
                        else:
                            empresa.remover_funcionario_da_escala(funcionario)
                            st.success(f'Férias registradas para {funcionario_selecionado} de {data_inicio_ferias} a {data_fim_ferias}. Funcionário removido da escala de trabalho.')
                        
                        salvar_empresas(st.session_state.empresas)
                        st.rerun()
        
        st.markdown("## Funcionários em Férias")
        funcionarios_em_ferias = [f for f in funcionarios if f.em_ferias()]
        if funcionarios_em_ferias:
            for funcionario in funcionarios_em_ferias:
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.markdown(f"**{funcionario.nome}**")
                    with col2:
                        st.write(f"{funcionario.ferias_atual['inicio']} a {funcionario.ferias_atual['fim']}")
                    with col3:
                        if st.button('Retornar ao Trabalho', key=f'retorno_{funcionario.nome}'):
                            funcionario.encerrar_ferias()
                            if funcionario.funcao == "Folguista":
                                empresa.adicionar_folguista_a_escala(funcionario)
                                st.success(f'{funcionario.nome} retornou ao trabalho e foi reintegrado à escala de folguistas.')
                            else:
                                empresa.adicionar_funcionario_a_escala(funcionario)
                                st.success(f'{funcionario.nome} retornou ao trabalho e foi reintegrado à escala.')
                            salvar_empresas(st.session_state.empresas)
                            st.rerun()
                st.markdown("---")
        else:
            st.info("Não há funcionários em férias no momento.")

        st.markdown("## Histórico de Férias")
        funcionarios_com_historico = [f for f in funcionarios if f.historico_ferias]
        if funcionarios_com_historico:
            for funcionario in funcionarios_com_historico:
                with st.expander(f"{funcionario.nome}"):
                    for ferias in funcionario.historico_ferias:
                        st.write(f"De {ferias['inicio']} a {ferias['fim']}")
        else:
            st.info("Não há histórico de férias registrado.")
