"""Заготовка DAG для ЛР № 3: Airflow 3.x. Заполните TODO под свой вариант.
Не является выполненным решением или проверенным Docker-развёртыванием.
"""
from __future__ import annotations

from datetime import datetime
from airflow.sdk import dag, task

@dag(
    dag_id="dccas_lw03_business_case",
    start_date=datetime(2026, 1, 1),
    schedule=None,  # ручной запуск учебного DAG
    catchup=False,
    tags=["dccas", "2027", "analytics"],
)
def business_pipeline():
    @task
    def extract() -> str:
        """TODO: загрузите разрешённый публичный CSV и верните путь к файлу."""
        raise NotImplementedError("TODO: extract data")

    @task
    def load_raw(dataset_path: str) -> int:
        """TODO: сохраните исходные записи в PostgreSQL RAW, верните count."""
        raise NotImplementedError("TODO: load RAW")

    @task
    def transform_stg(raw_count: int) -> int:
        """TODO: очистите и нормализуйте записи в STG, зафиксируйте потери."""
        raise NotImplementedError("TODO: transform STG")

    @task
    def quality_check(stg_count: int) -> int:
        """TODO: проверьте уникальность, пропуски, гранулярность и агрегаты."""
        raise NotImplementedError("TODO: data quality")

    @task
    def create_datamart(checked_count: int) -> str:
        """TODO: выполните SQL из отдельного файла и создайте VIEW."""
        raise NotImplementedError("TODO: create VIEW")

    source = extract()
    raw = load_raw(source)
    staging = transform_stg(raw)
    checked = quality_check(staging)
    create_datamart(checked)

business_pipeline()
