import logging
import os

log = logging.getLogger(__name__)


class CargaDimensional:
    ordem = [
        "dim_produto.sql",
        "dim_municipio.sql",
        "dim_data.sql",
        "dim_posto_fechar.sql",
        "dim_posto_inserir.sql",
        "fato_preco.sql",
    ]

    def __init__(self, banco, pasta_sql):
        self.banco = banco
        self.pasta = os.path.join(pasta_sql, "carga")

    def executar(self):
        for script in self.ordem:
            log.info("executando %s", script)
            self.banco.executar_script(os.path.join(self.pasta, script))
