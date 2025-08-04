{{ config(materialized='view', schema='gold') }}



SELECT DISTINCT
tipo_da_nota as id,
CASE 
    WHEN  tipo_da_nota='6672c44a297f99007c880c24' THEN 'Serviço'
    WHEN  tipo_da_nota='6672c45597ba5e00790a8c47' THEN 'Veículo'
    WHEN  tipo_da_nota='6672c45ec9c551007d58f2b7' THEN 'Peças'
    WHEN  tipo_da_nota='6672c46773b8840075297047' THEN 'Despesa'
    WHEN  tipo_da_nota='6672c47f97ba5e00790a8c7e' THEN 'Tansferência'
END tipo

FROM {{ref('processos')}}


