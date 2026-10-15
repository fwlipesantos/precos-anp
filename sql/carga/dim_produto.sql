merge into dim_produto d
using (
    select produto, max(unidade) as unidade
    from stg_preco
    group by produto
) s
on (d.produto = s.produto)
when matched then
    update set d.unidade = s.unidade
    where decode(d.unidade, s.unidade, 0, 1) = 1
when not matched then
    insert (produto, unidade)
    values (s.produto, s.unidade)
