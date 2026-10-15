merge into dim_municipio d
using (
    select uf, municipio, max(regiao) as regiao
    from stg_preco
    group by uf, municipio
) s
on (d.uf = s.uf and d.municipio = s.municipio)
when not matched then
    insert (regiao, uf, municipio)
    values (s.regiao, s.uf, s.municipio)
