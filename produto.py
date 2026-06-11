class Produto:
    def __init__(self, codigo, nome, categoria, preco, quantidade):
        self.codigo = int(codigo)
        self.nome = str(nome).strip()
        self.categoria = str(categoria).strip()
        self.preco = float(preco)
        self.quantidade = int(quantidade)

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade
        }

    @staticmethod
    def validar_dados(codigo, nome, categoria, preco, quantidade):
        if not str(nome).strip() or not str(categoria).strip():
            print("Erro: Nome e Categoria não podem ser vazios.")
            return False
        try:
            if int(codigo) <= 0:
                print("Erro: O código deve ser um número inteiro positivo.")
                return False
            if float(preco) <= 0:
                print("Erro: O preço deve ser maior que zero.")
                return False
            if int(quantidade) < 0:
                print("Erro: A quantidade não pode ser negativa.")
                return False
        except ValueError:
            print("Erro: Formato numérico inválido.")
            return False
        return True