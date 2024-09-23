# Fórmula cadê minha nota

Este projeto tem como objetivo ~~tirar sarro do atraso no lançamento de notas finais das disciplinas na plataforma SUAP.~~ estudar requisições http e manipulação de imagens com bibliotecas python.

## Instruções:

### 1. Instale as dependências do arquivo requirements.txt 
   Serão necessárias duas bibliotecas: Pillow Para manipulação de imagens. Requests para efetuar as requisições http para a API do SUAP. Para instalar execute no terminal:
   ```
   pip install -r requirements.txt
   ```

### 2. Preencha o arquivo config.ini
   Coloque seus dados no arquivo de configuração como **matrícula** e **senha** do SUAP, **ano** e **período** letivos e **data inicial** de contagem do atraso do lançamento das notas. Exemplo:
   ```
   [SUAP]
   MATRICULA=20152010567
   SENHA=0123456789
   ANO=2024
   PERIODO=1
   DATAINI=20/09/2024
   ```

   ***Atente para que seus dados permaneçam no seu ambiente local. Tome cuidado par que suas informações de login no SUAP não se tornem públicas. Lembre de manter seus dados em sigilo.***

### 3. Execução do programa
Execute o seguinte comando no terminal.
   ```
   python run.py
   ```

### 4. Resultados
   Será aberta uma janela com a `foto` do professor de cada disciplina, `barra de progresso` verde e cinza, `número de dias` de atraso por disciplina e nome da disciplina. Já no terminal haverá a seguinte estrutura:
   ```
   Login bem sucedido.
   NOME_USUAL - CURSO
   Disciplinas que ainda não receberam notas em ANO.PERIODO:
   - Dias: NÚMERO_DIAS_ATRASO - NOME_PROFESSOR - NOME_DISCIPLINA
   - Dias: NÚMERO_DIAS_ATRASO - NOME_PROFESSOR - NOME_DISCIPLINA
   - Dias: NÚMERO_DIAS_ATRASO - NOME_PROFESSOR - NOME_DISCIPLINA
   - ... N linhas para cada disciplina sem a nota final lançada no SUAP
   ```
   - **NOME_USUAL**: Nome usual cadastrado no SUAP.
   - **CURSO**: Curso em andamento.
   - **ANO**: Ano configurado no arquivo config.ini.
   - **PERIODO**: Período configurado no arquivo config.ini.
   - **NÚMERO_DIAS_ATRASO**: Quantidade de dias entre a data incial configurada no arquivo config.ini até a data de lançamento da nota final no SUAP ou até a data de hoje.
   - **NOME_PROFESSOR**: Nome do primeiro professor da disciplina (caso tenha mais de um) com atraso no lançamento da nota final no SUAP. 
   - **NOME_DISCIPLINA**: Código e nome da disciplina com atraso no lançamento da nota final no SUAP. 
   
### 5. Encerramento do programa
   Basta fechar a janela que foi aberta. Ou digite `Ctrl + C` no terminal. 
   
### 6. Coletando dados
   Execute o programa **diariamente** para que os dados sejam coletados e as barras de progresso aumentem. 

## Arquivos:

- **login.py**: Responsável por acessar os dados da API do SUAP e armazená-los num arquivo json.
- **run.py**: Responsável por montar e exibir uma janela com as fotos dos professores e barras de progresso representando os dias de atraso para lançamento das notas de cada disciplina.
- **config.ini**: Arquivo que contém as configurações do programa login.py.
- **requirements.txt**: Arquivo que contém as bibliotecas necessárias para a execução dos programas login.py e run.py.

## Artefatos a serem gerados:
- **disciplinas_sem_notas.json**: Arquivo que contém os dados das disciplinas com atraso de lançamento de notas finais.
- **Nome_Sobrenome.jpg**: Imagens das fotos dos professores das disciplinas com atraso no lançamento das notas.


