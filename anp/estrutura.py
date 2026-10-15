import os


class Estrutura:
    def __init__(self, banco, pasta_sql):
        self.banco = banco
        self.pasta = os.path.join(pasta_sql, "estrutura")

    def criar(self):
        for nome in sorted(os.listdir(self.pasta)):
            if nome.endswith(".sql"):
                self.banco.executar_script(os.path.join(self.pasta, nome), ignorar_existentes=True)
        self.banco.confirmar()
