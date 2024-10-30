import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
from database.config import get_session
from database.crud import DatabaseManager
from exportar_escalas import exportar_escalas_para_excel, adicionar_botao_exportacao

def criar_tabela_dias_mes(folguistas):
    """Cria uma tabela com todos os dias do mês para cada folguista"""
    hoje = datetime.now()
    num_dias = calendar.monthrange(hoje.year, hoje.month)[1]
    colunas = ['Folguista'] + [f'Dia {i}' for i in range(1, num_dias + 1)]
    
    if 'escala_folguistas' not in st.session_state:
        # Criar novo DataFrame
        df = pd.DataFrame(index=range(len(folguistas)), columns=colunas)
        df['Folguista'] = [f"{f.nome} ({f.familia_letras})" for f in folguistas]
        for dia in range(1, num_dias + 1):
            df[f'Dia {dia}'] = ''
    else:
        # Usar DataFrame existente da sessão
        df = st.session_state.escala_folguistas
    
    return df

def app():
    st.title('Escala de Folguistas')
    
    session = next(get_session())
    db = DatabaseManager(session)
    
    empresas = db.listar_empresas()
    empresa_options = {empresa.nome: empresa.id for empresa in empresas}
    
    empresa_selecionada = st.selectbox('Selecione a Empresa', options=list(empresa_options.keys()))

    if empresa_selecionada:
        empresa_id = empresa_options[empresa_selecionada]
        folguistas = db.listar_folguistas_por_empresa(empresa_id)
        
        if folguistas:
            hoje = datetime.now()
            st.header(f'Escala de Folguistas - {calendar.month_name[hoje.month]} {hoje.year}')
            
            df_escala = criar_tabela_dias_mes(folguistas)
            
            # Editor de dados
            df_editado = st.data_editor(
                df_escala,
                key="editor_folguistas",
                disabled=["Folguista"],
                hide_index=True,
                use_container_width=True
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button('Salvar Alterações'):
                    st.session_state.escala_folguistas = df_editado
                    st.success('Alterações salvas com sucesso!')
            
            # with col2:
            #     if st.button('Exportar para Excel'):
            #         if 'escala_folguistas' in st.session_state:
            #             try:
            #                 df_vazio = pd.DataFrame()
            #                 excel_file = exportar_escalas_para_excel(
            #                     df_vazio, 
            #                     st.session_state.escala_folguistas,
            #                     empresa_selecionada,
            #                     f"{calendar.month_name[hoje.month]} {hoje.year}"
            #                 )
                            
            #                 st.download_button(
            #                     label="Baixar Excel",
            #                     data=excel_file,
            #                     file_name=f"escala_folguistas_{empresa_selecionada}_{hoje.strftime('%B_%Y')}.xlsx",
            #                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            #                 )
            #             except Exception as e:
            #                 st.error(f"Erro ao exportar: {str(e)}")
            #         else:
            #             st.warning("Por favor, salve as alterações antes de exportar.")
            
            with col3:
                if st.button('Limpar Escala'):
                    if 'escala_folguistas' in st.session_state:
                        del st.session_state.escala_folguistas
                        st.success('Escala limpa com sucesso!')
                        st.rerun()
                
        else:
            st.warning('Não há folguistas cadastrados para esta empresa.')
    else:
        st.warning('Selecione uma empresa para gerar a escala de folguistas.')
