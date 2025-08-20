{{ config(materialized='table', schema='silver') }}

select
    cast(null as text) as id,
    cast(null as text) as titulo,
    cast(null as text) as autor,
    cast(null as timestamp without time zone) at time zone 'America/Sao_Paulo' as data_de_criacao,
    cast(null as timestamp without time zone) at time zone 'America/Sao_Paulo' as data_conclusao,
    cast(null as text) as status,
    cast(null as text) as empresa_pela_qual_a_nota_foi_emitida,
    cast(null as text) as empresa_solicitante_do_cancelamento,
    cast(null as text) as categoria_do_cancelamento,
    cast(null as text) as justificativa_da_solicitacao_de_cancelamento,
    cast(null as text) as tipo_da_nota,
    cast(null as text) as numero_da_nota,
    cast(null as boolean) as nota_possui_boleto,
    cast(null as timestamp without time zone) at time zone 'America/Sao_Paulo' as ultima_alteracao
where 1=0
