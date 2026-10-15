create or replace view vw_posto_staging as
select cnpj, revenda, endereco, bairro, cep, bandeira, id_municipio, inicio, primeira_coleta
from (
    select
        s.cnpj,
        s.revenda,
        s.endereco,
        s.bairro,
        s.cep,
        s.bandeira,
        m.id_municipio,
        row_number() over (partition by s.cnpj order by s.data_coleta desc) as ordem,
        min(s.data_coleta) over (partition by s.cnpj, s.revenda, s.endereco, s.bandeira) as inicio,
        min(s.data_coleta) over (partition by s.cnpj) as primeira_coleta
    from stg_preco s
    join dim_municipio m
        on m.uf = s.uf
       and m.municipio = s.municipio
)
where ordem = 1
