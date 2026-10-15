import logging
import os

import requests

log = logging.getLogger(__name__)


class Baixador:
    def __init__(self, url_base, pasta):
        self.url_base = url_base
        self.pasta = pasta

    def nome_arquivo(self, ano, semestre):
        return f"ca-{ano}-{semestre:02d}.csv"

    def baixar(self, ano, semestre):
        nome = self.nome_arquivo(ano, semestre)
        destino = os.path.join(self.pasta, nome)

        if os.path.exists(destino):
            log.info("%s ja foi baixado", nome)
            return destino

        os.makedirs(self.pasta, exist_ok=True)
        log.info("baixando %s", nome)
        resposta = requests.get(f"{self.url_base}/{nome}", timeout=300)
        resposta.raise_for_status()

        with open(destino, "wb") as arquivo:
            arquivo.write(resposta.content)

        return destino
