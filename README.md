# Fórmula cadê minha nota

Este projeto tem como objetivo ~~tirar sarro com o atraso no lançamento de notas finais das disciplinas na plataforma SUAP.~~ estudar requisições http e manipulação de imagens com bibliotecas python.

### Instruções:

1. **Instale as dependências do arquivo requirements.txt**: Serão necessárias duas bibliotecas: Pillow Para manipulação de imagens. Requests para efetuar as requisições http para a API do SUAP. Para instalar execute no terminal:
   ```
   pip install -r requirements.txt
   ```

2. **Preencha o arquivo config.ini**: Coloque seus dados no arquivo de configuração como **matrícula** e **senha** do SUAP, **ano** e **período** letivos e **data inicial** de contagem do atraso do lançamento das notas. 

   ***Atente para que seus dados permaneçam no seu ambiente local. Tome cuidado par que suas informações de login no SUAPnão se tornem públicas. Lembre de manter seus dados em sigilo.***

3. **Executar o programa**: Execute o comando no terminal.
   ```
   python run.py
   ```
   Será aberta uma janela com a `foto` do professor de cada professor, `barra de progresso` de cada disciplina, `número de dias` de atraso por disciplina.

4. **Encerrar o programa**: Basta fechar a janela que foi aberta. Ou digite `Ctrl + C` no terminal. 

5. **Resultados**: No terminal haverá a seguinte estrutura:
   ```
   Login bem sucedido.
   NOME_USUAL - CURSO
   Disciplinas que ainda não receberam notas em ANO.PERIODO:
   - Dias: Número de dias  de atraso - Nome do professor - Curso
   - Dias: Número de dias  de atraso - Nome do professor - Curso
   - Dias: Número de dias  de atraso - Nome do professor - Curso
   ```
   
6. **Coletando dados**: Execute o programa **diariamente** para que os dados sejam coletados e as barras de progresso aumentem. 

### Arquivos:

- **login.py**: Responsável por acessar os dados da API do SUAP e armazená-los num arquivo json.
- **run.py**: Vai montar e abrir uma janela com as fotos dos professores e barra de progresso representando os dias de atraso para lançamento das notas de cada disciplina.
- **config.ini**: Arquivo que contém as configurações do programa login.py.
- **requirements.txt**: Arquivo que contém as bibliotecas necessárias para a execução dos programas login.py e run.py.

### Artefatos a serem gerados:
- **disciplinas_sem_notas.json**: Arquivo que contém os dados das disciplinas com atraso de lançamento de notas finais.
- **Nome_Sobrenome.jpg**: Imagens das fotos dos professores das disciplinas com atraso no lançamento das notas.


