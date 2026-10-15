import pandas as pd
import pytest

from anp.leitor import LayoutDesconhecido, LeitorArquivo
from anp.tratamento import Tratamento
from anp.validacao import Validador

amostra = "dados/exemplo/ca-amostra.csv"


def ler_tratado():
    bruto = LeitorArquivo().ler(amostra)
    return Tratamento().tratar(bruto, "ca-amostra.csv")


def test_le_layout_atual():
    dados = LeitorArquivo().ler(amostra)
    assert len(dados) == 10
    assert "cnpj" in dados.columns


def test_le_layout_com_nomes_diferentes(tmp_path):
    arquivo = tmp_path / "antigo.csv"
    arquivo.write_text(
        "Região;Estado;Município;Revenda;CNPJ;Produto;Data da Coleta;Valor de Venda\n"
        "SE;SP;SANTOS;POSTO A;44.444.444/0001-44;GASOLINA;01/01/2019;4,39\n",
        encoding="latin1",
    )
    dados = LeitorArquivo().ler(arquivo)
    assert dados.loc[0, "municipio"] == "SANTOS"
    assert dados.loc[0, "bandeira"] is None


def test_layout_sem_coluna_obrigatoria(tmp_path):
    arquivo = tmp_path / "quebrado.csv"
    arquivo.write_text("Estado;Municipio;Produto\nSP;SANTOS;GASOLINA\n", encoding="utf-8")
    with pytest.raises(LayoutDesconhecido):
        LeitorArquivo().ler(arquivo)


def test_tratamento_converte_valores():
    dados = ler_tratado()
    assert dados.loc[0, "cnpj"] == "11111111000111"
    assert dados.loc[0, "valor_venda"] == 5.79
    assert dados.loc[0, "data_coleta"] == pd.Timestamp("2024-01-02")


def test_validador_separa_rejeitados():
    validos, rejeitados = Validador().separar(ler_tratado())
    motivos = sorted(rejeitados["motivo"].tolist())
    assert motivos == ["cnpj invalido", "data invalida", "preco zerado ou negativo"]
    assert len(validos) == 7


def test_validador_remove_duplicados():
    validos, _ = Validador().separar(ler_tratado())
    sem_duplicados, removidos = Validador().remover_duplicados(validos)
    assert removidos == 1
    assert len(sem_duplicados) == 6
