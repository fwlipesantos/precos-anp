import pandas as pd


class Tratamento:
    colunas_texto = ["regiao", "uf", "municipio", "revenda", "rua", "numero", "complemento", "bairro", "produto", "unidade", "bandeira"]
    colunas_staging = [
        "regiao", "uf", "municipio", "revenda", "cnpj", "endereco", "bairro", "cep",
        "produto", "data_coleta", "valor_venda", "valor_compra", "unidade", "bandeira", "arquivo",
    ]

    def tratar(self, dados, arquivo):
        dados = dados.copy()

        for coluna in self.colunas_texto:
            dados[coluna] = dados[coluna].fillna("").str.strip().str.upper()

        dados["cnpj"] = self.somente_numeros(dados["cnpj"])
        dados["cep"] = self.somente_numeros(dados["cep"])
        dados["endereco"] = (dados["rua"] + " " + dados["numero"] + " " + dados["complemento"]).str.strip()
        dados["data_coleta"] = pd.to_datetime(dados["data_coleta"], format="%d/%m/%Y", errors="coerce")
        dados["valor_venda"] = self.numero(dados["valor_venda"])
        dados["valor_compra"] = self.numero(dados["valor_compra"])
        dados["arquivo"] = arquivo

        return dados[self.colunas_staging]

    def somente_numeros(self, coluna):
        return coluna.fillna("").str.replace(r"\D", "", regex=True)

    def numero(self, coluna):
        return pd.to_numeric(coluna.fillna("").str.replace(",", ".", regex=False), errors="coerce")
