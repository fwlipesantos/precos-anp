import pandas as pd


class Validador:
    preco_maximo = 50

    def separar(self, dados):
        motivo = pd.Series("", index=dados.index)

        motivo[dados["cnpj"].str.len() != 14] = "cnpj invalido"
        motivo[dados["uf"].str.len() != 2] = "uf invalida"
        motivo[dados["produto"] == ""] = "produto vazio"
        motivo[dados["data_coleta"].isna()] = "data invalida"
        motivo[dados["valor_venda"].isna()] = "preco invalido"
        motivo[dados["valor_venda"] <= 0] = "preco zerado ou negativo"
        motivo[dados["valor_venda"] > self.preco_maximo] = "preco acima do limite"

        rejeitados = dados[motivo != ""].copy()
        rejeitados["motivo"] = motivo[motivo != ""]
        validos = dados[motivo == ""].copy()
        return validos, rejeitados

    def remover_duplicados(self, dados):
        antes = len(dados)
        dados = dados.drop_duplicates(subset=["cnpj", "produto", "data_coleta"], keep="last")
        return dados, antes - len(dados)
