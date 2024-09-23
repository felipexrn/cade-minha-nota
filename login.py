import requests
import getpass
import configparser
from datetime import datetime
import json
import os

def carregar_disciplinas(arquivo_json):
    if os.path.exists(arquivo_json):
        with open(arquivo_json, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    else:
        return {}

def salvar_disciplinas(arquivo_json, dados):
    with open(arquivo_json, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

# Função para baixar e salvar a foto do professor
def baixar_foto_professor(url_foto, nome_professor):
    resposta_foto = requests.get(url_foto)
    if resposta_foto.status_code == 200:
        nome_arquivo = f"{nome_professor.replace(' ', '_')}.jpg"
        with open(nome_arquivo, 'wb') as img_file:
            img_file.write(resposta_foto.content)
    else:
        print(f"Erro ao baixar a foto de {nome_professor}. Status: {resposta_foto.status_code}")

def pegar_atrasados():

    # Carregar disciplinas do arquivo JSON, se existir
    arquivo_json = 'disciplinas_sem_nota.json'
    disciplinas_sem_nota = carregar_disciplinas(arquivo_json)

    # Cria um objeto ConfigParser
    config = configparser.ConfigParser()

    # Carrega o arquivo config.ini
    config.read('config.ini')

    # Obtem os dados do arquivo de configuração
    matricula = config['SUAP']['MATRICULA']
    senha = config['SUAP']['SENHA']
    ano_letivo = config['SUAP']['ANO']
    periodo_letivo = config['SUAP']['PERIODO']
    data_ini = config['SUAP']['DATAINI']

    # Calcula o número de dias desde a data inicial até a data atual
    data_inicial = datetime.strptime(data_ini, '%d/%m/%Y')  # Converter a string da data inicial
    data_atual = datetime.now()  # Obter a data atual
    dias_sem_nota = (data_atual - data_inicial).days  # Calcular a diferença em dias  

    # URL de autenticação do SUAP
    url = "https://suap.ifrn.edu.br/api/v2/autenticacao/token/"
    token_access = ""
    token_refresh = ""

    # Pede dados de login se não estiverem configurados
    if (matricula == "" and senha ==""):
        matricula = input("digite sua matricula do SUAP\n")
        senha = getpass.getpass("Digite sua senha do SUAP\n")

    # Dados de login
    dados_login = {
        "username": f"{matricula}",
        "password": f"{senha}"
    }

    # Pede data inicial se não estiver configurada
    if (data_ini == ""):
        data_ini = input("digite a data inicial de contagem de dias (dd/mm/aaaa)\n")

    # Fazendo o POST para obter o token
    resposta_authenticacao = requests.post(url, data=dados_login)

    if resposta_authenticacao.status_code == 200:
        # Pegando o token
        token_access = resposta_authenticacao.json().get('access')
        token_refresh = resposta_authenticacao.json().get('refresh')

        print("Login bem sucedido.")
        
        # Exemplo de como usar o token para uma requisição autenticada
        cabecalho = {
            'Authorization': f'Bearer {token_access}',  # Corrigido para 'Bearer'
            'accept': 'application/json'  # Aceitar resposta em JSON
        }
        
        # Requisição dos meus dados 
        url_dados = "https://suap.ifrn.edu.br/api/v2/minhas-informacoes/meus-dados/"
        responsta_meus_dados = requests.get(url_dados, headers=cabecalho)
        
        # respostas da requisição 
        if responsta_meus_dados.status_code == 200:
            meus_dados = responsta_meus_dados.json()
            print(f"{meus_dados['nome_usual']} - {meus_dados['vinculo']['curso']}")
        else:
            print("Falha ao obter os dados:", responsta_meus_dados.status_code)   
            
        if ano_letivo == "" and periodo_letivo == "":
            # Pede o ano letivo e periodo letivo ao usuário se não tiver configurado
            ano_periodo_letivo = input("Digite o ano e periodo letivo para ver o boletim (formato: 2023.2)\n")    
            ano_periodo_letivo = '2024.1'
            ano_letivo, periodo_letivo = map(int, ano_periodo_letivo.split("."))

        # URL do boletim com o ano e periodo letivo
        url_boletim = f"https://suap.ifrn.edu.br/api/v2/minhas-informacoes/boletim/{ano_letivo}/{periodo_letivo}"

        # Requisição GET para buscar o boletim
        responsta_boletim = requests.get(url_boletim, headers=cabecalho)

        if responsta_boletim.status_code == 200:
            boletim = responsta_boletim.json()

            for disciplina in boletim:
                    
                if not disciplina['media_final_disciplina']:
                    nome_disciplina = disciplina['disciplina']                                                                         
                    
                    # URL da turma vitual com id    
                    url_turma_vitual = f"https://suap.ifrn.edu.br/api/v2/minhas-informacoes/turma-virtual/{disciplina['codigo_diario']}/"
                        
                    # Requisição GET para buscar turma vitual
                    resposta_turma_virtual = requests.get(url_turma_vitual, headers=cabecalho)
                        
                    if resposta_turma_virtual.status_code == 200:
                        turma_virtual = resposta_turma_virtual.json()
                        nome_professor = turma_virtual["professores"][0]["nome"]    
                        url_foto_professor = turma_virtual["professores"][0]["foto"]                
                        
                        # Atualiza ou adiciona a disciplina no dicionário
                        if nome_disciplina in disciplinas_sem_nota:
                            # Atualiza apenas o campo de dias se já existir
                            disciplinas_sem_nota[nome_disciplina]["dias"] = dias_sem_nota
                        else:
                            # Adiciona nova disciplina
                            disciplinas_sem_nota[nome_disciplina] = {
                                "dias": dias_sem_nota,
                                "professor": nome_professor,
                                "disciplina": nome_disciplina,
                                "ano": ano_letivo,
                                "periodo" : periodo_letivo
                            }                                   
                            
                        # Baixar e salvar a foto do professor
                        if not os.path.exists(f"{nome_professor.replace(' ', '_')}.jpg"):
                            baixar_foto_professor(url_foto_professor, nome_professor)
                    else:
                        print(f"Falha ao obter minhas turmas. Status: {resposta_turma_virtual.status_code}")                                    

            # Salva as disciplinas atualizadas no arquivo JSON
            salvar_disciplinas(arquivo_json, disciplinas_sem_nota)

            # Lista disciplinas sem notas do ano e período consultados
            print(f"Disciplinas que ainda não receberam notas em {ano_letivo}.{periodo_letivo}:")        
            for nome_disciplina, dados_disciplina in disciplinas_sem_nota.items():
                if ((dados_disciplina['ano'] == ano_letivo) and (dados_disciplina['periodo'] == periodo_letivo)):
                    print(f"- dias: {dados_disciplina['dias']} - {dados_disciplina['professor']} - {nome_disciplina}") 
                    
        else:
            print(f"Falha ao obter o boletim. Status: {responsta_boletim.status_code}")            
            
    else:
        print("Falha na autenticação:", resposta_authenticacao.status_code)
