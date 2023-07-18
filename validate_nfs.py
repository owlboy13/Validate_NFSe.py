import pandas as pd
from pdfquery import PDFQuery
import os
import re

caminho_planilha_excel = 'notas_fiscais.xlsx'
caminho_diretorio_pdfs = './Notas'
resultados_diretorio = './resultados'
xml_diretorio = './xml'

planilha_excel = pd.read_excel(caminho_planilha_excel)

excel_colunas_mapa_codigo = {
  # 'razao_social_emitente': {
  #   'precisa_extrair_codigo': False,
  #   'xml_codigo': [
  #     '14.173, 686.71, 204.405, 694.71',
  #     '14.173, 690.07, 204.405, 700.15',
  #     '14.173, 690.07, 180.149, 700.15',
  #     '14.173, 690.07, 238.06, 700.15',
  #     '14.173, 690.07, 219.593, 700.15',
  #     '14.173, 690.07, 198.595, 700.15',
  #     '14.173, 690.07, 266.961, 700.15',
  #     '14.173, 690.07, 278.068, 700.15'
  #   ],
  # },
  'cnpj_emitente': {
    'precisa_extrair_codigo': False,
    'xml_codigo': [
      '155.906, 701.749, 227.524, 709.749',
      '155.906, 709.072, 227.524, 717.072',
      '155.906, 712.431, 227.524, 722.511',
    ],
  },
  'razao_social_tomador': {
    'precisa_extrair_codigo': False,
    'xml_codigo': [
      '14.173, 593.969, 177.89, 601.969',
      '14.173, 601.292, 177.89, 609.292',
      '14.173, 604.652, 177.89, 614.732',
    ],
  },
  'cnpj_tomador': {
    'precisa_extrair_codigo': False,
    'xml_codigo': [
      '155.906, 615.199, 227.524, 623.199',
      '155.906, 622.522, 227.524, 630.522',
      '155.906, 625.882, 227.524, 635.962',
    ],
  },
  'codigo': {
    'precisa_extrair_codigo': True,
    'xml_codigo': [
      '14.173, 525.705, 119.699, 533.705',
      '14.173, 533.027, 119.699, 541.027',
      '14.173, 536.387, 119.699, 546.467',
    ],
  },
  'descricao': {
    'precisa_extrair_codigo': False,
    'xml_codigo': [
      '14.173, 486.366, 330.437, 494.366',
      '14.173, 493.689, 330.437, 501.689',
      '14.173, 493.689, 326.027, 501.689',
      '14.173, 497.049, 326.027, 507.129',
    ],
  }, 
  'valor': {
    'precisa_extrair_codigo': True,
    'xml_codigo': [
      '14.173, 408.871, 50.981, 416.871',
      '14.173, 416.193, 57.645, 424.193',
      '14.173, 416.193, 50.981, 424.193',
      '14.173, 416.193, 50.981, 424.193',
      '14.173, 416.193, 46.533, 424.193',
      '14.173, 419.553, 50.981, 429.633',
      '14.173, 419.553, 57.645, 429.633',
    ]
  }
}

def print_message(message):
  print(message)
  print('================')

def extrair_codigo(text):
  return ''.join(re.findall('(\d+|\.\d+|,)', text))

def extrair_pdf_conteudo(pdf, nome_do_arquivo):
  conteudo = {}
  for chave, valor in excel_colunas_mapa_codigo.items():
    texto = ''
    for codigo in valor.get('xml_codigo', []):
      texto = pdf.pq(f'LTTextLineHorizontal:in_bbox("{codigo}")').text().strip()
      if texto:
        break
    
    if not texto:
      print_message(
        f'Nao achou valor para o campo `{chave}`, '
        'provavelmente precisa de novo codigo, '
        f'olhar o codigo em {xml_diretorio}/{nome_do_arquivo}.xml')
    
    if valor.get('precisa_extrair_codigo'):
      texto = extrair_codigo(texto)

    conteudo[chave] = texto
  
  return conteudo

