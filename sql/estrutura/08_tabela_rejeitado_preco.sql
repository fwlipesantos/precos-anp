create table rejeitado_preco (
    arquivo        varchar2(100),
    linha          number,
    motivo         varchar2(100),
    conteudo       varchar2(4000),
    registrado_em  timestamp default systimestamp
)
