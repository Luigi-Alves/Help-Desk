class Chamado:
    def __init__(self, id, nome, setor, descricao, status="Aberto"):
        self.id = id
        self.nome = nome
        self.setor = setor
        self.descricao = descricao
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "setor": self.setor,
            "descricao": self.descricao,
            "status": self.status
        }