# Percorrer os arquivos PDFs no diretório
for pdf_nome in os.listdir(caminho_diretorio_pdfs):

  if pdf_nome.endswith('.pdf'):
    caminho_pdf = os.path.join(caminho_diretorio_pdfs, pdf_nome)
    nome_do_arquivo, _ = os.path.splitext(pdf_nome)
    
    # Extrair informações do PDF usando o pdfquery
    pdf = PDFQuery(caminho_pdf)
    pdf.load()
    
    # Commando usado para transformar o pdf em xml e conseguir
    #  os codigos das colunas
    pdf.tree.write(f'./{xml_diretorio}/{nome_do_arquivo}.xml', pretty_print=True)

    # Extraindo informacoes do pdf
    conteudo = extrair_pdf_conteudo(
      pdf=pdf,
      nome_do_arquivo=nome_do_arquivo)

    # Encontra CNPJ do pdf na planilha e tratar alguns campos
    #  para evitar erros de comparação
    pdf_existe_no_excel = None
    campos_diferente_pdf = []
    for _, linha in planilha_excel.iterrows():
      if linha['CNPJ_Emitente'] == conteudo['cnpj_emitente']:
        linha['Codigo'] = f"{extrair_codigo(linha['Codigo'])},"
        linha['Descricao'] = linha['Descricao'].strip()
        _valor = linha['Valor'] # valor no excel
        linha['Valor'] = (_valor
                          if isinstance(_valor, float)
                          else float(str(_valor)
                                      .encode('ascii', 'replace')
                                      .decode('utf-8')
                                      .replace('R$', '')
                                      .replace('?', '')
                                      .replace(',', '.')))
        
        _valor = conteudo['valor'] # valor no pdf
        _valor = _valor.replace('.', '').replace(',', '.')
        conteudo['valor'] = float(_valor)
        pdf_existe_no_excel = linha
        break

    # Se o PDF existir na planilha compara
    #  se ha campos diferentes, se sim, informar
    #  quais são esses campos diferentes
    campos_diferente = {}
    if not isinstance(pdf_existe_no_excel, type(None)):
      campos_diferente_pdf = list(set(conteudo.values()) - set(pdf_existe_no_excel))
      if campos_diferente_pdf:
        for key, value in conteudo.items():
          if value in campos_diferente_pdf:
            campos_diferente[key] = value
    else:
      print_message("CNPJ do PDF nao encontrado na planilha")
    

    # Inicializa o DataFrame vazio dentro
    # do loop para sempre iniciar vazio
    resultados = pd.DataFrame(columns=[
      'PDF',
      'RazaoSocial_Emitente',
      'CNPJ_Emitente',
      'RazaoSocial_Tomador',
      'CNPJ_Tomador',
      'Codigo',
      'Descricao',
      'Valor'])
    codigo = campos_diferente.get('codigo')
    if campos_diferente:
      resultados = pd.DataFrame([{
        'PDF': pdf_nome, 
        'RazaoSocial_Emitente': campos_diferente.get('razao_social_emitente'),
        'CNPJ_Emitente': campos_diferente.get('cnpj_emitente'),
        'RazaoSocial_Tomador': campos_diferente.get('razao_social_tomador'),
        'CNPJ_Tomador': campos_diferente.get('cnpj_tomador'),
        'Codigo': codigo.replace(',', '') if codigo else None,
        'Descricao': campos_diferente.get('descricao'),
        'Valor': campos_diferente.get('valor')
      }])

    # grava os campos diferentes, se houve,
    # num arquivo csv
    if not resultados.empty:
      print_message(f'Salvando arquivo {nome_do_arquivo} - {campos_diferente=}')
      resultados.to_csv(f'{resultados_diretorio}/{nome_do_arquivo}.csv')
      
     
        

   
