with mensal as (
    select
        m.uf,
        pr.produto,
        trunc(f.data_coleta, 'MM') as mes,
        round(avg(f.valor_venda), 3) as preco_medio,
        count(*) as coletas
    from fato_preco f
    join dim_posto p on p.id_posto = f.id_posto
    join dim_municipio m on m.id_municipio = p.id_municipio
    join dim_produto pr on pr.id_produto = f.id_produto
    group by m.uf, pr.produto, trunc(f.data_coleta, 'MM')
)
select
    uf,
    produto,
    mes,
    preco_medio,
    coletas,
    round(preco_medio - lag(preco_medio) over (partition by uf, produto order by mes), 3) as variacao_mes,
    round(avg(preco_medio) over (partition by uf, produto order by mes rows between 2 preceding and current row), 3) as media_movel_3m,
    rank() over (partition by produto, mes order by preco_medio desc) as ranking_mais_caro
from mensal
order by produto, mes, ranking_mais_caro
