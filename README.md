📑 Validador de Notas Fiscais de Serviço (NFS-e) com PDFQuery
🔍 Sistema avançado de validação de NFS-e que utiliza PDFQuery para extração precisa de dados, comparando com planilha de referência e identificando divergências.

📌 Visão Geral
Este script Python automatiza a validação de NFS-e utilizando tecnologia moderna de extração de dados:
✅ Extrai dados de NFS-e em PDF usando PDFQuery (mais preciso que PyPDF2)
✅ Compara com planilha de referência (Excel/CSV)
✅ Gera relatórios detalhados de divergências por prestador

Ideal para departamentos fiscais, contadores e empresas que necessitam validar grandes volumes de notas fiscais com precisão.

⚙️ Funcionalidades
1. Extração Avançada de Dados
Utiliza PDFQuery para extração precisa de dados de NFS-e em PDF

Captura:

Prestador de serviço (nome/CNPJ)

Tomador de serviço (nome/CNPJ)

Código de tributação

Descrição do serviço

Valor da nota

2. Validação Automatizada
Compara dados extraídos com planilha de referência

Identifica divergências com precisão

Classifica erros por criticidade

3. Geração de Relatórios
Cria planilhas individuais por prestador

Detalha cada divergência encontrada

Formato limpo e profissional em Excel

🛠️ Tecnologias Utilizadas
Python 3.10+

PDFQuery (extração precisa de dados de PDF)

Pandas (manipulação de dados e comparação)

OpenPyXL (geração de relatórios em Excel)


📥 Configuração e Uso
Pré-requisitos
bash
pip install pdfquery pandas openpyxl
Estrutura de Pastas
text
/notas_fiscais    # Armazena os PDFs das NFS-e
/xml              # Armazena XMLs intermediários (opcional)
/resultados       # Relatórios de divergências
modelo.xlsx       # Planilha de referência
Como Usar
Preencha modelo.xlsx com os dados corretos

Coloque as NFS-e em PDF na pasta /notas_fiscais

Execute:

bash
python Validate_NFSe.py
Consulte os resultados em /resultados

📂 Exemplo de Saída
Relatório: Prestador_X.xlsx

Campo	Valor Esperado	Valor NFS-e	Status
Valor	R$ 1.000,00	R$ 1.200,00	❌ Erro
Código	26655	26655	✔ OK
🆚 Por que PDFQuery?
Maior precisão na extração de dados de PDF

Melhor tratamento de PDFs complexos

Extrai dados específicos por coordenadas ou tags

Mais confiável que PyPDF2 para NFS-e

🚀 Roadmap
Adicionar suporte a lote de notas

Implementar validação de CNPJ

Criar dashboard de resultados

Adicionar notificações por e-mail

📄 Licença
MIT License

