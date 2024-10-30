import streamlit as st
from database.config import get_session
from database.models import Empresa
from database.crud import DatabaseManager

def app():
    st.title('Cadastro de Empresas')
    
    session = next(get_session())
    db = DatabaseManager(session)
    
    nome_empresa = st.text_input('Nome da Empresa')
    
    if st.button('Cadastrar Empresa'):
        if nome_empresa:
            empresa_existente = db.obter_empresa_por_nome(nome_empresa)
            
            if not empresa_existente:
                nova_empresa = Empresa(nome=nome_empresa)
                db.criar_empresa(nova_empresa)
                st.success(f'Empresa {nome_empresa} cadastrada com sucesso!')
            else:
                st.error('Esta empresa já está cadastrada.')
        else:
            st.error('Por favor, insira um nome para a empresa.')

    # Lista de empresas cadastradas
    st.subheader("Empresas Cadastradas")
    empresas = db.listar_empresas()
    for empresa in empresas:
        st.write(f"- {empresa.nome}")
