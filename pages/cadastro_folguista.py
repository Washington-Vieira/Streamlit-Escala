import streamlit as st
import calendar
from datetime import datetime
from data_manager import salvar_empresas

def app():
    st.title('Cadastro de Folguistas')
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(st.session_state.empresas.keys()))
    nome_folguista = st.text_input('Nome do Folguista')
    
    if st.button('Cadastrar Folguista'):
        if empresa_selecionada:
            empresa = st.session_state.empresas[empresa_selecionada]
            
            data_atual = datetime.now()
            num_dias_no_mes = calendar.monthrange(data_atual.year, data_atual.month)[1]
            
            if empresa.folguistas_escala is None:
                empresa.folguistas_escala = []
            
            # Supondo que você tenha uma classe Funcionario
            novo_folguista = Funcionario(nome=nome_folguista)
            empresa.folguistas.append(novo_folguista)
            
            # Atualizar a escala de folguistas
            folguista_escala = {'Folguista': f"{nome_folguista} (CP)"}
            folguista_escala.update({f'Dia {i+1}': '' for i in range(num_dias_no_mes)})
            empresa.folguistas_escala.append(folguista_escala)
            
            salvar_empresas(st.session_state.empresas)
            st.success(f'Folguista {nome_folguista} (CP) cadastrado na empresa {empresa_selecionada}!')
