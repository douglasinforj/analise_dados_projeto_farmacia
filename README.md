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
```