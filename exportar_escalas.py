import streamlit as st
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side
from openpyxl.utils import get_column_letter
from io import BytesIO
from datetime import datetime

def exportar_escalas_para_excel(df_escala_final, df_folguistas, empresa_nome, mes_ano):
    wb = Workbook()
    ws = wb.active
    ws.title = "Escala de Trabalho"

    # Configurar tamanho da página para A4
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE

    # Estilos
    titulo_font = Font(name='Arial', size=14, bold=True)
    header_font = Font(name='Arial', size=11, bold=True)
    cell_font = Font(name='Arial', size=10)
    border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

    # Título
    ws.merge_cells('A1:Z1')
    ws['A1'] = f"Escala de Trabalho - {empresa_nome} - {mes_ano}"
    ws['A1'].font = titulo_font
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    # Função para ajustar largura das colunas
    def ajustar_largura_colunas(worksheet):
        for column in worksheet.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 0.9
            worksheet.column_dimensions[column_letter].width = min(adjusted_width, 15)

    # Escala de trabalho
    if not df_escala_final.empty:
        # Cabeçalho da escala de trabalho
        for col, header in enumerate(df_escala_final.columns, start=1):
            cell = ws.cell(row=3, column=col, value=header)
            cell.font = header_font
            cell.border = border
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        # Dados da escala de trabalho
        for row, data in enumerate(df_escala_final.itertuples(index=False), start=4):
            for col, value in enumerate(data, start=1):
                cell = ws.cell(row=row, column=col, value=value)
                cell.font = cell_font
                cell.border = border
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    else:
        ws.cell(row=3, column=1, value="Nenhuma escala de trabalho disponível")

    ajustar_largura_colunas(ws)

    # Adicionar escala de folguistas em uma nova planilha
    ws_folguistas = wb.create_sheet(title="Escala de Folguistas")

    # Título da escala de folguistas
    ws_folguistas.merge_cells('A1:Z1')
    ws_folguistas['A1'] = f"Escala de Folguistas - {empresa_nome} - {mes_ano}"
    ws_folguistas['A1'].font = titulo_font
    ws_folguistas['A1'].alignment = Alignment(horizontal='center', vertical='center')

    if not df_folguistas.empty:
        # Cabeçalho da escala de folguistas
        for col, header in enumerate(df_folguistas.columns, start=1):
            cell = ws_folguistas.cell(row=3, column=col, value=header)
            cell.font = header_font
            cell.border = border
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

        # Dados da escala de folguistas
        for row, data in enumerate(df_folguistas.itertuples(index=False), start=4):
            for col, value in enumerate(data, start=1):
                cell = ws_folguistas.cell(row=row, column=col, value=value)
                cell.font = cell_font
                cell.border = border
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    else:
        ws_folguistas.cell(row=3, column=1, value="Nenhuma escala de folguistas disponível")

    ajustar_largura_colunas(ws_folguistas)

    # Salvar o arquivo Excel
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)
    
    return excel_file

# Função para adicionar o botão de exportação nas páginas
def adicionar_botao_exportacao(df_escala_final, df_folguistas, empresa_nome):
    if st.button('Exportar Escalas para Excel'):
        # Obter o mês e ano atual se não houver coluna 'Data'
        mes_ano = datetime.now().strftime('%B %Y')
        
        # Se houver uma coluna 'Data', use-a para obter o mês e ano
        if 'Data' in df_escala_final.columns and not df_escala_final['Data'].empty:
            mes_ano = pd.to_datetime(df_escala_final['Data'].iloc[0]).strftime('%B %Y')
        
        excel_file = exportar_escalas_para_excel(df_escala_final, df_folguistas, empresa_nome, mes_ano)
        
        st.download_button(
            label="Baixar Escalas em Excel",
            data=excel_file,
            file_name=f"escalas_{empresa_nome}_{mes_ano}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
