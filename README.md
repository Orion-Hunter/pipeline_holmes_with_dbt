# 🚀 Data Pipeline - Airflow + dbt + PostgreSQL

Este projeto implementa um **pipeline de dados** utilizando **Apache Airflow** para orquestração, **dbt** para transformação de dados e **PostgreSQL** como Data Warehouse.

O objetivo é organizar os dados em camadas (Silver → Gold), permitindo análises consistentes e escaláveis. Foram usados apenas 2 camadas da Arquitetura Medalhão pois os dados já vêm da fonte estrturuados e requerem poucos tratamentos(conversões de dados, limpezas, etc) para que sejam transformados na camada Gold e disponibilizados para análise.

---

## 📌 Visão Geral

- **Orquestração:** Apache Airflow  
- **Transformação:** dbt  
- **Armazenamento:** PostgreSQL  
- **Infraestrutura:** Docker + Docker Compose  

---

## 🏗️ Arquitetura do Pipeline

```mermaid
flowchart TD
    A[📥 Fonte de Dados] -->|Extract| C[Silver Layer]
    C -->|Modelagem dbt| D[Gold Layer]
    D -->|Consumido por| E[BI / Dashboards]
