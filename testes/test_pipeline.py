import pytest

from anp.leitor import LeitorArquivo
from anp.pipeline import Pipeline
from anp.tratamento import Tratamento
from anp.validacao import Validador

amostra = "dados/exemplo/ca-amostra.csv"


class BancoFalso:
    def __init__(self):
        self.staging = None
        self.rejeitados = None
        self.confirmado = False
        self.desfeito = False

    def carregar_staging(self, dados):
        self.staging = dados

    def salvar_rejeitados(self, arquivo, rejeitados):
        self.rejeitados = rejeitados

    def confirmar(self):
        self.confirmado = True

    def desfazer(self):
        self.desfeito = True


class ControleFalso:
    def __init__(self, processados=None):
        self.processados = processados or set()
        self.finalizados = []

    def ja_processado(self, arquivo, hash_arquivo):
        return (arquivo, hash_arquivo) in self.processados

    def iniciar(self, arquivo, hash_arquivo):
        self.atual = (arquivo, hash_arquivo)

    def finalizar(self, arquivo, status, linhas=0, rejeitadas=0, duplicadas=0, mensagem=""):
        self.finalizados.append((status, linhas, rejeitadas, duplicadas))


class CargaFalsa:
    def __init__(self, falhar=False):
        self.falhar = falhar
        self.executada = False

    def executar(self):
        if self.falhar:
            raise RuntimeError("erro no merge")
        self.executada = True


def montar(controle=None, carga=None):
    banco = BancoFalso()
    controle = controle or ControleFalso()
    carga = carga or CargaFalsa()
    pipeline = Pipeline(LeitorArquivo(), Tratamento(), Validador(), banco, controle, carga)
    return pipeline, banco, controle, carga


def test_processa_arquivo_completo():
    pipeline, banco, controle, carga = montar()

    linhas = pipeline.processar(amostra)

    assert linhas == 6
    assert len(banco.staging) == 6
    assert len(banco.rejeitados) == 3
    assert carga.executada
    assert banco.confirmado
    assert controle.finalizados[-1] == ("sucesso", 6, 3, 1)


def test_pula_arquivo_ja_processado():
    pipeline, _, _, _ = montar()
    hash_arquivo = pipeline.calcular_hash(amostra)
    pipeline, _, _, carga = montar(controle=ControleFalso({("ca-amostra.csv", hash_arquivo)}))

    linhas = pipeline.processar(amostra)

    assert linhas == 0
    assert not carga.executada


def test_reprocessar_ignora_controle():
    pipeline, _, _, _ = montar()
    hash_arquivo = pipeline.calcular_hash(amostra)
    pipeline, _, _, carga = montar(controle=ControleFalso({("ca-amostra.csv", hash_arquivo)}))

    pipeline.processar(amostra, reprocessar=True)

    assert carga.executada


def test_falha_na_carga_desfaz_e_registra_erro():
    pipeline, banco, controle, _ = montar(carga=CargaFalsa(falhar=True))

    with pytest.raises(RuntimeError):
        pipeline.processar(amostra)

    assert banco.desfeito
    assert not banco.confirmado
    assert controle.finalizados[-1][0] == "erro"
