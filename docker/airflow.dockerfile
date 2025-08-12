FROM apache/airflow:2.9.0-python3.12

# Defina as variáveis de ambiente para o Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Copie os arquivos locais para dentro do container
COPY app ${AIRFLOW_HOME}/app


COPY app/dags/ ${AIRFLOW_HOME}/dags/
COPY init/ ${AIRFLOW_HOME}/init/         



# Instale dependências adicionais do projeto
USER root
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean
RUN chmod +x init/init_airflow.sh
RUN chmod +x /opt/airflow/init/init_airflow.sh


USER airflow
# Instale pacotes Python adicionais

RUN pip install -Iv poetry==1.3.1
RUN pip install --upgrade pip

RUN poetry config virtualenvs.create false

RUN poetry config experimental.new-installer false

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install

WORKDIR /opt/airflow
ENTRYPOINT ["/opt/airflow/init/init_airflow.sh"]
#CMD ["webserver"]
