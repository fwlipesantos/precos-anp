create table controle_arquivo (
    arquivo     varchar2(100) primary key,
    hash        varchar2(64) not null,
    status      varchar2(20),
    linhas      number,
    rejeitadas  number,
    duplicadas  number,
    inicio      timestamp,
    fim         timestamp,
    mensagem    varchar2(4000)
)
