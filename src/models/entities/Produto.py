class Produto:
    def __init__(self, id_produto, nome_prod=None, descproduto=None, valorproduto=None):
        self.id_produto = id_produto
        self.nome_prod = nome_prod
        self.descproduto = descproduto
        self.valorproduto = valorproduto

    def to_JSON(self):
        return {
            'id': self.id_produto,
            'nome_prod': self.nome_prod,
            'descproduto': self.descproduto,
            'valorproduto': self.valorproduto
        }
