merge into dim_data d
using (
    select distinct data_coleta as data
    from stg_preco
) s
on (d.data = s.data)
when not matched then
    insert (data, ano, mes, dia, trimestre, semestre, dia_semana)
    values (
        s.data,
        extract(year from s.data),
        extract(month from s.data),
        extract(day from s.data),
        to_number(to_char(s.data, 'Q')),
        case when extract(month from s.data) <= 6 then 1 else 2 end,
        trim(to_char(s.data, 'DAY', 'NLS_DATE_LANGUAGE=PORTUGUESE'))
    )
