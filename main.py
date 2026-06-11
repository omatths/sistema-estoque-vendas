from produto import Produto
import estoque
import arquivos

def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número decimal (Preço).")

def menu_principal():
    print("\n" + "="*40)
    print("      SISTEMA DE ESTOQUE E VENDAS")
    print("="*40)
    print("1. Cadastrar Produto")
    print("2. Editar Produto")
    print("3. Remover Produto")
    print("4. Buscar Produto por Código (Binária)")
    print("5. Buscar Produto por Nome (Linear)")
    print("6. Registrar Venda")
    print("7. Listar Todos os Produtos (Ordenados)")
    print("8. Listar por Categoria")
    print("9. Relatório de Baixo Estoque")
    print("10. Sair")
    print("="*40)

def listar_paginado(lista_produtos):
    if not lista_produtos:
        print("Nenhum produto cadastrado.")
        return
    
    itens_por_pagina = 5
    total = len(lista_produtos)
    
    for i in range(0, total, itens_por_pagina):
        print(f"\n--- Exibindo itens {i+1} a {min(i+itens_por_pagina, total)} de {total} ---")
        for p in lista_produtos[i:i+itens_por_pagina]:
            print(f"Cód: {p.codigo} | Nome: {p.nome} | Cat: {p.categoria} | Preço: R${p.preco:.2f} | Qtd: {p.quantidade}")
        
        if i + itens_por_pagina < total:
            opcao = input("\nPressione ENTER para ver mais ou 's' para sair da listagem: ")
            if opcao.lower().strip() == 's':
                break

def main():
    v_nao_ordenado, v_ordenado = arquivos.carregar_dados()

    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- Cadastrar Produto ---")
            cod = ler_inteiro("Código: ")
            nome = input("Nome: ")
            cat = input("Categoria: ")
            preco = ler_float("Preço: R$ ")
            qtd = ler_inteiro("Quantidade: ")

            if Produto.validar_dados(cod, nome, cat, preco, qtd):
                novo = Produto(cod, nome, cat, preco, qtd)
                if estoque.cadastrar_produto(v_nao_ordenado, v_ordenado, novo):
                    print("Produto cadastrado com sucesso!")
                    arquivos.salvar_dados(v_nao_ordenado)

        elif opcao == "2":
            print("\n--- Editar Produto ---")
            cod = ler_inteiro("Digite o código do produto que deseja editar: ")
            idx = estoque.buscar_por_codigo_binaria(v_ordenado, cod)
            if idx == -1:
                print("Produto não encontrado.")
            else:
                p = v_ordenado[idx]
                print(f"Editando: {p.nome} (Atual - Preço: {p.preco} | Qtd: {p.quantidade})")
                novo_nome = input(f"Novo Nome [{p.nome}]: ") or p.nome
                novo_cat = input(f"Nova Categoria [{p.categoria}]: ") or p.categoria
                novo_preco = input(f"Novo Preço [{p.preco}]: R$ ")
                novo_preco = float(novo_preco) if novo_preco else p.preco
                nova_qtd = input(f"Nova Quantidade [{p.quantidade}]: ")
                nova_qtd = int(nova_qtd) if nova_qtd else p.quantidade

                if Produto.validar_dados(cod, novo_nome, novo_cat, novo_preco, nova_qtd):
                    p.nome = novo_nome
                    p.categoria = novo_cat
                    p.preco = novo_preco
                    p.quantidade = nova_qtd
                    print("Produto alterado com sucesso!")
                    arquivos.salvar_dados(v_nao_ordenado)

        elif opcao == "3":
            print("\n--- Remover Produto ---")
            cod = ler_inteiro("Código do produto a remover: ")
            if estoque.remover_produto(v_nao_ordenado, v_ordenado, cod):
                print("Produto removido.")
                arquivos.salvar_dados(v_nao_ordenado)

        elif opcao == "4":
            print("\n--- Busca Binária por Código ---")
            cod = ler_inteiro("Código de pesquisa: ")
            idx = estoque.buscar_por_codigo_binaria(v_ordenado, cod)
            if idx != -1:
                p = v_ordenado[idx]
                print(f"\nEncontrado: Cód: {p.codigo} | Nome: {p.nome} | Cat: {p.categoria} | Preço: R${p.preco:.2f} | Estoque: {p.quantidade}")
            else:
                print("Produto não localizado.")

        elif opcao == "5":
            print("\n--- Busca Linear por Nome ---")
            nome = input("Digite o nome ou parte dele: ")
            encontrados = estoque.buscar_por_nome_linear(v_nao_ordenado, nome)
            listar_paginado(encontrados)

        elif opcao == "6":
            print("\n--- Registrar Venda ---")
            cod = ler_inteiro("Código do produto vendido: ")
            idx = estoque.buscar_por_codigo_binaria(v_ordenado, cod)
            if idx == -1:
                print("Produto inexistente.")
            else:
                p = v_ordenado[idx]
                qtd_venda = ler_inteiro(f"Quantidade a vender (Disponível: {p.quantidade}): ")
                if qtd_venda <= 0:
                    print("Erro: Quantidade inválida.")
                elif qtd_venda > p.quantidade:
                    print("Erro: Estoque insuficiente para realizar a venda.")
                else:
                    p.quantidade -= qtd_venda
                    print(f"Venda registrada! {p.nome} agora possui {p.quantidade} unidades.")
                    arquivos.salvar_dados(v_nao_ordenado)

        elif opcao == "7":
            print("\n--- Todos os Produtos Cadastrados (Ordem de Código) ---")
            listar_paginado(v_ordenado)

        elif opcao == "8":
            print("\n--- Filtro por Categoria ---")
            cat = input("Digite a categoria: ").strip().lower()
            filtrados = [p for p in v_nao_ordenado if p.categoria.lower() == cat]
            listar_paginado(filtrados)

        elif opcao == "9":
            print("\n--- Relatório de Baixo Estoque ---")
            limite = ler_inteiro("Defina o limite mínimo de alerta: ")
            alertas = [p for p in v_nao_ordenado if p.quantidade < limite]
            listar_paginado(alertas)

        elif opcao == "10":
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("Opção inválida! Escolha um número de 1 a 10.")

if __name__ == "__main__":
    main()