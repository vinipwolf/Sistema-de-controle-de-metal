CREATE TABLE estoque (
    id_estoque SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    quantidade NUMERIC(12,3) NOT NULL,
    unidade VARCHAR(30) NOT NULL
);


CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    credito NUMERIC(12,2) NOT NULL DEFAULT 0
);


CREATE TABLE distribuidor (
    id_distribuidor SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    saldo_metal NUMERIC(12,3) NOT NULL DEFAULT 0,
    saldo_dinheiro NUMERIC(12,2) NOT NULL DEFAULT 0
);


CREATE TABLE pedido_venda (
    id_venda SERIAL PRIMARY KEY,
    dia DATE NOT NULL,
    quantidade NUMERIC(12,3) NOT NULL,
    cotacao NUMERIC(12,2) NOT NULL,
    total_rs NUMERIC(12,2) NOT NULL,

    id_cliente INT NOT NULL,
    id_estoque INT NOT NULL,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    FOREIGN KEY (id_estoque)
        REFERENCES estoque(id_estoque)
);


CREATE TABLE pagamento_clientes (
    id_pagamento_cliente SERIAL PRIMARY KEY,
    valor NUMERIC(12,2) NOT NULL,
    dia DATE NOT NULL,
    forma_pagamento VARCHAR(30) NOT NULL,

    id_cliente INT NOT NULL,
    id_estoque INT NOT NULL,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente),

    FOREIGN KEY (id_estoque)
        REFERENCES estoque(id_estoque)
);


CREATE TABLE pedido_compra (
    id_compra SERIAL PRIMARY KEY,
    cotacao NUMERIC(12,2) NOT NULL,
    dia DATE NOT NULL,
    quantidade NUMERIC(12,3) NOT NULL,
    total_rs NUMERIC(12,2) NOT NULL,

    id_distribuidor INT NOT NULL,

    FOREIGN KEY (id_distribuidor)
        REFERENCES distribuidor(id_distribuidor)
);


CREATE TABLE retirada_metal (
    id_retirada SERIAL PRIMARY KEY,
    quantidade NUMERIC(12,3) NOT NULL,
    dia DATE NOT NULL,

    id_compra INT NOT NULL,
    id_estoque INT NOT NULL,

    FOREIGN KEY (id_compra)
        REFERENCES pedido_compra(id_compra),

    FOREIGN KEY (id_estoque)
        REFERENCES estoque(id_estoque)
);


CREATE TABLE pagamento_distribuidor (
    id_pagamentodist SERIAL PRIMARY KEY,
    valor NUMERIC(12,2) NOT NULL,
    dia DATE NOT NULL,
    forma_pagamento VARCHAR(30) NOT NULL,

    id_distribuidor INT NOT NULL,
    id_estoque INT NOT NULL,

    FOREIGN KEY (id_distribuidor)
        REFERENCES distribuidor(id_distribuidor),

    FOREIGN KEY (id_estoque)
        REFERENCES estoque(id_estoque)
);