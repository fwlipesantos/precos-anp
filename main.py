import argparse
import logging

from anp.baixador import Baixador
from anp.banco import Banco
from anp.carga import CargaDimensional
from anp.configuracao import Configuracao
from anp.controle import ControleArquivos
from anp.estrutura import Estrutura
from anp.leitor import LeitorArquivo
from anp.pipeline import Pipeline
from anp.tratamento import Tratamento
from anp.validacao import Validador


def main():
    parser = argparse.ArgumentParser(description="carga dos precos de combustiveis da anp no oracle")
    parser.add_argument("--arquivo", help="caminho de um arquivo ja baixado")
    parser.add_argument("--ano", type=int, help="ano do arquivo a baixar")
    parser.add_argument("--semestre", type=int, choices=[1, 2], help="semestre do arquivo a baixar")
    parser.add_argument("--reprocessar", action="store_true", help="processa mesmo que o arquivo ja tenha sido carregado")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

    configuracao = Configuracao()
    banco = Banco(configuracao.usuario, configuracao.senha, configuracao.dsn)
    Estrutura(banco, configuracao.pasta_sql).criar()

    if args.arquivo:
        caminho = args.arquivo
    elif args.ano and args.semestre:
        caminho = Baixador(configuracao.url_base, configuracao.pasta_arquivos).baixar(args.ano, args.semestre)
    else:
        parser.error("informe --arquivo ou --ano e --semestre")

    pipeline = Pipeline(
        leitor=LeitorArquivo(),
        tratamento=Tratamento(),
        validador=Validador(),
        banco=banco,
        controle=ControleArquivos(banco),
        carga=CargaDimensional(banco, configuracao.pasta_sql),
    )
    pipeline.processar(caminho, args.reprocessar)


if __name__ == "__main__":
    main()
