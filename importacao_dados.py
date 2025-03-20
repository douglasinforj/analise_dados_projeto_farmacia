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
