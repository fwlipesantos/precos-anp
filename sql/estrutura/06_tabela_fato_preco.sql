create table fato_preco (
    data_coleta   date not null references dim_data (data),
    id_posto      number not null references dim_posto (id_posto),
    id_produto    number not null references dim_produto (id_produto),
    valor_venda   number(10,3),
    valor_compra  number(10,3),
    arquivo       varchar2(100),
    carregado_em  timestamp default systimestamp,
    constraint pk_fato_preco primary key (data_coleta, id_posto, id_produto)
)
partition by range (data_coleta) interval (numtoyminterval(1, 'MONTH'))
(partition p_inicio values less than (date '2000-01-01'))
