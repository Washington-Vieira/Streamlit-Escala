import streamlit as st
import pandas as pd
from data_manager import salvar_empresas
from exportar_escalas import adicionar_botao_exportacao

def app():
    st.title('Escala de Folguistas')

    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(st.session_state.empresas.keys()))

    if empresa_selecionada:
        empresa = st.session_state.empresas[empresa_selecionada]
        
        st.header('Escala de Folguistas')
        if empresa.folguistas_escala:
            df_folguistas = pd.DataFrame(empresa.folguistas_escala)
        else:
            df_folguistas = pd.DataFrame(columns=['Folguista'])

        st.write("Edite a escala dos folguistas:")
        
        df_folguistas_editado = st.data_editor(
            df_folguistas,
            key="editor_folguistas",
            num_rows="fixed",
            hide_index=True
        )
        
        if st.button('Salvar Alterações - Folguistas'):
            empresa.folguistas_escala = df_folguistas_editado.to_dict('records')
            salvar_empresas(st.session_state.empresas)
            st.success('Alterações na escala de folguistas salvas com sucesso!')

        # Adicionar botão de exportação
        # df_escala_final = pd.DataFrame()  # DataFrame vazio para a escala final
        # adicionar_botao_exportacao(df_escala_final, df_folguistas_editado, empresa_selecionada)

    else:
        st.warning('Selecione uma empresa para exibir a escala de folguistas.')
