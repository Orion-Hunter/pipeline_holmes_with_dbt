{{ config(materialized='view', schema='gold') }}


SELECT DISTINCT

empresa_solicitante_do_cancelamento as id, 
CASE 
 when empresa_solicitante_do_cancelamento='644153adca56e3005f4eed69' then 'HMB IMPERATRIZ'
 when empresa_solicitante_do_cancelamento='6568ec4e48ace600568f5c85' then 'BYD IMPERATRIZ'
 when empresa_solicitante_do_cancelamento='644153a1ca56e3005f4eed52' then 'HMB MARABA'
 when empresa_solicitante_do_cancelamento='6441555fd3b01e0050ef2cf0' then 'HMB PARAUAPEBAS'
 when empresa_solicitante_do_cancelamento='644150753e7b520081221a94' then 'GM PARAUAPEBAS'
 when empresa_solicitante_do_cancelamento='64414fad357d92004ae70ff5' then 'GM MARABA'
 when empresa_solicitante_do_cancelamento='646e42c6bc325600908fa12b' then 'INTERMEDIACAO MARABA'
 when empresa_solicitante_do_cancelamento='646e9d265279455383f75787' then 'CORRETORA MBA'
 else empresa_solicitante_do_cancelamento
END as empresa
FROM {{ ref('processos') }}
