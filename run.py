from PIL import Image, ImageDraw, ImageFont
import json
import login

# Função para criar a imagem com as barras de progresso e textos
def criar_imagem(atrasados, nome_arquivo_imagem):
    largura_total = 0  # Variável para calcular a largura total da imagem
    altura_total = 0  # Altura inicial da imagem
    altura_frame = 60  # Altura de cada "barra" com texto
    espacamento = 10  # Espaçamento entre as barras
    margem_superior = 10
    margem_inferior = 10
    tamanho_fonte_titulo = 13
    padding_titulo = 30
    tamanho_fonte = 12
    
    # Define o tamanho da imagem (inicialmente)
    tamanho_barra = 400
    max_dias = 0
    for atrasado in atrasados:
        max_dias = max(max_dias, atrasados[atrasado]['dias'])
    proporcao = 1.1 * (max_dias + 1)
    
    # Calcular a largura total e altura total da imagem
    for atrasado in atrasados:
        largura_total = max(largura_total, 10 + 30 + tamanho_barra + 25)
        altura_total += (altura_frame + espacamento)
    
    altura_total += margem_superior + tamanho_fonte_titulo + margem_inferior
    
    # Cria uma nova imagem em branco (fundo branco)
    imagem = Image.new('RGB', (largura_total, altura_total), (255, 255, 255))
    draw = ImageDraw.Draw(imagem)
    
    # Definir uma fonte para o texto (você pode mudar o caminho ou a fonte)
    try:
        fonte_titulo = ImageFont.truetype("arialbd.ttf", tamanho_fonte_titulo)  # Tente usar a fonte Arial
        fonte = ImageFont.truetype("arialbd.ttf", tamanho_fonte)  # Tente usar a fonte Arial
    except IOError:
        fonte_titulo = ImageFont.load_default()  # Se a fonte não for encontrada, usa a fonte padrão
        fonte = ImageFont.load_default()  # Se a fonte não for encontrada, usa a fonte padrão
    
    y_offset = margem_superior  # Offset vertical para posicionar os elementos

    # Desenha o título na imagem
    titulo = "Dias de atraso para postagem da média final do periodo " + login.pegar_ano_periodo()
    draw.text(((largura_total-(len(titulo)*tamanho_fonte_titulo/2))//2, y_offset), titulo, font=fonte_titulo, fill=(0, 0, 0))
    y_offset += padding_titulo  # Ajusta a posição para o próximo elemento

    for atrasado in atrasados:
        # Calcula a posição de cada elemento
        y_pos = y_offset
        # Carrega a imagem do professor
        try:
            img_professor = Image.open(f"{atrasados[atrasado]['professor'].replace(' ', '_')}.jpg")
        except:
            img_professor = Image.new('RGB', (38, 50), (200, 200, 200))  # Se a imagem não for encontrada, cria uma imagem vazia
        img_professor = img_professor.resize((38, 50), Image.LANCZOS)
        
        # Coloca a imagem do professor na imagem principal
        imagem.paste(img_professor, (10, y_pos))
        
        # Desenha o nome da disciplina acima da barra de progresso
        draw.text((55, y_pos), f"{atrasados[atrasado]['disciplina']}".split(" - ")[1], font=fonte, fill=(0, 0, 0))
        
        # Desenha a barra de progresso abaixo do nome da disciplina
        draw.rectangle([55, y_pos + 20, 55 + tamanho_barra, y_pos + 50], outline="darkgrey", fill="gray")
        progresso = int(tamanho_barra * (atrasados[atrasado]['dias'] / proporcao))
        draw.rectangle([55, y_pos + 20, 55 + progresso, y_pos + 50], outline="darkgrey", fill="green")
        
        # Escreve o texto sobre a barra de progresso
        draw.text((55 + tamanho_barra // 2 - 20, y_pos + 30), f"{atrasados[atrasado]['dias']} dias", font=fonte, fill=(255, 255, 255))
        
        # Atualiza o offset
        y_offset += altura_frame + espacamento  # Ajusta a posição para o próximo

    # Salva a imagem no disco
    imagem.save(nome_arquivo_imagem)

# Função para carregar o dicionário de atrasados do arquivo JSON
def carregar_dados_json(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    
    # Ordenar os atrasados pela quantidade de dias
    return dict(sorted(dados.items(), key=lambda item: item[1]['dias'], reverse=True))

# Conecta ao SUAP e recupera os dados
login.pegar_atrasados()

# Nome do arquivo JSON com os dados dos professores
nome_arquivo = "config.ini"
login.atualizar_config(nome_arquivo)
arquivo_json = login.carregar_nome_json(nome_arquivo)

# Carrega os dados de atraso do arquivo JSON
atrasados = carregar_dados_json(arquivo_json)

# Nome do arquivo da imagem gerada
nome_arquivo_imagem = f"relatorio_atrasos_{login.pegar_ano_periodo()}.png"

# Cria a imagem com as barras de progresso
criar_imagem(atrasados, nome_arquivo_imagem)

print(f"A imagem foi salva como '{nome_arquivo_imagem}'.")
