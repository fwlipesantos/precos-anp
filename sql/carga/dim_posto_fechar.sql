merge into dim_posto d
using vw_posto_staging s
on (d.cnpj = s.cnpj and d.atual = 'S')
when matched then
    update set
        d.valido_ate = s.inicio - 1,
        d.atual = 'N'
    where decode(d.revenda, s.revenda, 0, 1) = 1
       or decode(d.endereco, s.endereco, 0, 1) = 1
       or decode(d.bandeira, s.bandeira, 0, 1) = 1
