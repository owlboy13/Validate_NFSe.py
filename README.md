# Validate_NFSe.py
Validação de Notas Fiscais do Sistema Nacional (NFS-e) com base no prestador, tomador, descrição, valor e código de tributação da nota fiscal.

Resumo: com as notas fiscais em pdf inderidas em uma pasta e uma planilha com os dados de validação, 
o código converte essas notas em xml e atraves desa conversão de cada dado buscado compara com o que está na planilha e indentifica se existe alguma divergência,
havendo essa diferença entre o que está na planilha e o que está na nota o código cria um arquivo em excel com o nome do prestador de serviço e demonstra na planilha qual o erro da nota.

dentro da pasta onde fica o código é preciso criar três pastas, resultados, xml, notas fiscais

resultados: onde será gerado a planilha comas divergencias
xml: onde será enviado os xmls convertidos
notas fiscais: onde será inserido as notas fiscais em pdf para validação


Exemplo:

o que está na planilha, correto:
prestador de serviço: José Paulo Duarte 
tomador de serviço: doces ltda
código: 26655
descrição da prestação de serviço: venda de doces
valor R$ 1.000,00

o que está na nota fiscal:

prestador de serviço: José Paulo Duarte 
tomador de serviço: doces ltda
código: 26655
descrição da prestação de serviço: venda de doces
valor R$ 1.200,00

o valor está errado na nota fiscal, dessa forma o código cria uma planilha de excel apenas do José Paulo Duarte, informando qual dado está incorreto, nesse caso é o valor.


