import unicodedata

import pandas as pd


class LayoutDesconhecido(Exception):
    pass


class LeitorArquivo:
    mapa = {
        "regiao - sigla": "regiao",
        "regiao": "regiao",
        "estado - sigla": "uf",
        "estado": "uf",
        "municipio": "municipio",
        "revenda": "revenda",
        "cnpj da revenda": "cnpj",
        "cnpj": "cnpj",
        "nome da rua": "rua",
        "numero rua": "numero",
        "complemento": "complemento",
        "bairro": "bairro",
        "cep": "cep",
        "produto": "produto",
        "data da coleta": "data_coleta",
        "valor de venda": "valor_venda",
        "valor de compra": "valor_compra",
        "unidade de medida": "unidade",
        "bandeira": "bandeira",
    }

    obrigatorias = ["uf", "municipio", "revenda", "cnpj", "produto", "data_coleta", "valor_venda"]
    opcionais = ["regiao", "rua", "numero", "complemento", "bairro", "cep", "valor_compra", "unidade", "bandeira"]

    def ler(self, caminho):
        dados = self.abrir(caminho)
        dados.columns = [self.padronizar(coluna) for coluna in dados.columns]
        dados = dados.rename(columns=self.mapa)

        faltando = [coluna for coluna in self.obrigatorias if coluna not in dados.columns]
        if faltando:
            raise LayoutDesconhecido("colunas obrigatorias ausentes: " + ", ".join(faltando))

        for coluna in self.opcionais:
            if coluna not in dados.columns:
                dados[coluna] = None

        return dados[self.obrigatorias + self.opcionais]

    def abrir(self, caminho):
        try:
            return pd.read_csv(caminho, sep=";", dtype=str, encoding="utf-8-sig")
        except UnicodeDecodeError:
            return pd.read_csv(caminho, sep=";", dtype=str, encoding="latin1")

    def padronizar(self, texto):
        texto = unicodedata.normalize("NFKD", texto)
        texto = texto.encode("ascii", "ignore").decode("ascii")
        return texto.strip().lower()
