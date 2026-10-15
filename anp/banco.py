import logging

import oracledb
import pandas as pd

log = logging.getLogger(__name__)


class Banco:
    colunas_staging = [
        "regiao", "uf", "municipio", "revenda", "cnpj", "endereco", "bairro", "cep",
        "produto", "data_coleta", "valor_venda", "valor_compra", "unidade", "bandeira", "arquivo",
    ]

    def __init__(self, usuario, senha, dsn):
        self.conexao = oracledb.connect(user=usuario, password=senha, dsn=dsn)

    def executar(self, comando, parametros=None):
        with self.conexao.cursor() as cursor:
            cursor.execute(comando, parametros or {})
            return cursor.rowcount

    def consultar(self, comando, parametros=None):
        with self.conexao.cursor() as cursor:
            cursor.execute(comando, parametros or {})
            return cursor.fetchall()

    def executar_script(self, caminho, ignorar_existentes=False):
        with open(caminho, encoding="utf-8") as arquivo:
            comando = arquivo.read().strip()

        try:
            linhas = self.executar(comando)
            log.info("%s: %s linhas", caminho, linhas)
        except oracledb.DatabaseError as erro:
            if ignorar_existentes and "ORA-00955" in str(erro):
                return
            raise

    def carregar_staging(self, dados):
        self.executar("delete from stg_preco")
        linhas = self.para_linhas(dados[self.colunas_staging])
        campos = ", ".join(self.colunas_staging)
        valores = ", ".join(":" + str(posicao + 1) for posicao in range(len(self.colunas_staging)))

        with self.conexao.cursor() as cursor:
            cursor.executemany(f"insert into stg_preco ({campos}) values ({valores})", linhas)

    def salvar_rejeitados(self, arquivo, rejeitados):
        self.executar("delete from rejeitado_preco where arquivo = :arquivo", {"arquivo": arquivo})
        if rejeitados.empty:
            return

        linhas = []
        for posicao, linha in rejeitados.iterrows():
            conteudo = "; ".join(str(valor) for valor in linha.drop("motivo").values)
            linhas.append((arquivo, int(posicao) + 2, linha["motivo"], conteudo[:4000]))

        with self.conexao.cursor() as cursor:
            cursor.executemany(
                "insert into rejeitado_preco (arquivo, linha, motivo, conteudo) values (:1, :2, :3, :4)",
                linhas,
            )

    def para_linhas(self, dados):
        dados = dados.astype(object).where(pd.notna(dados), None)
        linhas = []
        for linha in dados.itertuples(index=False):
            valores = []
            for valor in linha:
                if isinstance(valor, pd.Timestamp):
                    valor = valor.to_pydatetime()
                valores.append(valor)
            linhas.append(valores)
        return linhas

    def confirmar(self):
        self.conexao.commit()

    def desfazer(self):
        self.conexao.rollback()
