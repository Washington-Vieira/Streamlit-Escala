import streamlit as st
import calendar
from datetime import datetime
from data_manager import salvar_empresas
from models import Funcionario

def app():
    st.title('Cadastro de Folguistas')
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(st.session_state.empresas.keys()))
    nome_folguista = st.text_input('Nome do Folguista')
    
    if st.button('Cadastrar Folguista'):
        if empresa_selecionada and nome_folguista:
            empresa = st.session_state.empresas[empresa_selecionada]
            
            data_atual = datetime.now()
            num_dias_no_mes = calendar.monthrange(data_atual.year, data_atual.month)[1]
            
            if empresa.folguistas_escala is None:
                empresa.folguistas_escala = []
            
            # Criar um novo folguista com valores padrão
            novo_folguista = Funcionario(
                nome=nome_folguista,
                funcao="Folguista",
                familia_letras="CP",
                horario_turno="Variável",
                data_inicio=data_atual.date(),
                turno="Variável"
            )
            empresa.folguistas.append(novo_folguista)
            
            # Atualizar a escala de folguistas
            folguista_escala = {'Folguista': f"{nome_folguista} (CP)"}
            folguista_escala.update({f'Dia {i+1}': '' for i in range(num_dias_no_mes)})
            empresa.folguistas_escala.append(folguista_escala)
            
            salvar_empresas(st.session_state.empresas)
            st.success(f'Folguista {nome_folguista} (CP) cadastrado na empresa {empresa_selecionada}!')
        else:
            st.error('Por favor, preencha todos os campos.')
