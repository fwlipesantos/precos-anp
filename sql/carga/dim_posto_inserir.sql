insert into dim_posto (cnpj, revenda, endereco, bairro, cep, bandeira, id_municipio, valido_de, valido_ate, atual)
select
    s.cnpj,
    s.revenda,
    s.endereco,
    s.bairro,
    s.cep,
    s.bandeira,
    s.id_municipio,
    case
        when exists (select 1 from dim_posto h where h.cnpj = s.cnpj) then s.inicio
        else s.primeira_coleta
    end,
    null,
    'S'
from vw_posto_staging s
where not exists (
    select 1
    from dim_posto d
    where d.cnpj = s.cnpj
      and d.atual = 'S'
)
