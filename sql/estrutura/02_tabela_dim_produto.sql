create table dim_produto (
    id_produto  number generated always as identity primary key,
    produto     varchar2(50) not null,
    unidade     varchar2(20),
    constraint uk_dim_produto unique (produto)
)
