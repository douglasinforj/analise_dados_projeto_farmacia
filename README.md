# Analise Dados Projeto Farmácia

## Descrição

## Recursos do projeto

### Banco de dados Mysql

 - Acessando banco de dados mysql, vamos criar o banco de tabelas do projeto

```
CREATE DATABASE farmacia;

USE farmacia;

-- Tabela de Produtos
CREATE TABLE produtos (
    produto_id INT AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(255) NOT NULL,
    preco_custo DECIMAL(10, 2),
    preco_venda DECIMAL(10, 2),
    categoria VARCHAR(100)
);

-- Tabela de Vendedores
CREATE TABLE vendedores (
    vendedor_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    regiao VARCHAR(100)
);

-- Tabela de Clientes
CREATE TABLE clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255),
    idade INT,
    genero VARCHAR(50),
    endereco TEXT,
    telefone VARCHAR(50),
    cep VARCHAR(10),
    data_registro DATE
);

-- Tabela de Vendas
CREATE TABLE vendas (
    venda_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    vendedor_id INT,
    produto_id INT,
    quantidade INT,
    preco_unitario DECIMAL(10, 2),
    total_venda DECIMAL(10, 2),
    data_venda DATE,
    metodo_pagamento VARCHAR(50),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id),
    FOREIGN KEY (vendedor_id) REFERENCES vendedores(vendedor_id),
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
);

```

### Arquivos ficticios de dados para o projeto (Download dos Dados)
Você pode baixar o arquivo de dados diretamente através do link abaixo:
 - [📂 Baixar clientes.csv](https://github.com/douglasinforj/analise_dados_projeto_farmacia/raw/main/data/clientes.csv)
 - [📂 Baixar produtos.csv](https://github.com/douglasinforj/analise_dados_projeto_farmacia/raw/main/data/produtos.csv)
 - [📂 Baixar vendas.csv](https://github.com/douglasinforj/analise_dados_projeto_farmacia/raw/main/data/vendas.csv)
 - [📂 Baixar vendedores.csv](https://github.com/douglasinforj/analise_dados_projeto_farmacia/raw/main/data/vendedores.csv)

### Importar os arquivos para o banco de dados

### No terminal na pasta do projeto
```
python -m venv venv   #criando ambiente virtual
cd venv/Scripts/activate

pip install mysql-connector-python  # conexão com o mysql
pip install pandas
```

### Script para importação de dados
- Criar uma arquivo com nome importacao.py na raiz do projeto.
```
import os
import pandas as pd
import mysql.connector

# Conectar ao banco de dados MySQL
connection = mysql.connector.connect(
    host='localhost',        # ou o host do seu servidor MySQL
    user='root',             # seu usuário
    password='admin',        # sua senha
    database='farmacia',     # nome do banco de dados
    charset="utf8mb4"
)

cursor = connection.cursor()

# Arquivos CSV a serem carregados
files = ['data/produtos.csv', 'data/vendedores.csv', 'data/clientes.csv', 'data/vendas.csv']

# Verificar se os arquivos existem
for file in files:
    if os.path.exists(file):
        print(f"Arquivo encontrado: {file}")
    else:
        print(f"Arquivo não encontrado: {file}")

# Carregar os arquivos CSV em DataFrames
df_produtos = pd.read_csv('data/produtos.csv')
df_vendedores = pd.read_csv('data/vendedores.csv')
df_clientes = pd.read_csv('data/clientes.csv')
df_vendas = pd.read_csv('data/vendas.csv')

# Função para escapar caracteres especiais (ex: aspas simples)
def escape_string(value):
    return value.replace("'", "\\'") if isinstance(value, str) else value

# Função para inserir dados nas tabelas
def insert_data(table, data):
    for i, row in data.iterrows():
        columns = ', '.join(data.columns)
        values = ', '.join([f"'{escape_string(x)}'" if isinstance(x, str) else str(x) for x in row])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        try:
            cursor.execute(sql)
        except mysql.connector.Error as err:
            print(f"Erro ao inserir dados na tabela {table}: {err}")
            print(f"SQL executado: {sql}")

# Inserir dados na tabela de produtos
for i, row in df_produtos.iterrows():
    produto = escape_string(row['produto'])
    preco_custo = row['preco_custo']
    preco_venda = row['preco_venda']
    categoria = escape_string(row['categoria'])
    
    sql = f"INSERT INTO produtos (produto, preco_custo, preco_venda, categoria) VALUES ('{produto}', {preco_custo}, {preco_venda}, '{categoria}')"
    cursor.execute(sql)

# Inserir dados na tabela de vendedores
for i, row in df_vendedores.iterrows():
    vendedor_id = row['vendedor_id']
    nome = escape_string(row['nome'])
    regiao = escape_string(row['regiao'])
    
    sql = f"INSERT INTO vendedores (vendedor_id, nome, regiao) VALUES ({vendedor_id}, '{nome}', '{regiao}')"
    cursor.execute(sql)

# Inserir dados na tabela de clientes
for i, row in df_clientes.iterrows():
    cliente_id = row['cliente_id']
    nome = escape_string(row['nome'])
    idade = row['idade']
    genero = escape_string(row['genero'])
    endereco = escape_string(row['endereco'])
    telefone = escape_string(row['telefone'])
    cep = row['cep']
    data_registro = row['data_registro']
    
    sql = f"INSERT INTO clientes (cliente_id, nome, idade, genero, endereco, telefone, cep, data_registro) VALUES ({cliente_id}, '{nome}', {idade}, '{genero}', '{endereco}', '{telefone}', '{cep}', '{data_registro}')"
    cursor.execute(sql)

# Inserir dados na tabela de vendas
for i, row in df_vendas.iterrows():
    venda_id = row['venda_id']
    cliente_id = row['cliente_id']
    vendedor_id = row['vendedor_id']
    produto = escape_string(row['produto'])
    quantidade = row['quantidade']
    preco_unitario = row['preco_unitario']
    total_venda = row['total_venda']
    data_venda = row['data_venda']
    metodo_pagamento = escape_string(row['metodo_pagamento'])
    
    # Obter o produto_id correspondente ao nome do produto
    cursor.execute(f"SELECT produto_id FROM produtos WHERE produto = '{produto}'")
    produto_id = cursor.fetchone()
    
    if produto_id:
        produto_id = produto_id[0]
        
        sql = f"INSERT INTO vendas (venda_id, cliente_id, vendedor_id, produto_id, quantidade, preco_unitario, total_venda, data_venda, metodo_pagamento) VALUES ({venda_id}, {cliente_id}, {vendedor_id}, {produto_id}, {quantidade}, {preco_unitario}, {total_venda}, '{data_venda}', '{metodo_pagamento}')"
        cursor.execute(sql)
    else:
        print(f"Produto {produto} não encontrado para venda_id {venda_id}")

# Confirmar e fechar a conexão
connection.commit()
cursor.close()
connection.close()

print("Dados importados com sucesso!")


```