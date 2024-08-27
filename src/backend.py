import pandas as pd
import re
import logging
from . import regraOrgao  # Importa o módulo regraOrgao, que deve conter funções para verificar a justiça e o tribunal

# Configura o nível de log para INFO, o que significa que todas as mensagens de INFO e erros serão exibidas
logging.basicConfig(level=logging.INFO)


def formatar_numero_processo(numero):
    """
        Formata o número do processo para 20 caracteres, se possível.
        Remove todos os caracteres não numéricos e ajusta o tamanho do número.
    """
    numero_formatado = re.sub(r'\D', '', str(numero))  # Remove caracteres não numéricos
    tamanho = len(numero_formatado)

    if 18 <= tamanho <= 20:
        return numero_formatado.zfill(20)  # Preenche com zeros à esquerda se necessário para ter 20 dígitos
    elif tamanho == 17:
        return numero_formatado
    elif tamanho > 20:
        logging.info(f"Tamanho incorreto. Maior que 20 caracteres: {numero_formatado}")
        return numero_formatado
    else:
        logging.info(f"Número com menos de 18 caracteres: {numero_formatado}")
        return numero_formatado


def verificar_vazio_ou_zeros(numero_formatado):
    """
        Verifica se o número formatado está vazio ou contém apenas zeros.
        Retorna True se estiver vazio ou se for composto apenas por zeros.
    """
    return not numero_formatado or numero_formatado == '0' * len(numero_formatado)


def verifica_nup_jud(numero_formatado):
    """
        Verifica se o número formatado é um NUP (Número Único de Protocolo) válido ou um número Judicial.
        Retorna 'Judicial', 'NUP' ou 'Inválido' dependendo do formato e dos critérios de validação.
    """
    if not numero_formatado:
        return 'Inválido'

    padrao_nup = r'^0*(\d{5}\d{6}\d{4}\d{2})$'
    padrao_jud = r'^0*(\d{7}\d{2}\d{4}\d{1}\d{2}\d{4})$'

    regex_nup = re.compile(padrao_nup)
    regex_jud = re.compile(padrao_jud)

    numero = str(numero_formatado)

    def segmento_de_data_valido(segmento):
        """
        Verifica se o segmento de data (parte do número) está dentro do intervalo esperado (1950-2025).
        """
        return 1950 <= int(segmento) <= 2025

    if len(numero) > 7 and segmento_de_data_valido(numero[-11:-7]) and regex_jud.match(numero):
        return 'Judicial'
    elif len(numero) > 2 and segmento_de_data_valido(numero[-6:-2]) and regex_nup.match(numero):
        return 'NUP'

    return 'Inválido'


def ler_excel(arquivo_entrada):
    """
        Lê o arquivo Excel de entrada e retorna um DataFrame.
        Retorna None se ocorrer algum erro na leitura do arquivo.
    """
    try:
        return pd.read_excel(arquivo_entrada, engine='openpyxl')
    except Exception as e:
        logging.error(f"Erro ao ler o arquivo Excel: {e}")
        return None


def salvar_excel(dfs, arquivo_saida):
    """
        Salva os DataFrames processados em um arquivo Excel com múltiplas planilhas.
        Cada planilha contém dados de uma categoria específica (Judicial, NUP, Inválido).
    """
    try:
        with pd.ExcelWriter(arquivo_saida) as writer:
            for nome, df in dfs.items():
                # Renomeia colunas antes de salvar
                df = df.rename(columns={
                    'NUMERO PROCESSO': 'PROCESSO',
                    'VALOR UNIAO': 'VALOR ECONOMICO',
                })

                if nome == 'Judicial':
                    # Seleciona apenas as colunas relevantes para processos judiciais
                    df = df[['PROCESSO', 'VALOR ECONOMICO', 'JUSTIÇA', 'TRIBUNAL', 'PROCURADORIA']]
                elif nome == 'Outros Órgãos':
                    # Seleciona apenas as colunas relevantes para outros órgãos
                    df = df[['PROCESSO', 'VALOR ECONOMICO', 'JUSTIÇA', 'TRIBUNAL']]
                else:
                    # Seleciona apenas as colunas relevantes para outros tipos de processos
                    df = df[['PROCESSO', 'VALOR ECONOMICO']]

                df.to_excel(writer, sheet_name=nome, index=False)  # Salva cada DataFrame em uma planilha separada
        logging.info(f'Arquivo {arquivo_saida} salvo com sucesso!')
    except Exception as e:
        logging.error(f"Erro ao salvar o arquivo Excel: {e}")


def processar_dados_excel(arquivo_entrada):
    """
        Processa o arquivo Excel de entrada e retorna DataFrames processados, organizados por categoria:
        'Judicial', 'NUP', 'Inválido'. Aplica as funções de formatação e classificação aos números de processos.
    """
    df = ler_excel(arquivo_entrada)
    if df is None:
        return None

    # Verifica se as colunas esperadas estão presentes no arquivo Excel
    if 'NUMERO PROCESSO' not in df.columns or 'DATA DE SAIDA NECAP' not in df.columns:
        logging.error("As colunas 'NUMERO PROCESSO' ou 'DATA DE SAIDA NECAP' não foram encontradas no arquivo Excel.")
        return None

    # Formata os números dos processos
    df['NUMERO PROCESSO'] = df['NUMERO PROCESSO'].apply(formatar_numero_processo)

    # Remove linhas com números de processos vazios ou inválidos
    df = df[~df['NUMERO PROCESSO'].apply(verificar_vazio_ou_zeros) & (df['NUMERO PROCESSO'] != '')]

    # Verifica e classifica os números dos processos em 'Judicial', 'NUP' ou 'Inválido'
    df['CATEGORIA'] = df['NUMERO PROCESSO'].apply(verifica_nup_jud)

    # Formata a coluna 'DATA DE SAIDA NECAP' para datetime
    df['DATA DE SAIDA NECAP'] = pd.to_datetime(df['DATA DE SAIDA NECAP'], errors='coerce')

    # Ordena pelo 'DATA DE SAIDA NECAP' e remove duplicatas mantendo a última ocorrência
    df = df.sort_values(by='DATA DE SAIDA NECAP').drop_duplicates(subset=['NUMERO PROCESSO'], keep='last')

    # Separa os dados em categorias e adiciona informações específicas para processos judiciais
    aba_judicial = df[df['CATEGORIA'] == 'Judicial']
    aba_judicial = aba_judicial.copy()  # Cria uma cópia para modificar e evitar o SettingWithCopyWarning

    # Aplica funções do módulo regraOrgao para verificar justiça e tribunal
    aba_judicial['JUSTIÇA'] = aba_judicial['NUMERO PROCESSO'].apply(regraOrgao.verifica_justica)
    aba_judicial[['TRIBUNAL', 'PROCURADORIA']] = aba_judicial['NUMERO PROCESSO'].apply(
        lambda x: pd.Series(regraOrgao.verifica_tribunal(x))
    )

    # Filtra os processos judiciais onde a justiça ou o tribunal não foram encontrados
    aba_nao_encontrada = aba_judicial[
        (aba_judicial['JUSTIÇA'] == 'Regra não Encontrada.') |
        (aba_judicial['TRIBUNAL'] == 'Regra não Encontrada.')
        ]

    return {
        'Judicial': aba_judicial,
        'NUP': df[df['CATEGORIA'] == 'NUP'],
        'Inválido': df[df['CATEGORIA'] == 'Inválido'],
        'Outros Órgãos': aba_nao_encontrada
    }
