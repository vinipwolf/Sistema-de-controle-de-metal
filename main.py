from banco import consultar_vendas, consultar_compras,consultar_pagamentos_clientes,consultar_pagamento_distribuidor,consultar_retirada_metal,cadastrar_cliente,cadastrar_distribuidor,consultar_distribuidor,consultar_cliente,consultar_saldo_retirada,relatorio_movimentacoes, consultar_pedidos_compra, consultar_distribuidores, consultar_clientes, registrar_pagamento_distribuidor, registrar_retirada_metal, registrar_compra, consultar_estoque, registrar_venda, registrar_pagamento_cliente

while True:
    print("\n=== SISTEMA ===")
    print("1 - Consultar estoque")
    print("2 - Registrar venda")
    print("3 - Registrar pagamento de cliente")
    print("4 - Registrar compra de metal")
    print("5 - Registrar retirada metal")
    print("6 - Registrar pagamento distribuidor")
    print("7 - Consultar clientes")
    print("8 - Consultar distribuidores")
    print("9 - Consultar pedidos de compra pendentes")
    print("10 - Consultar historico de vendas")
    print("11 - Consultar historico compras")
    print("12 - Consultar pagamentos dos clientes")
    print("13 - Consultar pagamentos dos distribuidores")
    print("14 - Consultar historico de retiradas de metal")
    print("15 - Cadastrar cliente")
    print("16 - Cadastrar distribuidor")
    print("17 - Consultar cliente")
    print("18 - Consultar distribuidor")
    print("19 - Consultar saldo de retirada")
    print("20 - Relatorio de movimentações")
    print("21 - Sair")

    opcao = input("Escolha uma opção: ")



    if opcao == "1":
        estoque = consultar_estoque()

        print("\n=== Estoque ===")

        for item in estoque:
            print(
                f"Item: {item[0]}"
                f" Quantidade: {item[1]} {item[2]}"
            )

    elif opcao == "2":
        id_cliente = int(input("ID do cliente: "))
        quantidade = int(input("Quantidade: "))
        cotacao = int(input("Cotação: "))

        total_venda = registrar_venda(id_cliente, quantidade, cotacao)

        if total_venda is not None:
            print("=== VENDA REGISTRADA ===")
            print(
                f"ID Cliente: {id_cliente}"
                f"\nQuantidade: {quantidade}"
                f"\nCotação: {cotacao}"
                f"\nTotal: {total_venda}"
            )
    elif opcao == "3":
        id_cliente = int(input("ID do cliente: "))
        valor = float(input("Valor: "))
        forma_pagamento = input("Forma de Pagamento: ")

        sucesso = registrar_pagamento_cliente(id_cliente, valor, forma_pagamento)

        if sucesso is True:
            print("=== PAGAMENTO REGISTRADO ===")
            print(
                f"ID Cliente: {id_cliente}"
                f"\n Valor: {valor}"
                f"\n Forma de pagamento: {forma_pagamento}"
            )

    elif opcao == "4":
        id_distribuidor = int(input("ID do distribuidor: "))
        quantidade = float(input("Quantidade: "))
        cotacao = int(input("cotacao "))

        total_compra = registrar_compra(id_distribuidor, quantidade, cotacao)

        if total_compra is not None:
            print("=== Compra registrada ===")
            print(
                f"ID Distribuidor: {id_distribuidor}"
                f"\n Quantidade: {quantidade}"
                f"\n cotacao: {cotacao}"
                F"\n Total :{total_compra}"
            )            
    elif opcao == "5":
        id_compra = int(input("ID do pedido de compra: "))
        quantidade = int(input("quantidade: "))

        quantidade_retirada, quantidade_restante, sucesso = registrar_retirada_metal(id_compra, quantidade)

        if sucesso is True:
            print("=== Retirada registrada ===")
            print(
                f"ID Compra: {id_compra}"
                f"\n Quantidade: {quantidade}"
                f"\n Quantidade retirada: {quantidade_retirada}"
                F"\n Quantidade restante :{quantidade_restante}"
            )

    elif opcao == "6":
        id_distribuidor = int(input("ID do distribuidor: "))
        valor = float(input("Valor do pagamento: "))
        forma_pagamento = input("Forma de pagamento: ")

        sucesso = registrar_pagamento_distribuidor(id_distribuidor, valor, forma_pagamento)

        if sucesso is True:
            print("=== Retirada registrada ===")
            print(
                f"ID distribuidor: {id_distribuidor}"
                f"\nvalor: {valor}"
                f"\nforma de pagamento: {forma_pagamento}"
            )

    elif opcao == "7":
        clientes = consultar_clientes()

        print("\n=== Clientes ===")

        for cliente in clientes:
            print(
                f"ID: {cliente[0]}"
                f"\nNome: {cliente[1]}"
                f"\nCrédito: R$ {cliente[2]:.2f}"
                "\n-------------------------"
            )

    elif opcao == "8":
        distribuidores = consultar_distribuidores()

        print("\n=== DISTRIBUIDORES ===")

        for distribuidor in distribuidores:
            print(
                f"ID: {distribuidor[0]}"
                f"\nNome: {distribuidor[1]}"
                f"\nSaldo metal: {distribuidor[2]:.2f}"
                f"\nSaldo dinheiro: R$ {distribuidor[3]:.2f}"

                "\n-------------------------"
            )

    elif opcao == "9":
        compras = consultar_pedidos_compra()

        print("\n=== COMPRAS PENDENTES ===")

        for compra in compras:
            print(
                f"ID Compra: {compra[0]}"
                f"\nDistribuidor: {compra[1]}"
                f"\nQuantidade comprada: {compra[2]:.1f} g"
                f"\nQuantidade retirada: {compra[3]:.1f} g"
                f"\nQuantidade pendente: {compra[4]:.1f} g"
                "\n-------------------------"
            )
    elif opcao == "10":
        vendas = consultar_vendas()

        print("\n=== HISTÓRICO DE VENDAS ===")

        for venda in vendas:
            print(
                f"ID Venda: {venda[0]}"
                f"\nCliente: {venda[1]}"
                f"\nQuantidade: {venda[2]} g"
                f"\nCotação: R$ {venda[3]:.2f}"
                f"\nTotal: R$ {venda[5]:.2f}"
                f"\nData: {venda[4]}"
                "\n-------------------------"
            )

    elif opcao == "11":
        compras = consultar_compras()

        print("\n=== HISTÓRICO DE COMPRAS ===")

        for compra in compras:
            print(
                f"ID Compra: {compra[0]}"
                f"\nDistribuidor: {compra[1]}"
                f"\nQuantidade: {compra[2]} g"
                f"\nCotação: R$ {compra[3]:.2f}"
                f"\nTotal: R$ {compra[5]:.2f}"
                f"\nData: {compra[4]}"
                "\n-------------------------"
            )

    elif opcao == "12":
        pagamentos = consultar_pagamentos_clientes()

        print("\n=== PAGAMENTOS DOS CLIENTES ===")

        for pagamento in pagamentos:
            print(
                f"ID Pagamento: {pagamento[0]}"
                f"\nCliente: {pagamento[2]}"
                f"\nValor: R$ {pagamento[1]:.2f}"
                f"\nForma de pagamento: {pagamento[4]}"
                f"\nData: {pagamento[3]}"
                "\n-------------------------"
            )

    elif opcao == "13":
        pagamentos = consultar_pagamento_distribuidor()

        print("\n=== PAGAMENTOS AOS DISTRIBUIDORES ===")

        for pagamento in pagamentos:
            print(
                f"ID Pagamento: {pagamento[0]}"
                f"\nDistribuidor: {pagamento[1]}"
                f"\nValor: R$ {pagamento[2]:.2f}"
                f"\nForma de pagamento: {pagamento[4]}"
                f"\nData: {pagamento[3]}"
                "\n-------------------------"
            )

    elif opcao == "14":
        retiradas = consultar_retirada_metal()
        print("\n=== HISTÓRICO DE RETIRADAS ===")

        for retirada in retiradas:
            print(
                f"ID Retirada: {retirada[0]}"
                f"\nID Compra: {retirada[1]}"
                f"\nDistribuidor: {retirada[2]}"
                f"\nQuantidade: {retirada[3]} g"
                f"\nData: {retirada[4]}"
                "\n-------------------------"
            )

    elif opcao == "15":
        nome = input("Nome do cliente: ")

        id_cliente = cadastrar_cliente(nome)

        if id_cliente is not None:
            print("\n=== CLIENTE CADASTRADO ===")
            print(f"ID: {id_cliente}")
            print(f"Nome: {nome}")

    elif opcao == "16":
        nome = input("Nome do distribuidor: ")

        id_distribuidor = cadastrar_distribuidor(nome)

        if id_distribuidor is not None:
            print("\n=== DISTRIBUIDOR CADASTRADO ===")
            print(f"ID: {id_distribuidor}")
            print(f"Nome: {nome}")

    elif opcao == "17":
        id_cliente = int(input("ID do cliente: "))

        cliente = consultar_cliente(id_cliente)

        if cliente is None:
            print("Cliente não encontrado.")
        else:
            print("\n=== CLIENTE ===")
            print(
                f"ID: {cliente[0]}"
                f"\nNome: {cliente[1]}"
                f"\nCrédito: R$ {cliente[2]:.2f}"
            )
    elif opcao == "18":
        id_distribuidor = int(input("ID do distribuidor: "))

        distribuidor = consultar_distribuidor(id_distribuidor)

        if distribuidor is None:
            print("Distribuidor não encontrado.")
        else:
            print("\n=== DISTRIBUIDOR ===")
            print(
                f"ID: {distribuidor[0]}"
                f"\nNome: {distribuidor[1]}"
                f"\nSaldo metal: {distribuidor[2]:.2f}"
                f"\nSaldo dinheiro: R$ {distribuidor[3]:.2f}"
            )
    elif opcao == "19":
        id_compra = int(input("ID da compra: "))

        saldo = consultar_saldo_retirada(id_compra)

        if saldo is not None:
            quantidade_comprada, quantidade_retirada, quantidade_restante = saldo

            print("\n=== SALDO DA COMPRA ===")
            print(
                f"ID Compra: {id_compra}"
                f"\nQuantidade comprada: {quantidade_comprada} g"
                f"\nQuantidade retirada: {quantidade_retirada} g"
                f"\nQuantidade restante: {quantidade_restante} g"
            )
    elif opcao == "20":
        data_inicio = input("Data inicial (AAAA-MM-DD): ")
        data_fim = input("Data final (AAAA-MM-DD): ")

        relatorio = relatorio_movimentacoes(data_inicio, data_fim)

        if relatorio is not None:
            vendas, compras, pagamentos_clientes, pagamentos_distribuidores, retiradas = relatorio

        print("\n=== RELATÓRIO DE MOVIMENTAÇÃO ===")

        print("\n--- VENDAS ---")
        for venda in vendas:
            print(
                f"Data: {venda[0]}"
                f"\nCliente: {venda[2]}"
                f"\nQuantidade: {venda[1]} g"
                f"\nCotação: R$ {venda[3]:.2f}"
                f"\nTotal: R$ {venda[4]:.2f}"
                "\n-------------------------"
            )

        print("\n--- COMPRAS ---")
        for compra in compras:
            print(
                f"Data: {compra[0]}"
                f"\nDistribuidor: {compra[2]}"
                f"\nQuantidade: {compra[1]} g"
                f"\nCotação: R$ {compra[3]:.2f}"
                f"\nTotal: R$ {compra[4]:.2f}"
                "\n-------------------------"
            )

        print("\n--- PAGAMENTOS DE CLIENTES ---")
        for pagamento in pagamentos_clientes:
            print(
                f"Data: {pagamento[0]}"
                f"\nCliente: {pagamento[2]}"
                f"\nValor: R$ {pagamento[1]:.2f}"
                f"\nForma de pagamento: {pagamento[3]}"
                "\n-------------------------"
            )

        print("\n--- PAGAMENTOS A DISTRIBUIDORES ---")
        for pagamento in pagamentos_distribuidores:
            print(
                f"Data: {pagamento[0]}"
                f"\nDistribuidor: {pagamento[2]}"
                f"\nValor: R$ {pagamento[1]:.2f}"
                f"\nForma de pagamento: {pagamento[3]}"
                "\n-------------------------"
            )

        print("\n--- RETIRADAS ---")
        for retirada in retiradas:
            print(
                f"Data: {retirada[0]}"
                f"\nID Retirada: {retirada[1]}"
                f"\nQuantidade: {retirada[2]} g"
                "\n-------------------------"
            )

    elif opcao == "21":
        break

    else:
        print("Opção invalida!")













        
