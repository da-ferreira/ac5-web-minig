### Integrantes
Integrantes
David Ferreira de Almeida - 1904024
Matheus de Jesus Oliveira - 1903603
Pedro Henrique Oliveira Dantas Lopes - 1904007
Rafael Serino Kiss - 1903107
Thiago Souza do Amparo - 1904089

### Como rodar o projeto

Para rodar o projeto, é necessário ter o python instalado.

### 1. Rode o seguinte comando para executar o ambiente virtual:
```
python -m venv venv
```

### 2. Rode o seguinte comando para ativar o ambiente virtual:
```
venv\Scripts\activate
```

### 3. Rode o seguinte comando para instalar as dependências (estando na raiz do projeto):
```
pip install -r requirements.txt
```

### 4. Rodando o scrapping e salvando no banco de dados:
Obs: O banco de dados já está populado, então não é necessário rodar o scrapping novamente. Apenas se quiser atualizar os dados.
Rode o arquivo : `dataScraper.ipynb`. Rode todas as células do notebook.

### 5. Rodando a aplicação (estando na raiz do projeto):
```
cd scripts
python .\app.py
```
