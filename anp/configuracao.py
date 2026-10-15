import os


class Configuracao:
    def __init__(self):
        self.usuario = os.getenv("oracle_usuario", "anp")
        self.senha = os.getenv("oracle_senha", "anp")
        self.dsn = os.getenv("oracle_dsn", "localhost:1521/FREEPDB1")
        self.pasta_arquivos = os.getenv("pasta_arquivos", "arquivos")
        self.pasta_sql = os.getenv("pasta_sql", "sql")
        self.url_base = os.getenv(
            "anp_url_base",
            "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsas/ca",
        )
