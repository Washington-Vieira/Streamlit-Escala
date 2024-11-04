import streamlit as st
from datetime import datetime
from database.config import get_session
from database.models import Folguista
from database.crud import DatabaseManager

def app():
    st.title('Cadastro de Folguistas')
    
    session = next(get_session())
    db = DatabaseManager(session)
    
    # Lista de empresas para seleção
    empresas = db.listar_empresas()
    empresa_options = {empresa.nome: empresa.id for empresa in empresas}
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(empresa_options.keys()))
    nome_folguista = st.text_input('Nome do Folguista')
    
    if st.button('Cadastrar Folguista'):
        if empresa_selecionada and nome_folguista:
            novo_folguista = Folguista(
                nome=nome_folguista,
                funcao="Folguista",
                familia_letras="CP",
                horario_turno="Variável",
                data_inicio=datetime.now().date(),
                turno="Variável",
                empresa_id=empresa_options[empresa_selecionada],
                em_ferias=False
            )
            
            db.criar_folguista(novo_folguista)
            st.success(f'Folguista {nome_folguista} cadastrado com sucesso!')
        else:
            st.error('Por favor, preencha todos os campos.')

    # Lista de folguistas da empresa selecionada
    if empresa_selecionada:
        st.subheader(f"Folguistas de {empresa_selecionada}")
        folguistas = db.listar_folguistas_por_empresa(empresa_options[empresa_selecionada])
        for folg in folguistas:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"- {folg.nome}")
            with col2:
                if st.button(f'Excluir {folg.nome}'):
                    # Alerta de confirmação
                    if st.session_state.get(f'confirmar_exclusao_{folg.id}', False):
                        db.session.delete(folg)  # Exclui o folguista
                        db.session.commit()  # Confirma a exclusão
                        st.success(f'Folguista {folg.nome} excluído com sucesso!')
                        st.session_state[f'confirmar_exclusao_{folg.id}'] = False  # Resetar estado
                    else:
                        st.session_state[f'confirmar_exclusao_{folg.id}'] = True
                        st.warning(f'Você tem certeza que deseja excluir o folguista {folg.nome}? Clique novamente para confirmar.')
