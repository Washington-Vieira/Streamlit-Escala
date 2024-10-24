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
        # Certifique-se de que todos os itens são objetos de funcionário
        funcionarios.extend([f for f in empresa.funcionarios_em_ferias if hasattr(f, 'nome')])
        # Inclua os folguistas na lista de seleção de funcionários
        funcionarios.extend([f for f in empresa.folguistas if hasattr(f, 'nome')])

        st.subheader('Registrar Férias')
        # Inclua os folguistas na seleção de funcionários
        funcionario_selecionado = st.selectbox('Selecione o Funcionário', options=[f.nome for f in funcionarios])
        data_inicio_ferias = st.date_input('Data de Início das Férias', value=datetime.today())
        duracao_ferias = st.number_input('Duração das Férias (em dias)', min_value=1, max_value=30, value=30)
        
        if st.button('Registrar Férias'):
            for funcionario in funcionarios:
                if funcionario.nome == funcionario_selecionado:
                    data_fim_ferias = data_inicio_ferias + timedelta(days=duracao_ferias)
                    funcionario.registrar_ferias(data_inicio_ferias, data_fim_ferias)
                    empresa.remover_funcionario_da_escala(funcionario)
                    salvar_empresas(st.session_state.empresas)
                    st.success(f'Férias registradas para {funcionario_selecionado} de {data_inicio_ferias} a {data_fim_ferias}. Funcionário removido da escala de trabalho.')
                    st.rerun()
        
        st.subheader('Funcionários em Férias')
        funcionarios_em_ferias = [f for f in funcionarios if f.em_ferias()]
        if funcionarios_em_ferias:
            for funcionario in funcionarios_em_ferias:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{funcionario.nome}: {funcionario.ferias_atual['inicio']} a {funcionario.ferias_atual['fim']}")
                with col2:
                    if st.button('Retornar ao Trabalho', key=f'retorno_{funcionario.nome}'):
                        funcionario.encerrar_ferias()
                        if funcionario in empresa.folguistas:
                            empresa.adicionar_folguista(funcionario)
                        else:
                            empresa.adicionar_funcionario_a_escala(funcionario)
                        salvar_empresas(st.session_state.empresas)
                        st.success(f'{funcionario.nome} retornou ao trabalho e foi reintegrado à escala ou lista de folguistas.')
                        st.rerun()
        else:
            st.info("Não há funcionários em férias no momento.")

        st.subheader('Histórico de Férias')
        funcionarios_com_historico = [f for f in funcionarios if f.historico_ferias]
        if funcionarios_com_historico:
            for funcionario in funcionarios_com_historico:
                st.write(f"{funcionario.nome}:")
                for ferias in funcionario.historico_ferias:
                    st.write(f"  - De {ferias['inicio']} a {ferias['fim']}")
        else:
            st.info("Não há histórico de férias registrado.")
