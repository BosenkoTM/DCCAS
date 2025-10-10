"""
DAG для анализа президентов США
Вариант задания №30

Автор: Студент
Дата: 2024
"""

from datetime import datetime, timedelta
import pandas as pd
import os
import kaggle
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago

# Конфигурация по умолчанию для DAG
default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Создание DAG
dag = DAG(
    'us_presidents_analysis',
    default_args=default_args,
    description='Анализ президентов США - вариант 30',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['etl', 'us_presidents', 'kaggle', 'variant_30']
)

# Пути к файлам данных
DATA_DIR = '/opt/airflow/dags/data'

def extract_from_kaggle(**context):
    """
    Extract: Скачивание данных о президентах США с Kaggle
    """
    print("Начинаем извлечение данных о президентах США с Kaggle...")
    
    try:
        # Создаем директорию для данных если не существует
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Настройка Kaggle API
        # kaggle.json находится в папке dags
        kaggle_dir = '/opt/airflow/dags'
        os.environ['KAGGLE_CONFIG_DIR'] = kaggle_dir
        
        # Проверяем наличие kaggle.json
        kaggle_json_path = os.path.join(kaggle_dir, 'kaggle.json')
        if not os.path.exists(kaggle_json_path):
            raise FileNotFoundError(f"Файл kaggle.json не найден в {kaggle_json_path}")
        
        print(f"Используем kaggle.json из: {kaggle_json_path}")
        
        # Скачивание датасета
        dataset_name = "harshitagpt/us-presidents"
        print(f"Скачиваем датасет: {dataset_name}")
        
        # Используем kaggle API для скачивания
        import kagglehub
        path = kagglehub.dataset_download(dataset_name)
        print(f"Данные скачаны в: {path}")
        
        # Копируем файл в нашу рабочую директорию
        import shutil
        source_file = os.path.join(path, "us_presidents.csv")
        if os.path.exists(source_file):
            dest_file = os.path.join(DATA_DIR, "us_presidents.csv")
            shutil.copy2(source_file, dest_file)
            print(f"Файл скопирован в: {dest_file}")
        else:
            # Если файл не найден, попробуем найти CSV файлы в скачанной директории
            csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
            if csv_files:
                source_file = os.path.join(path, csv_files[0])
                dest_file = os.path.join(DATA_DIR, "us_presidents.csv")
                shutil.copy2(source_file, dest_file)
                print(f"Файл {csv_files[0]} скопирован в: {dest_file}")
            else:
                raise FileNotFoundError("CSV файл не найден в скачанном датасете")
        
        # Читаем и проверяем данные
        df = pd.read_csv(dest_file)
        print(f"Загружено {len(df)} записей о президентах")
        print("Первые 5 записей:")
        print(df.head())
        print("Структура данных:")
        print(df.info())
        
        # Сохранение информации о файле для следующих задач
        context['task_instance'].xcom_push(key='data_file_path', value=dest_file)
        context['task_instance'].xcom_push(key='records_count', value=len(df))
        
        print("Данные о президентах успешно извлечены с Kaggle")
        return f"Извлечено {len(df)} записей о президентах США"
        
    except Exception as e:
        print(f"Ошибка при извлечении данных с Kaggle: {str(e)}")
        raise

def load_to_postgres(**context):
    """
    Load: Загрузка сырых данных в PostgreSQL
    """
    print("Начинаем загрузку данных в PostgreSQL...")
    
    try:
        # Получение пути к файлу данных
        data_file_path = context['task_instance'].xcom_pull(key='data_file_path', task_ids='extract_from_kaggle')
        
        if not data_file_path or not os.path.exists(data_file_path):
            raise ValueError("Файл данных не найден")
        
        # Чтение CSV файла
        df = pd.read_csv(data_file_path)
        print(f"Загружено {len(df)} записей из файла")
        
        # Подключение к PostgreSQL
        postgres_hook = PostgresHook(postgres_conn_id='analytics_postgres')
        
        # Создание таблицы для сырых данных
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS raw_us_presidents (
            id SERIAL PRIMARY KEY,
            s_no INTEGER,
            start_date TEXT,
            end_date TEXT,
            president TEXT,
            prior TEXT,
            party TEXT,
            vice TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        postgres_hook.run(create_table_sql)
        print("Таблица raw_us_presidents создана")
        
        # Очистка таблицы перед загрузкой новых данных
        postgres_hook.run("DELETE FROM raw_us_presidents")
        
        # Подготовка данных для вставки
        df_clean = df.copy()
        
        # Переименование колонок для соответствия схеме БД
        column_mapping = {
            'S.No.': 's_no',
            'start': 'start_date',
            'end': 'end_date',
            'president': 'president',
            'prior': 'prior',
            'party': 'party',
            'vice': 'vice'
        }
        
        # Переименовываем колонки если они существуют
        for old_col, new_col in column_mapping.items():
            if old_col in df_clean.columns:
                df_clean = df_clean.rename(columns={old_col: new_col})
        
        # Удаляем колонки, которых нет в схеме
        allowed_columns = ['s_no', 'start_date', 'end_date', 'president', 'prior', 'party', 'vice']
        df_clean = df_clean[[col for col in df_clean.columns if col in allowed_columns]]
        
        # Загрузка данных в PostgreSQL
        postgres_hook.insert_rows(
            table='raw_us_presidents',
            rows=df_clean.values.tolist(),
            target_fields=list(df_clean.columns)
        )
        
        print(f"Успешно загружено {len(df_clean)} записей в PostgreSQL")
        
        # Проверка загруженных данных
        check_query = "SELECT COUNT(*) as count FROM raw_us_presidents"
        result = postgres_hook.get_first(check_query)
        print(f"Проверка: в таблице {result[0]} записей")
        
        return f"Загружено {len(df_clean)} записей в PostgreSQL"
        
    except Exception as e:
        print(f"Ошибка при загрузке в PostgreSQL: {str(e)}")
        raise

# Определение задач DAG

# Extract задача
extract_task = PythonOperator(
    task_id='extract_from_kaggle',
    python_callable=extract_from_kaggle,
    dag=dag,
    doc_md="""
    ### Извлечение данных с Kaggle
    Скачивает датасет о президентах США с Kaggle API.
    """
)

# Load задача
load_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    dag=dag,
    doc_md="""
    ### Загрузка в PostgreSQL
    Загружает сырые данные о президентах в таблицу raw_us_presidents.
    """
)

# Transform задача - создание витрины данных
create_datamart_task = PostgresOperator(
    task_id='create_datamart',
    postgres_conn_id='analytics_postgres',
    sql='datamart_variant_30.sql',
    dag=dag,
    doc_md="""
    ### Создание витрины данных
    Создает VIEW с полями: president, party, inauguration_age, years_in_office.
    """
)

# Определение зависимостей между задачами
extract_task >> load_task >> create_datamart_task
