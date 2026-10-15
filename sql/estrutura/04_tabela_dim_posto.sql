create table dim_posto (
    id_posto      number generated always as identity primary key,
    cnpj          varchar2(14) not null,
    revenda       varchar2(200),
    endereco      varchar2(300),
    bairro        varchar2(100),
    cep           varchar2(8),
    bandeira      varchar2(100),
    id_municipio  number not null references dim_municipio (id_municipio),
    valido_de     date not null,
    valido_ate    date,
    atual         char(1) default 'S' not null
)
