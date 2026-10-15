import hashlib
import logging
import os

log = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, leitor, tratamento, validador, banco, controle, carga):
        self.leitor = leitor
        self.tratamento = tratamento
        self.validador = validador
        self.banco = banco
        self.controle = controle
        self.carga = carga

    def calcular_hash(self, caminho):
        resumo = hashlib.sha256()
        with open(caminho, "rb") as arquivo:
            bloco = arquivo.read(1024 * 1024)
            while bloco:
                resumo.update(bloco)
                bloco = arquivo.read(1024 * 1024)
        return resumo.hexdigest()

    def processar(self, caminho, reprocessar=False):
        nome = os.path.basename(caminho)
        hash_arquivo = self.calcular_hash(caminho)

        if not reprocessar and self.controle.ja_processado(nome, hash_arquivo):
            log.info("%s ja foi processado, pulando", nome)
            return 0

        self.controle.iniciar(nome, hash_arquivo)

        try:
            bruto = self.leitor.ler(caminho)
            dados = self.tratamento.tratar(bruto, nome)
            validos, rejeitados = self.validador.separar(dados)
            validos, duplicados = self.validador.remover_duplicados(validos)

            if validos.empty:
                raise ValueError("nenhum registro valido no arquivo")

            log.info("%s: %s validos, %s rejeitados, %s duplicados", nome, len(validos), len(rejeitados), duplicados)

            self.banco.carregar_staging(validos)
            self.banco.salvar_rejeitados(nome, rejeitados)
            self.carga.executar()
            self.banco.confirmar()
        except Exception as erro:
            self.banco.desfazer()
            self.controle.finalizar(nome, "erro", mensagem=str(erro))
            raise

        self.controle.finalizar(nome, "sucesso", len(validos), len(rejeitados), duplicados)
        return len(validos)
