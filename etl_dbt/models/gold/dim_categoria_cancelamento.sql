{{ config(materialized='view', schema='gold') }}

SELECT DISTINCT
MD5(TRIM(categoria_do_cancelamento)) as categoria_id,
categoria_do_cancelamento
FROM {{ ref('processos') }}
WHERE
categoria_do_cancelamento is not NULL
