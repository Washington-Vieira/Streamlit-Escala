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

    # Adicionar funcionalidade de exclusão de folguista
    st.subheader('Excluir Folguista')
    if empresa_selecionada:
        empresa = st.session_state.empresas[empresa_selecionada]
        folguistas = empresa.folguistas
        folguista_para_excluir = st.selectbox('Selecione o Folguista para Excluir', options=[f.nome for f in folguistas])

        if st.checkbox('Confirmar exclusão', key='confirm_excluir_folguista'):
            if st.button('Excluir Folguista'):
                for folguista in folguistas:
                    if folguista.nome == folguista_para_excluir:
                        folguistas.remove(folguista)
                        # Remover o folguista da escala
                        empresa.remover_folguista_da_escala(folguista)
                        salvar_empresas(st.session_state.empresas)
                        st.success(f'Folguista {folguista_para_excluir} excluído com sucesso!')
                        st.rerun()
        else:
            st.error('Marque a caixa de confirmação para excluir.', icon="⚠️")
