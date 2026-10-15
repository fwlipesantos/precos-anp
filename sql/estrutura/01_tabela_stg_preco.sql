create table stg_preco (
    regiao        varchar2(2),
    uf            varchar2(2),
    municipio     varchar2(100),
    revenda       varchar2(200),
    cnpj          varchar2(14),
    endereco      varchar2(300),
    bairro        varchar2(100),
    cep           varchar2(8),
    produto       varchar2(50),
    data_coleta   date,
    valor_venda   number(10,3),
    valor_compra  number(10,3),
    unidade       varchar2(20),
    bandeira      varchar2(100),
    arquivo       varchar2(100)
)
