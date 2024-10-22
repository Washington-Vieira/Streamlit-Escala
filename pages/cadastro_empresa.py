import streamlit as st
from data_manager import salvar_empresas
from models import Empresa

def app():
    st.title('Cadastro de Empresas')
    
    nome_empresa = st.text_input('Nome da Empresa')
    if st.button('Cadastrar Empresa'):
        if nome_empresa:
            if nome_empresa not in st.session_state.empresas:
                nova_empresa = Empresa(nome_empresa)
                st.session_state.empresas[nome_empresa] = nova_empresa
                salvar_empresas(st.session_state.empresas)
                st.success(f'Empresa {nome_empresa} cadastrada com sucesso!')
            else:
                st.error('Esta empresa já está cadastrada.')
        else:
            st.error('Por favor, insira um nome para a empresa.')
