# M.IA

Este projeto é uma aplicação Python para processar números de processos judiciais a partir de arquivos Excel.
Ele formata, classifica, e organiza os números de processos em diferentes categorias (Judicial, NUP, Inválido),
além de aplicar regras específicas para identificar a justiça e o tribunal associados aos processos judiciais.

- **PROJETO:** ATUALIZAÇÃO EM LOTE DO VALOR ECONÔMICO NO SAPIENS

- **NUP:** 00410.061155/2024-76

![Imagem Front-end do Robô M.IA](../M.IA/UI/image/mia_front_end.png)


## Arquivo de Entrada

O robô M.IA processa arquivos Excel no formato ".xlsx". 
Independentemente do número de colunas presentes no arquivo, apenas as seguintes colunas são obrigatórias:

    NUMERO PROCESSO  |  VALOR UNIAO  |  DATA DE SAIDA NECAP

## Funcionalidades

- **Formatação de Números de Processos:** Remove caracteres não numéricos e ajusta o tamanho dos números de processos para garantir que estejam no formato correto.


- **Verificação de Categorias:** Classifica os números de processos como "Judicial", "NUP" ou "Inválido" com base em padrões específicos.


- **Extração de Informações:** Aplica regras para identificar a justiça e o tribunal de processos judiciais usando funções externas do módulo "regraOrgao".


- **Filtragem e Organização:** Filtra processos judiciais onde as regras não foram encontradas e organiza os dados em diferentes planilhas de um arquivo Excel.


- **Manuseio de Arquivos Excel:** Lê e escreve arquivos Excel, com suporte para múltiplas planilhas, preservando as colunas relevantes para cada categoria de processos.



## Dependências

É recomendado o uso de um ambiente virtual python para evitar a interferência na configuração da máquina.

Para gerar um ambiente python virtual utilize o comando a seguir:
    
    python -m venv .venv 

### Este projeto requer as seguintes bibliotecas:

#### Para gerar o executável:

- pyinstaller e/ou auto-py-to-exe. (Use o arquivo **main.py** como principal)

#### Back-end:

- Pandas: Para manipulação de dados e operações com arquivos Excel.


- Openpyxl: Para leitura e escrita de arquivos Excel.


- re (Regex): Para formatação de números de processos usando expressões regulares.


- logging: Para registro de eventos e mensagens de erro.

#### Front-end:
- PyQt5: Para disposição do layout

 Para facilitar, todas as dependências podem ser instaladas usando o comando abaixo.
 As dependências usadas estão no arquivo **requirements.txt**.

    python -m pip install -r requirements.txt

Se novas bibliotecas forem inclusas no projeto, pode ser necessário atualizar o arquivo **requirements.txt**. Se for esse o caso atualize com o comando abaixo:

    python -m pip freeze > requirements.txt

## Logs e Mensagens de Erro

Durante a execução, o script gera logs para informar o status do processamento, como erros ao ler ou salvar arquivos,
e inconsistências no formato dos números dos processos. Esses logs ajudam a identificar e resolver possíveis problemas.

## Personalização

Você pode personalizar as funções no arquivo **main.py** para adaptar o processamento às suas necessidades específicas. 
Além disso, o módulo **regraOrgao.py** pode ser expandido para incluir novas regras ou modificar as existentes.

## Contribuição

Contribuições são bem-vindas!
Se você encontrar bugs ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto é distribuído sob a licença MIT. Consulte o arquivo **LICENSE** para obter mais informações.