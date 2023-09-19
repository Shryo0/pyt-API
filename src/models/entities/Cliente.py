class Cliente:
    def __init__(self, id, nome=None, telefone=None, cep=None, complemento=None, numcpf=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.cep = cep
        self.complemento = complemento
        self.numcpf = numcpf
        
    def to_JSON(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'cep': self.cep,
            'complemento': self.complemento,
            'numcpf': self.numcpf
        }