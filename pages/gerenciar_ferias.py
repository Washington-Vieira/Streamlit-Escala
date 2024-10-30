import streamlit as st
from datetime import datetime, timedelta
from database.config import get_session
from database.crud import DatabaseManager
from database.models import Ferias

def app():
    st.title('Gerenciar Férias de Funcionários')
    
    # Inicializar conexão com banco de dados
    session = next(get_session())
    db = DatabaseManager(session)
    
    # Lista empresas do banco de dados
    empresas = db.listar_empresas()
    empresa_options = {empresa.nome: empresa.id for empresa in empresas}
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(empresa_options.keys()))
    
    if empresa_selecionada:
        empresa_id = empresa_options[empresa_selecionada]
        
        # Buscar funcionários e folguistas da empresa
        funcionarios = db.listar_funcionarios_por_empresa(empresa_id)
        folguistas = db.listar_folguistas_por_empresa(empresa_id)
        
        # Combinar listas de funcionários e folguistas
        todos_funcionarios = funcionarios + folguistas

        if todos_funcionarios:
            st.markdown("## Registrar Férias")
            with st.form("registrar_ferias"):
                funcionario_selecionado = st.selectbox(
                    'Selecione o Funcionário',
                    options=[f.nome for f in todos_funcionarios]
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    data_inicio_ferias = st.date_input('Data de Início das Férias', value=datetime.today())
                with col2:
                    duracao_ferias = st.number_input('Duração das Férias (em dias)', min_value=1, max_value=30, value=30)
                
                submit_button = st.form_submit_button("Registrar Férias")
                
                if submit_button:
                    funcionario = next((f for f in todos_funcionarios if f.nome == funcionario_selecionado), None)
                    if funcionario:
                        data_fim_ferias = data_inicio_ferias + timedelta(days=duracao_ferias)
                        
                        # Criar novo registro de férias
                        novas_ferias = Ferias(
                            funcionario_id=funcionario.id,
                            data_inicio=data_inicio_ferias,
                            data_fim=data_fim_ferias,
                            ativa=True
                        )
                        
                        # Atualizar status do funcionário
                        funcionario.em_ferias = True
                        
                        # Salvar no banco de dados
                        session.add(novas_ferias)
                        session.commit()
                        
                        st.success(f'Férias registradas para {funcionario_selecionado} de {data_inicio_ferias} a {data_fim_ferias}')
                        st.rerun()

            st.markdown("## Funcionários em Férias")
            funcionarios_em_ferias = [f for f in todos_funcionarios if f.em_ferias]
            
            if funcionarios_em_ferias:
                for funcionario in funcionarios_em_ferias:
                    # Buscar férias ativas do funcionário
                    ferias_ativa = session.query(Ferias).filter(
                        Ferias.funcionario_id == funcionario.id,
                        Ferias.ativa == True
                    ).first()
                    
                    if ferias_ativa:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.markdown(f"**{funcionario.nome}**")
                            with col2:
                                st.write(f"{ferias_ativa.data_inicio} a {ferias_ativa.data_fim}")
                            with col3:
                                if st.button('Retornar ao Trabalho', key=f'retorno_{funcionario.nome}'):
                                    # Encerrar férias ativas
                                    ferias_ativa.ativa = False
                                    funcionario.em_ferias = False
                                    session.commit()
                                    
                                    st.success(f'{funcionario.nome} retornou ao trabalho')
                                    st.rerun()
                        st.markdown("---")
            else:
                st.info("Não há funcionários em férias no momento.")

            st.markdown("## Histórico de Férias")
            # Buscar apenas funcionários que têm histórico de férias
            funcionarios_com_historico = session.query(Ferias.funcionario_id).distinct().all()
            funcionarios_com_historico_ids = [f[0] for f in funcionarios_com_historico]
            
            funcionarios_filtrados = [f for f in todos_funcionarios if f.id in funcionarios_com_historico_ids]
            
            if funcionarios_filtrados:
                for funcionario in funcionarios_filtrados:
                    historico = session.query(Ferias).filter(
                        Ferias.funcionario_id == funcionario.id
                    ).order_by(Ferias.data_inicio.desc()).all()
                    
                    with st.expander(f"{funcionario.nome}"):
                        for ferias in historico:
                            st.write(f"De {ferias.data_inicio} a {ferias.data_fim}")
                            if ferias.ativa:
                                st.write("*(Férias em andamento)*")
                            st.markdown("---")
            else:
                st.info("Nenhum funcionário possui histórico de férias.")
        else:
            st.warning('Não há funcionários cadastrados para esta empresa.')
    else:
        st.warning('Selecione uma empresa para gerenciar férias.')
