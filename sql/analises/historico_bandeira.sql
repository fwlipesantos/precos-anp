select
    p.cnpj,
    p.revenda,
    p.bandeira,
    p.valido_de,
    p.valido_ate,
    p.atual
from dim_posto p
where p.cnpj in (
    select cnpj
    from dim_posto
    group by cnpj
    having count(*) > 1
)
order by p.cnpj, p.valido_de
