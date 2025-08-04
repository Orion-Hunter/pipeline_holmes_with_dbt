{{ config(materialized='view', schema='gold') }}

SELECT DISTINCT
MD5(TRIM(autor)) as autor_id,
autor 
FROM {{ ref('processos') }}
