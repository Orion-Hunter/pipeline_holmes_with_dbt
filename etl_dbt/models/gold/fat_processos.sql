{{ config(materialized='view', schema='gold') }}

SELECT
    f.id,
    f.titulo,
    (
        SELECT
          d.autor_id
        FROM {{ ref('dim_autor') }} d 
        where 
        TRIM(f.autor)=TRIM(d.autor)  
    ) as autor_id,
    f.data_de_criacao,
    f.data_conclusao, 
    ROUND(EXTRACT(EPOCH FROM (coalesce(f.data_conclusao, current_timestamp) - f.data_de_criacao)) / 3600, 2) AS duracao,
    f.status,
    f.empresa_pela_qual_a_nota_foi_emitida as empresa_pela_qual_a_nota_foi_emitida_id,
    f.empresa_solicitante_do_cancelamento as empresa_solicitante_do_cancelamento_id,
    (
        SELECT
          d.categoria_id
        FROM {{ ref('dim_categoria_cancelamento') }} d 
        where 
        TRIM(f.categoria_do_cancelamento)=TRIM(d.categoria_do_cancelamento)  
    ) as categoria_do_cancelamento_id,
    f.justificativa_da_solicitacao_de_cancelamento,
    f.tipo_da_nota as tipo_da_nota_id,
    f.numero_da_nota,
    f.nota_possui_boleto

FROM {{ref('processos')}} f