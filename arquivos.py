import json
import os
from produto import Produto

ARQUIVO_DADOS = "estoque.json"

def salvar_dados(vetor_nao_ordenado):
    try:
        dados = [p.to_dict() for p in vetor_nao_ordenado]
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except IOError:
        print("Erro ao tentar salvar os dados no arquivo.")

def carregar_dados():
    vetor_nao_ordenado = []
    vetor_ordenado = []
    
    if not os.path.exists(ARQUIVO_DADOS):
        return vetor_nao_ordenado, vetor_ordenado

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            for item in dados:
                p = Produto(item["codigo"], item["nome"], item["categoria"], item["preco"], item["quantidade"])
                vetor_nao_ordenado.append(p)
        
        # Cria o vetor ordenado a partir dos dados carregados
        vetor_ordenado = vetor_nao_ordenado.copy()
        vetor_ordenado.sort(key=lambda prod: prod.codigo)
    except (json.JSONDecodeError, IOError):
        print("Erro ao carregar arquivo de dados. Iniciando estoque vazio.")
        
    return vetor_nao_ordenado, vetor_ordenado