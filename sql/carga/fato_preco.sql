merge into fato_preco f
using (
    select
        s.data_coleta,
        p.id_posto,
        pr.id_produto,
        s.valor_venda,
        s.valor_compra,
        s.arquivo
    from stg_preco s
    join dim_produto pr
        on pr.produto = s.produto
    join dim_posto p
        on p.cnpj = s.cnpj
       and s.data_coleta between p.valido_de and nvl(p.valido_ate, date '9999-12-31')
) s
on (f.data_coleta = s.data_coleta and f.id_posto = s.id_posto and f.id_produto = s.id_produto)
when matched then
    update set
        f.valor_venda = s.valor_venda,
        f.valor_compra = s.valor_compra,
        f.arquivo = s.arquivo,
        f.carregado_em = systimestamp
when not matched then
    insert (data_coleta, id_posto, id_produto, valor_venda, valor_compra, arquivo)
    values (s.data_coleta, s.id_posto, s.id_produto, s.valor_venda, s.valor_compra, s.arquivo)
