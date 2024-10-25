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

    # Função para configurar dimensões e estilos das células
    def configurar_celulas(worksheet, df):
        # Configurar largura das colunas
        for col in worksheet.columns:
            col_letter = get_column_letter(col[0].column)
            if col[0].column == 1:  # Coluna dos nomes
                worksheet.column_dimensions[col_letter].width = 20  # Ajuste conforme necessário
            else:  # Colunas dos dias
                worksheet.column_dimensions[col_letter].width = 6

        # Configurar altura das linhas
        worksheet.row_dimensions[3].height = 15  # Altura do cabeçalho
        for row in range(4, worksheet.max_row + 1):  # Linhas de dados
            worksheet.row_dimensions[row].height = 50.25

        # Aplicar estilos
        for row in worksheet.iter_rows(min_row=1, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
            for cell in row:
                cell.border = border
                cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
                if cell.row == 3:
                    cell.font = header_font
                else:
                    cell.font = cell_font

        # Ajustar o tamanho da fonte da linha 3 para 10
        for col in worksheet.iter_cols(min_row=3, max_row=3):
            for cell in col:
                cell.font = Font(size=10, bold=True)

    # Remover todas as bordas da linha 2
    no_border = Border(left=Side(style=None), 
                       right=Side(style=None), 
                       top=Side(style=None), 
                       bottom=Side(style=None))
    
    for col in ws.iter_cols(min_row=2, max_row=2):
        for cell in col:
            cell.border = no_border

    # Escala de trabalho
    if not df_escala_final.empty:
        # Cabeçalho da escala de trabalho
        for col, header in enumerate(df_escala_final.columns, start=1):
            ws.cell(row=3, column=col, value=header)

        # Dados da escala de trabalho
        for row, data in enumerate(df_escala_final.itertuples(index=False), start=4):
            for col, value in enumerate(data, start=1):
                ws.cell(row=row, column=col, value=value)

        configurar_celulas(ws, df_escala_final)
    else:
        ws.cell(row=3, column=1, value="Nenhuma escala de trabalho disponível")

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
            ws_folguistas.cell(row=3, column=col, value=header)

        # Dados da escala de folguistas
        for row, data in enumerate(df_folguistas.itertuples(index=False), start=4):
            for col, value in enumerate(data, start=1):
                ws_folguistas.cell(row=row, column=col, value=value)

        configurar_celulas(ws_folguistas, df_folguistas)
    else:
        ws_folguistas.cell(row=3, column=1, value="Nenhuma escala de folguistas disponível")

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
