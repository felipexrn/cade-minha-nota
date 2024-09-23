import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import json
import login

# Função para criar a barra de progresso com texto sobreposto
def criar_barras(atrasados):
    global largura_total  # Usa uma variável global para calcular a largura total
    
    # Define o tamanho da barra
    tamanho_barra = 300      
    max_dias = 0
    for atrasado in atrasados:
        max_dias = max(max_dias, atrasados[atrasado]['dias'])
    proporcao = 1.1 * (max_dias +1)

    for atrasado in atrasados:
        # Cria um frame para cada barra
        frame = tk.Frame(root)
        frame.pack(pady=5, anchor='w')
        
        # Carrega a imagem do professor
        img = Image.open(f"{atrasados[atrasado]['professor'].replace(' ', '_')}.jpg")
        img = img.resize((30, 40), Image.LANCZOS)  # Redimensiona a imagem
        foto = ImageTk.PhotoImage(img)

        # Exibe a imagem
        label_img = tk.Label(frame, image=foto)
        label_img.image = foto
        label_img.pack(side=tk.LEFT, padx=10)

        # Cria um canvas para colocar a barra de progresso
        canvas = tk.Canvas(frame, width=tamanho_barra, height=30)
        canvas.pack(side=tk.BOTTOM, padx=10)

        # Desenha a barra de progresso no canvas
        canvas.create_rectangle(0, 0, tamanho_barra, 30, outline="", fill="gray")
        canvas.create_rectangle(0, 0, int(tamanho_barra * (atrasados[atrasado]['dias'] / proporcao)), 30, outline="", fill="green")

        # Exibe o valor (dias) sobre a barra de progresso
        canvas.create_text(tamanho_barra // 2, 15, text=f"{atrasados[atrasado]['dias']} dias", fill="white", font=("Arial", 12))
        
        # Exibe o nome da disciplina
        label_disciplina = tk.Label(frame, text=f"{atrasados[atrasado]['disciplina']}".split(" - ")[1])
        label_disciplina.pack(side=tk.TOP, padx=10, anchor='w')

        # Calcula a largura total
        largura_total = max(largura_total, 10 + 30 + tamanho_barra + 50)

# Função para carregar o dicionário de atrasados do arquivo JSON
def carregar_dados_json(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)

# Cria a janela principal
root = tk.Tk()
root.title("Fómula cadê minha nota")

# Inicializa dimensões gerais
largura_total = 0 
altura_total = 400 
altura_frame = 50

# Conecta ao SUAP e recupera os dados
login.pegar_atrasados()

# Nome do arquivo JSON com os dados dos professores
arquivo_json = 'disciplinas_sem_nota.json'

# Carrega os dados de atraso do arquivo JSON
atrasados = carregar_dados_json(arquivo_json)

# Cria as barras de progresso
criar_barras(atrasados)

# Calcular a altura total
altura_total = len(atrasados) * altura_frame + 50  # 50 pixels por disciplina + padding

# Define o tamanho da janela
root.geometry(f"{largura_total}x{altura_total}")

# Inicia o loop da interface gráfica
root.mainloop()
