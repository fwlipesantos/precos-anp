class ControleArquivos:
    def __init__(self, banco):
        self.banco = banco

    def ja_processado(self, arquivo, hash_arquivo):
        linhas = self.banco.consultar(
            "select 1 from controle_arquivo where arquivo = :arquivo and hash = :hash and status = 'sucesso'",
            {"arquivo": arquivo, "hash": hash_arquivo},
        )
        return len(linhas) > 0

    def iniciar(self, arquivo, hash_arquivo):
        self.banco.executar(
            """
            merge into controle_arquivo c
            using (select :arquivo arquivo, :hash hash from dual) n
            on (c.arquivo = n.arquivo)
            when matched then update set c.hash = n.hash, c.status = 'processando', c.inicio = systimestamp,
                c.fim = null, c.linhas = null, c.rejeitadas = null, c.duplicadas = null, c.mensagem = null
            when not matched then insert (arquivo, hash, status, inicio)
                values (n.arquivo, n.hash, 'processando', systimestamp)
            """,
            {"arquivo": arquivo, "hash": hash_arquivo},
        )
        self.banco.confirmar()

    def finalizar(self, arquivo, status, linhas=0, rejeitadas=0, duplicadas=0, mensagem=""):
        self.banco.executar(
            """
            update controle_arquivo
            set status = :status, linhas = :linhas, rejeitadas = :rejeitadas, duplicadas = :duplicadas,
                mensagem = :mensagem, fim = systimestamp
            where arquivo = :arquivo
            """,
            {
                "arquivo": arquivo,
                "status": status,
                "linhas": linhas,
                "rejeitadas": rejeitadas,
                "duplicadas": duplicadas,
                "mensagem": mensagem[:4000],
            },
        )
        self.banco.confirmar()
