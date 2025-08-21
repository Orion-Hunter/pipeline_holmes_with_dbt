# 🚀 Data Pipeline - Airflow + dbt + PostgreSQL

Este projeto implementa um **pipeline de dados** utilizando **Apache Airflow** para orquestração, **dbt** para transformação de dados e **PostgreSQL** como Data Warehouse.

O objetivo é organizar os dados 

em camadas (Silver → Gold), permitindo análises consistentes e escaláveis.

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
