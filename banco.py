import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

def conectar():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def consultar_estoque():

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT nome, quantidade, unidade FROM Estoque")

        estoque = cursor.fetchall()

        cursor.close()
        conexao.close()

        return estoque

    except Exception as erro:
        print("Erro ao consultar clientes:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def registrar_venda(id_cliente, quantidade, cotacao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            return

        if cotacao <= 0:
            print("A cotação deve ser maior que zero.")
            return
        
        cursor.execute(
            """
            SELECT id_cliente
            FROM Clientes
            WHERE id_cliente = %s
            """,
            (id_cliente,)
        )
        cliente = cursor.fetchone()

        if cliente is None:
            print("Cliente não encontrado!")
            return

        cursor.execute(
            """
            SELECT quantidade
            FROM Estoque
            WHERE nome = 'ouro'
            """
        )

        estoque_ouro = cursor.fetchone()

        if estoque_ouro is None:
            print("Não tem ouro no estoque!")
            return

        quantidade_disponivel = estoque_ouro[0]

        if quantidade_disponivel < quantidade:
            print("Estoque insuficiente!")
            print(f"Quantidade disponível: {quantidade_disponivel} g")
            return

        total = cotacao * quantidade
        cursor.execute(
            """
            INSERT INTO pedido_venda(dia, quantidade, cotacao, total_rs, id_cliente, id_estoque)
            VALUES (CURRENT_DATE, %s, %s, %s, %s, 1)
            """,
            (quantidade, cotacao, total, id_cliente)
        )
        cursor.execute(
            """
            UPDATE Estoque
            SET quantidade = quantidade - %s
            WHERE id_estoque = 1
            """,
            (quantidade,)
        )
        cursor.execute(
            """
            UPDATE Clientes
            SET credito = credito + %s
            WHERE id_cliente = %s
            """,
            (total, id_cliente)
        )

        conexao.commit()

        return total

    except Exception as erro:
        conexao.rollback()
        print("Erro ao registrar venda:", erro)

    finally:
        cursor.close()
        conexao.close()

def registrar_pagamento_cliente(id_cliente, valor, forma_pagamento):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if valor <= 0:
            print("Valor inválido")
            return False
        
        cursor.execute(
            """
            SELECT credito
            FROM Clientes
            WHERE id_cliente = %s
            """,
            (id_cliente,)
        )
        
        cliente = cursor.fetchone()

        if cliente == None:
            print("Cliente não encontrado")
            return False

        credito_atual = cliente[0]

        if credito_atual < valor:
            print("O pagamento é maior que o crédito do cliente")
            print(f"Credito atual: {credito_atual}")
            return False

        if forma_pagamento.lower() == "cheque":
            tipo_estoque = "cheque"
        else:
            tipo_estoque = "dinheiro"

        cursor.execute(
            """
            SELECT id_estoque
            FROM Estoque
            WHERE nome = %s
            """,
            (tipo_estoque,)
        )

        estoque_dinheiro = cursor.fetchone()

        if estoque_dinheiro is None:
            ("ID do estoque não encontrado")
            return False

        id_estoque = estoque_dinheiro[0]

        cursor.execute(
            """
            INSERT INTO Pagamento_clientes (valor, dia, forma_pagamento, id_cliente, id_estoque)
            VALUES (%s, CURRENT_DATE, %s, %s, %s)
            """,
            (valor, forma_pagamento, id_cliente, id_estoque)
        )

        cursor.execute(
            """
            UPDATE Clientes
            SET credito = credito - %s
            WHERE id_cliente = %s
            """,
            (valor, id_cliente)
        )

        if forma_pagamento.lower() == "cheque":
            tipo_estoque = "cheque"
        else:
            tipo_estoque = "dinheiro"


        cursor.execute(
            """
            UPDATE Estoque
            SET quantidade = quantidade + %s
            WHERE nome = %s
            """,
            (valor, tipo_estoque)
        )

        conexao.commit()

        return True
    
    except Exception as erro:
        conexao.rollback()
        print("Erro ao registrar pagamento:", erro)
        return False
        

    finally:
        cursor.close()
        conexao.close()

def registrar_compra(id_distribuidor, quantidade, cotacao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if quantidade <= 0:
            print("Quantidade Invalida")
            return None
        if cotacao <= 0:
            print("Cotacao Invalida")
            return None

        cursor.execute(
        """
        SELECT id_distribuidor
        FROM Distribuidor
        WHERE id_distribuidor = %s
        """,
        (id_distribuidor,)
        )
        distribuidor = cursor.fetchone()

        if distribuidor == None:
            print("Distribuidor não encontrado")
            return None

        total = cotacao * quantidade

        cursor.execute(
            """
            INSERT INTO Pedido_compra (quantidade, cotacao, dia, total_rs, id_distribuidor)
            VALUES (%s, %s, CURRENT_DATE, %s, %s)
            """,
            (quantidade, cotacao, total, id_distribuidor)
        )
        cursor.execute(
            """
            UPDATE Distribuidor 
            SET saldo_dinheiro = saldo_dinheiro + %s
            WHERE id_distribuidor = %s
            """,
            (total, id_distribuidor)
        )

        conexao.commit()

        return total

    except Exception as erro:
        conexao.rollback()
        print("Erro ao registrar compra:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()

def registrar_retirada_metal(id_compra, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    try:    
        if quantidade <= 0:
            print("Quantidade Invalida")
            return None, None, False

        cursor.execute(
            """
            SELECT quantidade
            FROM Pedido_compra
            WHERE id_compra = %s
            """,
            (id_compra,)
        )

        compra = cursor.fetchone()

        if compra == None:
            print("Pedido de compra não encontrado")
            return None, None, False

        quantidade_compra = compra[0]

        cursor.execute(
            """
            SELECT COALESCE(SUM(quantidade), 0)
            FROM Retirada_metal
            WHERE id_compra = %s
            """,
            (id_compra,)
        )

        resultado = cursor.fetchone()
        quantidade_retirada = resultado[0]

        quantidade_restante = quantidade_compra - quantidade_retirada

        if quantidade > quantidade_restante:
            print("Quantidade maior que o saldo disponível para retirada.")
            print(f"Quantidade comprada: {quantidade_compra} g")
            print(f"Já retirado: {quantidade_retirada} g")
            print(f"Disponível para retirada: {quantidade_restante} g")
            return None, None, False

        cursor.execute(
            """
            SELECT id_estoque
            FROM Estoque
            WHERE nome = 'ouro'
            """
        )

        estoque = cursor.fetchone()

        if estoque is None:
            print("Estoque não encontrado")
            return None, None, False

        id_estoque = estoque[0]

        cursor.execute(
            """
            INSERT INTO Retirada_metal (quantidade, dia, id_compra, id_estoque)
            VALUES (%s, CURRENT_DATE, %s, %s)
            """,
            (quantidade, id_compra, id_estoque)
        )
        cursor.execute(
            """
            UPDATE Estoque
            SET quantidade = quantidade + %s
            WHERE id_estoque = %s
            """,
            (quantidade, id_estoque)
        )

        conexao.commit()

        nova_quantidade_retirada = quantidade_retirada + quantidade
        nova_quantidade_restante = quantidade_restante - quantidade

        return nova_quantidade_retirada, nova_quantidade_restante, True

    except Exception as erro:
        conexao.rollback()
        print("Erro ao registrar compra:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()

def registrar_pagamento_distribuidor(id_distribuidor, valor, forma_pagamento):

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if valor <= 0:
            print("Valor Invalido")
            return False

        cursor.execute(
            """
            SELECT saldo_dinheiro
            FROM Distribuidor
            WHERE id_distribuidor = %s
            """,
            (id_distribuidor,)
        )

        distribuidor = cursor.fetchone()

        if distribuidor is None:
            print("Distribuidor não encontrado")
            return False

        credito_atual = distribuidor[0]

        if credito_atual < valor:
            print("Pagamento maior que o saldo devedor")
            print(f"Saldo atual: {credito_atual}")
            return False

        cursor.execute(
            """
            SELECT id_estoque, quantidade
            FROM Estoque
            WHERE nome = 'dinheiro'
            """,
        )

        estoque = cursor.fetchone()

        if estoque is None:
            print("Dinheiro não encontrado")
            return False

        id_estoque = estoque[0]
        dinheiro_atual = estoque[1]

        if dinheiro_atual < valor:
            print("Dinheiro insuficiente para pagamento")
            print(f"Dinheiro disponivel: {dinheiro_atual}")
            return False

        cursor.execute(
            """
            INSERT INTO Pagamento_distribuidor (valor, dia, forma_pagamento, id_distribuidor, id_estoque)
            VALUES (%s, CURRENT_DATE, %s, %s, %s)
            """,
            (valor, forma_pagamento, id_distribuidor, id_estoque)
        )

        cursor.execute(
            """
            UPDATE Distribuidor
            SET saldo_dinheiro = saldo_dinheiro - %s
            WHERE id_distribuidor = %s
            """,
            (valor, id_distribuidor)
        )

        cursor.execute(
            """
            UPDATE Estoque
            SET quantidade = quantidade - %s
            WHERE id_estoque = %s
            """,
            (valor, id_estoque)
        )

        conexao.commit()

        return True

    except Exception as erro:
        conexao.rollback()
        print("Erro ao registrar pagamento:", erro)
        return False

    finally:
        cursor.close()
        conexao.close()

def consultar_distribuidores():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_distribuidor, nome, saldo_metal, saldo_dinheiro FROM Distribuidor ORDER BY nome")

        distribuidores = cursor.fetchall()

        cursor.close()
        conexao.close()

        return distribuidores

    except Exception as erro:
        print("Erro ao consultar distribuidor:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()   

    try:
        cursor.execute("SELECT id_cliente, nome, credito FROM Clientes ORDER BY nome")

        clientes = cursor.fetchall()

        cursor.close()
        conexao.close()

        return clientes

    except Exception as erro:
        print("Erro ao consultar clientes:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_pedidos_compra():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pc.id_compra,
                d.nome,
                pc.quantidade,
                COALESCE(SUM(rm.quantidade), 0) AS quantidade_retirada,
                pc.quantidade - COALESCE(SUM(rm.quantidade), 0) AS quantidade_pendente

            FROM pedido_compra pc
            
            JOIN distribuidor d
                ON pc.id_distribuidor = d.id_distribuidor

            LEFT JOIN Retirada_metal rm
                ON pc.id_compra = rm.id_compra
            
            GROUP BY
                pc.id_compra,
                d.nome,
                pc.quantidade

            HAVING
                pc.quantidade - COALESCE(SUM(rm.quantidade), 0) > 0

            ORDER BY pc.id_compra
            """
        )

        compras = cursor.fetchall()

        return compras

    except Exception as erro:
        print("Erro ao consultar compras pendentes:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_vendas():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pv.id_venda,
                c.nome,
                pv.quantidade,
                pv.cotacao,
                pv.dia,
                pv.total_rs
            FROM Pedido_venda pv

            JOIN Clientes c
                ON pv.id_cliente = c.id_cliente
            
            ORDER BY pv.dia DESC, pV.id_cliente DESC
            """
        )

        vendas = cursor.fetchall()

        return vendas

    except Exception as erro:
        print("Erro ao consultar vendas:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_compras():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pc.id_compra,
                d.nome,
                pc.quantidade,
                pc.cotacao,
                pc.dia,
                pc.total_rs
            FROM Pedido_compra pc

            JOIN Distribuidor d
                ON d.id_distribuidor = pc.id_distribuidor
            
            ORDER BY pc.dia DESC, pc.id_distribuidor DESC
            """
        )

        compras = cursor.fetchall()

        return compras

    except Exception as erro:
        print("Erro ao consultar compras:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_pagamentos_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pc.id_pagamento_cliente,
                pc.valor,
                c.nome,
                pc.dia,
                pc.forma_pagamento

            FROM Pagamento_clientes pc

            JOIN clientes c
                ON c.id_cliente = pc.id_cliente
            
            ORDER BY pc.dia DESC, pc.id_pagamento_cliente DESC
            """
        )

        pagamentos = cursor.fetchall()

        return pagamentos

    except Exception as erro:
        print("Erro ao consultar pagamentos:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_pagamento_distribuidor():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pd.id_pagamentodist,
                d.nome,
                pd.valor,
                pd.dia,
                pd.forma_pagamento
            FROM Pagamento_distribuidor pd

            JOIN Distribuidor d
                ON d.id_distribuidor = pd.id_distribuidor
            
            ORDER BY pd.dia DESC, pd.id_pagamentodist DESC
            """
        )

        pagamentos = cursor.fetchall()

        return pagamentos

    except Exception as erro:
        print("Erro ao consultar pagamentos:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_retirada_metal():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT
                rm.id_retirada,
                rm.id_compra,
                d.nome,
                rm.quantidade,
                rm.dia
            FROM Retirada_metal rm

            JOIN Pedido_compra pc
                ON pc.id_compra = rm.id_compra

            JOIN distribuidor d
                ON d.id_distribuidor = pc.id_distribuidor
            
            ORDER BY rm.dia DESC, rm.id_retirada DESC
            """
        )

        retiradas = cursor.fetchall()

        return retiradas

    except Exception as erro:
        print("Erro ao consultar retiradas:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def cadastrar_cliente(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if nome.strip() == "":
            print("Nome Invalido")
            return None

        cursor.execute(
            """
            INSERT INTO Clientes (nome, credito)
            VALUES (%s, 0)
            RETURNING id_cliente
            """,
            (nome,)
        )

        id_cliente = cursor.fetchone()[0]

        conexao.commit()

        return id_cliente

    except Exception as erro:
        conexao.rollback()
        print("Erro ao cadastrar cliente:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()

def cadastrar_distribuidor(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    try:       
        if nome.strip() == "":
            print("Nome Invalido")
            return None

        cursor.execute(
            """
            INSERT INTO Distribuidor (nome, saldo_metal, saldo_dinheiro)
            VALUES (%s, 0, 0)
            RETURNING id_distribuidor
            """,
            (nome,)
        )

        id_distribuidor = cursor.fetchone()[0]

        conexao.commit()

        return id_distribuidor

    except Exception as erro:
        conexao.rollback()
        print("Erro ao cadastrar distribuidor:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()        

def consultar_distribuidor(id_distribuidor):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("SELECT id_distribuidor, nome, saldo_metal, saldo_dinheiro FROM Distribuidor WHERE id_distribuidor = %s",
                       (id_distribuidor,))

        distribuidor = cursor.fetchone()

        cursor.close()
        conexao.close()

        return distribuidor

    except Exception as erro:
        print("Erro ao consultar distribuidor:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()   

    try:
        cursor.execute("SELECT id_cliente, nome, credito FROM Clientes WHERE id_cliente = %s",
                       (id_cliente,))

        cliente = cursor.fetchone()

        cursor.close()
        conexao.close()

        return cliente

    except Exception as erro:
        print("Erro ao consultar cliente:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()

def consultar_saldo_retirada(id_compra):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT quantidade
            FROM Pedido_compra
            WHERE id_compra = %s
            """,
            (id_compra,)
        )

        compra = cursor.fetchone()

        if compra is None:
            print("Compra não encontrada")
            return None

        quantidade_comprada = compra[0]

        cursor.execute(
            """
            SELECT COALESCE(SUM(quantidade), 0)
            FROM Retirada_metal
            WHERE id_compra = %s
            """,
            (id_compra,)
        )

        quantidade_retirada = cursor.fetchone()[0]

        quantidade_restante = quantidade_comprada - quantidade_retirada

        return quantidade_comprada, quantidade_retirada, quantidade_restante

    except Exception as erro:
        print("Erro ao consultar saldo da retirada:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()

def relatorio_movimentacoes(data_inicio, data_final):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            SELECT
                pv.dia,
                pv.quantidade,
                c.nome,
                pv.cotacao,
                pv.total_rs

            FROM Pedido_venda pv

            JOIN clientes c
                ON c.id_cliente = pv.id_cliente

            WHERE pv.dia BETWEEN %s AND %s

            ORDER BY pv.dia
            """,
            (data_inicio, data_final)
        )

        venda = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                pc.dia,
                pc.quantidade,
                d.nome,
                pc.cotacao,
                pc.total_rs
            FROM Pedido_compra pc

            JOIN Distribuidor d
                ON d.id_distribuidor = pc.id_distribuidor

            WHERE
                pc.dia BETWEEN %s AND %s
            
            ORDER BY pc.dia
            """,
            (data_inicio, data_final)
        )

        compra = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                pg.dia,
                pg.valor,
                c.nome,
                pg.forma_pagamento
            FROM Pagamento_clientes pg

            JOIN Clientes c
                ON c.id_cliente = pg.id_cliente

            WHERE
                pg.dia BETWEEN %s AND %s
            
            ORDER BY pg.dia
            """,
            (data_inicio, data_final)
        )

        pagamento_cliente = cursor.fetchall()

        cursor.execute(
            """
            SELECT
                pd.dia,
                pd.valor,
                d.nome,
                pd.forma_pagamento
            FROM Pagamento_distribuidor pd

            JOIN Distribuidor d
                ON d.id_distribuidor = pd.id_distribuidor

            WHERE
                pd.dia BETWEEN %s AND %s
            
            ORDER BY pd.dia
            """,
            (data_inicio, data_final)
        )

        pagamento_distribuidor = cursor.fetchall()

        cursor.execute(
            """
            SELECT dia, id_retirada, quantidade
            FROM Retirada_metal
            WHERE dia BETWEEN %s AND %s
            ORDER BY dia
            """,
            (data_inicio, data_final)
        )

        retirada = cursor.fetchall()

        return venda, compra, pagamento_cliente, pagamento_distribuidor, retirada

    except Exception as erro:
        print("Erro ao gerar relatório:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()            