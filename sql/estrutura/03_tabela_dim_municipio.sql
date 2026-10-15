create table dim_municipio (
    id_municipio  number generated always as identity primary key,
    regiao        varchar2(2),
    uf            varchar2(2) not null,
    municipio     varchar2(100) not null,
    constraint uk_dim_municipio unique (uf, municipio)
)
