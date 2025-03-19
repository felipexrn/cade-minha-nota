import requests
import getpass
import configparser
from datetime import datetime
import json
import os

# carrega ou cria o arquivo das disciplinas sem notas postadas
def carregar_disciplinas(arquivo_json):
    if os.path.exists(arquivo_json):
        with open(arquivo_json, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    else:
        # Se o arquivo não existir, cria um novo arquivo vazio
        with open(arquivo_json, 'w', encoding='utf-8') as arquivo:
            json.dump({}, arquivo, ensure_ascii=False, indent=4)
        return {}

# salva o arquivo das disciplinas sem notas postadas
def salvar_disciplinas(arquivo_json, dados):
    with open(arquivo_json, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

# carrega nome do arquivo
def carregar_nome_json(nome_arquivo):
    config = configparser.ConfigParser()

    atualizar_config(nome_arquivo)

    # Carrega o arquivo config.ini
    config.read(nome_arquivo)
    
    ano = config['SUAP']['ano']
    periodo = config['SUAP']['periodo']
    if str(ano) == "" or str(periodo) == "":
        exit(f"Erro ao carregar nome do arquivo json. Verifique o ano e período letivos")

    return f"disciplinas_sem_nota_{ano}.{periodo}.json"

# Função para baixar e salvar a foto do professor
def baixar_foto_professor(url_foto, nome_professor):
    resposta_foto = requests.get(url_foto)
    if resposta_foto.status_code == 200:
        nome_arquivo = f"{nome_professor.replace(' ', '_')}.jpg"
        with open(nome_arquivo, 'wb') as img_file:
            img_file.write(resposta_foto.content)
    else:
        print(f"Erro ao baixar a foto de {nome_professor}. Status: {resposta_foto.status_code}")

# cria ou salva arquivo de configuração    
def atualizar_config(nome_arquivo, matricula ="", senha="", ano="", periodo="", data_ini=""):
    # Carrega o arquivo de configuração
    config = configparser.ConfigParser()
    
    if not os.path.exists(nome_arquivo):
        config['SUAP'] = {
            'matricula': str(matricula),
            'senha': str(senha),
            'ano': str(ano),
            'periodo': str(periodo),
            'dataini': str(data_ini)
        }

        # Pede dados de login se não estiverem configurados
        if (matricula == "" or senha == ""):
            matricula = input("digite sua matricula do SUAP\n")
            senha = getpass.getpass("Digite sua senha do SUAP\n")
        
        # Pede o ano letivo e periodo letivo ao usuário se não tiver configurado
        if ano == "" or periodo == "":
            ano_periodo = input("Digite o ano e periodo letivo para ver o boletim (formato: 2023.2)\n")    
            ano, periodo = map(int, ano_periodo.split("."))

        # Pede data inicial se não estiver configurada
        while True:
            try:
                datetime.strptime(data_ini, '%d/%m/%Y')
                break
            except:            
                data_ini = input("digite a data inicial de contagem de dias (dd/mm/aaaa)\n")
    
    config.read(nome_arquivo)

    config['SUAP']['matricula'] = str(matricula) if str(matricula) != "" else config['SUAP']['matricula']
    config['SUAP']['senha']     = str(senha)     if str(senha)     != "" else config['SUAP']['senha'] 
    config['SUAP']['ano']       = str(ano)       if str(ano)       != "" else config['SUAP']['ano'] 
    config['SUAP']['periodo']   = str(periodo)   if str(periodo)   != "" else config['SUAP']['periodo']
    config['SUAP']['dataini']   = str(data_ini)  if str(data_ini)  != "" else config['SUAP']['dataini']

    # Salva as alterações de volta no arquivo
    with open(nome_arquivo, 'w', encoding='utf-8') as configfile:
        config.write(configfile, space_around_delimiters=False)

def pegar_ano_periodo():
     # Cria um objeto ConfigParser
    config = configparser.ConfigParser()
    
    # Verifica se o arquivo de configuração existe, se não, cria um com valores vazios
    nome_arquivo = 'config.ini'

    # Carrega o arquivo config.ini
    config.read(nome_arquivo)

    return  config['SUAP']['ano'] + "." + config['SUAP']['periodo']


# Acessa API do SUAP com os dados da configuração e salva e exibe os dados das disciplinas
def pegar_atrasados():    
    # Cria um objeto ConfigParser
    config = configparser.ConfigParser()
    
    # Verifica se o arquivo de configuração existe, se não, cria um com valores vazios
    nome_arquivo = 'config.ini'
    #if not os.path.exists(nome_arquivo):
    atualizar_config(nome_arquivo)

    # Carrega o arquivo config.ini
    config.read(nome_arquivo)

    # Obtem os dados do arquivo de configuração
    matricula = config['SUAP']['matricula']
    senha = config['SUAP']['senha']
    ano_letivo = config['SUAP']['ano']
    periodo_letivo = config['SUAP']['periodo']
    data_ini = config['SUAP']['dataini']

    # URL de autenticação do SUAP
    url = "https://suap.ifrn.edu.br/api/token/pair"
    token_access = ""
    token_refresh = ""

    # Dados de login
    dados_login = {
        "username": f"{matricula}",
        "password": f"{senha}"
    }

    # Fazendo o POST para obter o token
    resposta_authenticacao = requests.post(url, json=dados_login)

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
        url_dados = "https://suap.ifrn.edu.br/api/rh/meus-dados/"
        responsta_meus_dados = requests.get(url_dados, headers=cabecalho)
        
        # respostas da requisição 
        if responsta_meus_dados.status_code == 200:
            meus_dados = responsta_meus_dados.json()
            print(f"{meus_dados['nome_usual']} - {meus_dados['vinculo']['curso']}")
        else:
            print("Falha ao obter os dados:", responsta_meus_dados.status_code)               

        # URL do boletim com o ano e periodo letivo
        url_boletim = f"https://suap.ifrn.edu.br/api/edu/meu-boletim/{ano_letivo}/{periodo_letivo}"

        # Requisição GET para buscar o boletim
        responsta_boletim = requests.get(url_boletim, headers=cabecalho)

        if responsta_boletim.status_code == 200:
            boletim = responsta_boletim.json()        

            data_inicial = datetime.strptime(data_ini, '%d/%m/%Y')  # Converter a string da data inicial
            data_atual = datetime.now()  # Obter a data atual
            dias_sem_nota = (data_atual - data_inicial).days  # Calcular a diferença em dias  

            # Carregar disciplinas do arquivo JSON, se existir
            arquivo_json = carregar_nome_json(nome_arquivo)
            disciplinas_sem_nota = carregar_disciplinas(arquivo_json)
            
            for disciplina in boletim:
                   
                #if not disciplina['media_final_disciplina']:
                nome_disciplina = disciplina['disciplina']                                                                         
                
                # URL da turma vitual com id    
                url_turma_vitual = f"https://suap.ifrn.edu.br/api/edu/minha-turma-virtual/{disciplina['codigo_diario']}/"
                    
                # Requisição GET para buscar turma vitual
                resposta_turma_virtual = requests.get(url_turma_vitual, headers=cabecalho)
                    
                if resposta_turma_virtual.status_code == 200:
                    turma_virtual = resposta_turma_virtual.json()
                    nome_professor = turma_virtual["professores"][0]["nome"]    
                    url_foto_professor = turma_virtual["professores"][0]["foto"]   

                    # Adiciona e atualiza a disciplina no dicionário
                    disciplinas_sem_nota[nome_disciplina] = {
                        "dias": dias_sem_nota if not disciplina['media_final_disciplina'] else 0,
                        "professor": nome_professor,
                        "disciplina": nome_disciplina,
                        "ano": ano_letivo,
                        "periodo" : periodo_letivo
                    }                                                           
                        
                    # Baixar e salvar a foto do professor
                    if not os.path.exists(f"{nome_professor.replace(' ', '_')}.jpg"):
                        baixar_foto_professor(url_foto_professor, nome_professor)
                else:
                    exit(f"Falha ao obter minhas turmas. Status: {resposta_turma_virtual.status_code} - Verifique ano e período letivo")                                    

            # Salva as disciplinas atualizadas no arquivo JSON
            salvar_disciplinas(arquivo_json, disciplinas_sem_nota)

            # Encerra se não houverem atrasos
            if len(disciplinas_sem_nota.items()) == 0:
                exit(f"Não existem disciplinas sem nota em {ano_letivo}.{periodo_letivo}.")
            
            # Lista disciplinas sem notas do ano e período consultados
            print(f"Disciplinas que ainda não receberam notas em {ano_letivo}.{periodo_letivo}:")        
            for nome_disciplina, dados_disciplina in disciplinas_sem_nota.items():
                if ((str(dados_disciplina['ano']) == str(ano_letivo)) and str((dados_disciplina['periodo']) == str(periodo_letivo))):
                    print(f"- dias: {dados_disciplina['dias']} - {dados_disciplina['professor']} - {nome_disciplina}") 
           
            # salva as informações no config.ini  
            atualizar_config(nome_arquivo, matricula,senha,ano_letivo,periodo_letivo,data_ini)

        else:
            exit(f"Falha ao obter o boletim. Status: {responsta_boletim.status_code} - Verifique ano e período letivo")            
            
    else:
        exit(f"Falha na autenticação. Status: {resposta_authenticacao.status_code} - Verifique o usuário e senha")
