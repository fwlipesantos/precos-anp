# contexto do projeto

Leia este arquivo antes de qualquer alteração.

## objetivo

Portfólio do Felipe Santos (Data Engineer) para uma vaga de Engenheiro de Dados / DevOps que usa Python modular, Airflow 3, SQL avançado com Oracle, Rancher/Kubernetes on-premise, ambientes dev, hml e prod e promoção por pull request.

O portfólio equilibra engenharia de dados (modelagem, carga incremental, SCD2, SQL, qualidade) com operação (ambientes, CI/CD, alertas, investigação de falhas).

## os três projetos

1. **pipeline de preços da ANP** (este repositório): modelo dimensional no Oracle, carga incremental com MERGE, SCD tipo 2 nos postos, quarentena de registros inválidos e controle de arquivos.
2. **orquestração e entrega**: DAGs no Airflow 3, imagem Docker, dev, hml e prod no Kubernetes com Rancher e CI/CD no GitHub Actions.
3. **qualidade e confiabilidade**: testes de qualidade por camada, alertas de falha, atraso e volume, ficha de cada processo e casos de falha investigados.

## estilo de código

- código limpo, organizado em classes, simples de entender
- sem sintaxe complicada: nada de compreensão aninhada, truques de uma linha ou decoradores próprios
- nomes de variáveis, funções, arquivos e mensagens em português e em minúsculo
- classes com inicial maiúscula (padrão do Python), o resto em minúsculo
- pouquíssimos comentários, o nome das coisas deve explicar
- cada classe com uma responsabilidade só

## estado atual

- feito: leitura com mapa de layouts, tratamento, validação com quarentena, staging, dimensões, SCD2 de posto, fato particionada, controle de arquivos e 10 testes passando
- não testado contra um Oracle real ainda: rodar `docker compose up -d` e `python main.py --arquivo dados/exemplo/ca-amostra.csv`
- projetos 2 e 3 prontos nos repositórios esteira-anp e qualidade-anp
