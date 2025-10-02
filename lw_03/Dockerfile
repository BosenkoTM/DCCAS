FROM apache/airflow:2.5.0-python3.8

# Установка дополнительных зависимостей
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Установка Python пакетов
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
