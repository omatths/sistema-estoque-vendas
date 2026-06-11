from produto import Produto

def buscar_por_codigo_binaria(vetor_ordenado, codigo):
    esquerda = 0
    direita = len(vetor_ordenado) - 1

    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if vetor_ordenado[meio].codigo == codigo:
            return meio  # Retorna o índice no vetor ordenado
        elif vetor_ordenado[meio].codigo < codigo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1

def buscar_por_nome_linear(vetor_nao_ordenado, nome):
    resultados = []
    nome_pesquisa = nome.lower().strip()
    for p in vetor_nao_ordenado:
        if nome_pesquisa in p.nome.lower():
            resultados.append(p)
    return resultados

def cadastrar_produto(vetor_nao_ordenado, vetor_ordenado, produto):
    # Validar se o código já existe usando a busca binária rápida
    if buscar_por_codigo_binaria(vetor_ordenado, produto.codigo) != -1:
        print("Erro: Já existe um produto cadastrado com este código.")
        return False

    # Inserção no vetor não ordenado: O(1)
    vetor_nao_ordenado.append(produto)

    # Inserção mantendo o vetor ordenado: O(n)
    posicao = 0
    while posicao < len(vetor_ordenado) and vetor_ordenado[posicao].codigo < produto.codigo:
        posicao += 1
    vetor_ordenado.insert(posicao, produto)
    return True

def remover_produto(vetor_nao_ordenado, vetor_ordenado, codigo):
    idx_ordenado = buscar_por_codigo_binaria(vetor_ordenado, codigo)
    if idx_ordenado == -1:
        print("Erro: Produto não encontrado para remoção.")
        return False

    produto = vetor_ordenado[idx_ordenado]
    
    # Remove de ambos os vetores
    vetor_ordenado.pop(idx_ordenado)
    vetor_nao_ordenado.remove(produto)
    return True