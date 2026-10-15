create table dim_data (
    data        date primary key,
    ano         number(4),
    mes         number(2),
    dia         number(2),
    trimestre   number(1),
    semestre    number(1),
    dia_semana  varchar2(20)
)
