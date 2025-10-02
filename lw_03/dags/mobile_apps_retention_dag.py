"""
DAG для анализа коэффициента удержания мобильных приложений
Вариант задания №30

Автор: Студент
Дата: 2024
"""

from datetime import datetime, timedelta
import pandas as pd
import json
import sqlite3
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago

# Конфигурация по умолчанию для DAG
default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email': ['test@example.com']
}

# Создание DAG
dag = DAG(
    'mobile_apps_retention_analysis',
    default_args=default_args,
    description='Анализ коэффициента удержания мобильных приложений',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['etl', 'mobile_apps', 'retention', 'variant_30']
)

# Пути к файлам данных
DATA_DIR = '/opt/airflow/dags/data'
DB_PATH = '/opt/airflow/mobile_apps_retention.db'

def extract_apps_data(**context):
    """
    Extract: Чтение данных о приложениях из CSV файла
    """
    print("Начинаем извлечение данных о приложениях из CSV...")
    
    csv_path = os.path.join(DATA_DIR, 'apps.csv')
    
    try:
        # Чтение CSV файла
        apps_df = pd.read_csv(csv_path)
        print(f"Загружено {len(apps_df)} записей о приложениях")
        print("Первые 5 записей:")
        print(apps_df.head())
        
        # Сохранение данных для следующих задач
        apps_data = apps_df.to_dict('records')
        context['task_instance'].xcom_push(key='apps_data', value=apps_data)
        
        print("Данные о приложениях успешно извлечены и сохранены в XCom")
        return f"Извлечено {len(apps_df)} записей о приложениях"
        
    except Exception as e:
        print(f"Ошибка при извлечении данных о приложениях: {str(e)}")
        raise

def extract_installs_data(**context):
    """
    Extract: Чтение данных об установках из Excel файла
    """
    print("Начинаем извлечение данных об установках из Excel...")
    
    excel_path = os.path.join(DATA_DIR, 'installs.xlsx')
    
    try:
        # Чтение Excel файла
        installs_df = pd.read_excel(excel_path)
        print(f"Загружено {len(installs_df)} записей об установках")
        print("Первые 5 записей:")
        print(installs_df.head())
        
        # Сохранение данных для следующих задач
        installs_data = installs_df.to_dict('records')
        context['task_instance'].xcom_push(key='installs_data', value=installs_data)
        
        print("Данные об установках успешно извлечены и сохранены в XCom")
        return f"Извлечено {len(installs_df)} записей об установках"
        
    except Exception as e:
        print(f"Ошибка при извлечении данных об установках: {str(e)}")
        raise

def extract_uninstalls_data(**context):
    """
    Extract: Чтение данных об удалениях из JSON файла
    """
    print("Начинаем извлечение данных об удалениях из JSON...")
    
    json_path = os.path.join(DATA_DIR, 'uninstalls.json')
    
    try:
        # Чтение JSON файла
        with open(json_path, 'r', encoding='utf-8') as f:
            uninstalls_data = json.load(f)
        
        uninstalls_df = pd.DataFrame(uninstalls_data)
        print(f"Загружено {len(uninstalls_df)} записей об удалениях")
        print("Первые 5 записей:")
        print(uninstalls_df.head())
        
        # Сохранение данных для следующих задач
        context['task_instance'].xcom_push(key='uninstalls_data', value=uninstalls_data)
        
        print("Данные об удалениях успешно извлечены и сохранены в XCom")
        return f"Извлечено {len(uninstalls_df)} записей об удалениях"
        
    except Exception as e:
        print(f"Ошибка при извлечении данных об удалениях: {str(e)}")
        raise

def transform_data(**context):
    """
    Transform: Консолидация данных и расчет коэффициента удержания
    """
    print("Начинаем трансформацию данных...")
    
    try:
        # Получение данных из предыдущих задач
        apps_data = context['task_instance'].xcom_pull(key='apps_data', task_ids='extract_apps')
        installs_data = context['task_instance'].xcom_pull(key='installs_data', task_ids='extract_installs')
        uninstalls_data = context['task_instance'].xcom_pull(key='uninstalls_data', task_ids='extract_uninstalls')
        
        # Преобразование в DataFrame
        apps_df = pd.DataFrame(apps_data)
        installs_df = pd.DataFrame(installs_data)
        uninstalls_df = pd.DataFrame(uninstalls_data)
        
        print("Данные успешно получены из XCom")
        print(f"Приложения: {len(apps_df)} записей")
        print(f"Установки: {len(installs_df)} записей")
        print(f"Удаления: {len(uninstalls_df)} записей")
        
        # Объединение данных
        # Сначала объединяем приложения с установками
        merged_df = pd.merge(apps_df, installs_df, on='app_id', how='inner')
        print(f"После объединения с установками: {len(merged_df)} записей")
        
        # Затем объединяем с удалениями
        final_df = pd.merge(merged_df, uninstalls_df, on='app_id', how='inner')
        print(f"После объединения с удалениями: {len(final_df)} записей")
        
        # Расчет коэффициента удержания по категориям
        print("Начинаем расчет коэффициента удержания...")
        
        retention_analysis = final_df.groupby('category').agg({
            'installs_count': 'sum',
            'uninstalls_count': 'sum'
        }).reset_index()
        
        # Переименование колонок для ясности
        retention_analysis.columns = ['category', 'total_installs', 'total_uninstalls']
        
        # Расчет коэффициента удержания
        retention_analysis['retention_rate'] = (
            (retention_analysis['total_installs'] - retention_analysis['total_uninstalls']) / 
            retention_analysis['total_installs'] * 100
        ).round(2)
        
        # Добавление дополнительных метрик
        retention_analysis['retained_users'] = (
            retention_analysis['total_installs'] - retention_analysis['total_uninstalls']
        )
        retention_analysis['churn_rate'] = (
            retention_analysis['total_uninstalls'] / retention_analysis['total_installs'] * 100
        ).round(2)
        
        print("Результаты анализа коэффициента удержания:")
        print(retention_analysis)
        
        # Сохранение результатов для загрузки в БД
        result_data = retention_analysis.to_dict('records')
        context['task_instance'].xcom_push(key='retention_analysis', value=result_data)
        
        print("Трансформация данных завершена успешно")
        return f"Проанализировано {len(retention_analysis)} категорий приложений"
        
    except Exception as e:
        print(f"Ошибка при трансформации данных: {str(e)}")
        raise

def load_to_database(**context):
    """
    Load: Загрузка результатов анализа в SQLite базу данных
    """
    print("Начинаем загрузку данных в базу данных...")
    
    try:
        # Получение результатов анализа
        retention_data = context['task_instance'].xcom_pull(
            key='retention_analysis', 
            task_ids='transform_data'
        )
        
        if not retention_data:
            raise ValueError("Нет данных для загрузки в базу данных")
        
        # Создание DataFrame из результатов
        retention_df = pd.DataFrame(retention_data)
        
        # Подключение к SQLite базе данных
        conn = sqlite3.connect(DB_PATH)
        
        try:
            # Создание таблицы если она не существует
            create_table_query = """
            CREATE TABLE IF NOT EXISTS retention_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                total_installs INTEGER NOT NULL,
                total_uninstalls INTEGER NOT NULL,
                retained_users INTEGER NOT NULL,
                retention_rate REAL NOT NULL,
                churn_rate REAL NOT NULL,
                analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            conn.execute(create_table_query)
            
            # Очистка таблицы перед загрузкой новых данных
            conn.execute("DELETE FROM retention_analysis")
            
            # Загрузка данных в таблицу
            retention_df.to_sql('retention_analysis', conn, if_exists='append', index=False)
            
            # Подтверждение транзакции
            conn.commit()
            
            print(f"Успешно загружено {len(retention_df)} записей в базу данных")
            
            # Проверка загруженных данных
            verification_query = "SELECT * FROM retention_analysis ORDER BY retention_rate DESC"
            result = pd.read_sql_query(verification_query, conn)
            print("Проверка загруженных данных:")
            print(result)
            
        finally:
            conn.close()
        
        print("Загрузка в базу данных завершена успешно")
        return f"Загружено {len(retention_df)} записей в SQLite базу данных"
        
    except Exception as e:
        print(f"Ошибка при загрузке в базу данных: {str(e)}")
        raise

def generate_report(**context):
    """
    Генерация отчета с результатами анализа
    """
    print("Генерируем отчет с результатами анализа...")
    
    try:
        # Получение данных из базы данных
        conn = sqlite3.connect(DB_PATH)
        
        try:
            query = """
            SELECT 
                category,
                total_installs,
                total_uninstalls,
                retained_users,
                retention_rate,
                churn_rate
            FROM retention_analysis 
            ORDER BY retention_rate DESC
            """
            
            result_df = pd.read_sql_query(query, conn)
            
            # Формирование отчета
            report = f"""
            ОТЧЕТ ПО АНАЛИЗУ КОЭФФИЦИЕНТА УДЕРЖАНИЯ МОБИЛЬНЫХ ПРИЛОЖЕНИЙ
            ================================================================
            
            Дата анализа: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Общее количество категорий: {len(result_df)}
            
            РЕЗУЛЬТАТЫ ПО КАТЕГОРИЯМ:
            """
            
            for _, row in result_df.iterrows():
                report += f"""
            
            Категория: {row['category']}
            - Общее количество установок: {row['total_installs']:,}
            - Общее количество удалений: {row['total_uninstalls']:,}
            - Удержанные пользователи: {row['retained_users']:,}
            - Коэффициент удержания: {row['retention_rate']:.2f}%
            - Коэффициент оттока: {row['churn_rate']:.2f}%
            """
            
            # Добавление общей статистики
            total_installs = result_df['total_installs'].sum()
            total_uninstalls = result_df['total_uninstalls'].sum()
            overall_retention = (total_installs - total_uninstalls) / total_installs * 100
            
            report += f"""
            
            ОБЩАЯ СТАТИСТИКА:
            - Общее количество установок: {total_installs:,}
            - Общее количество удалений: {total_uninstalls:,}
            - Общий коэффициент удержания: {overall_retention:.2f}%
            
            РЕКОМЕНДАЦИИ:
            """
            
            # Добавление рекомендаций на основе анализа
            best_category = result_df.iloc[0]
            worst_category = result_df.iloc[-1]
            
            report += f"""
            - Лучший показатель удержания у категории "{best_category['category']}" ({best_category['retention_rate']:.2f}%)
            - Требует внимания категория "{worst_category['category']}" ({worst_category['retention_rate']:.2f}%)
            - Рекомендуется изучить успешные практики категории "{best_category['category']}"
            """
            
            print("Отчет сгенерирован:")
            print(report)
            
            # Сохранение отчета для email
            context['task_instance'].xcom_push(key='report', value=report)
            
        finally:
            conn.close()
            
        return "Отчет успешно сгенерирован"
        
    except Exception as e:
        print(f"Ошибка при генерации отчета: {str(e)}")
        raise

# Определение задач DAG

# Extract задачи
extract_apps_task = PythonOperator(
    task_id='extract_apps',
    python_callable=extract_apps_data,
    dag=dag,
    doc_md="""
    ### Извлечение данных о приложениях
    Читает CSV файл с информацией о приложениях и их категориях.
    """
)

extract_installs_task = PythonOperator(
    task_id='extract_installs',
    python_callable=extract_installs_data,
    dag=dag,
    doc_md="""
    ### Извлечение данных об установках
    Читает Excel файл с данными о количестве установок приложений.
    """
)

extract_uninstalls_task = PythonOperator(
    task_id='extract_uninstalls',
    python_callable=extract_uninstalls_data,
    dag=dag,
    doc_md="""
    ### Извлечение данных об удалениях
    Читает JSON файл с данными о количестве удалений приложений.
    """
)

# Transform задача
transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
    doc_md="""
    ### Трансформация данных
    Объединяет данные из всех источников и рассчитывает коэффициент удержания по категориям.
    """
)

# Load задача
load_task = PythonOperator(
    task_id='load_to_database',
    python_callable=load_to_database,
    dag=dag,
    doc_md="""
    ### Загрузка в базу данных
    Сохраняет результаты анализа в SQLite базу данных.
    """
)

# Генерация отчета
report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
    doc_md="""
    ### Генерация отчета
    Создает детальный отчет с результатами анализа коэффициента удержания.
    """
)

# Email уведомление
email_task = EmailOperator(
    task_id='send_email_notification',
    to=['test@example.com'],
    subject='Анализ коэффициента удержания мобильных приложений - Завершен',
    html_content="""
    <h3>Анализ коэффициента удержания мобильных приложений завершен успешно!</h3>
    <p>DAG: mobile_apps_retention_analysis</p>
    <p>Дата выполнения: {{ ds }}</p>
    <p>Все задачи выполнены без ошибок.</p>
    <p>Результаты сохранены в базе данных SQLite.</p>
    <br>
    <p>Для просмотра детального отчета проверьте логи задачи generate_report.</p>
    """,
    dag=dag
)

# Определение зависимостей между задачами
# Extract задачи выполняются параллельно
[extract_apps_task, extract_installs_task, extract_uninstalls_task] >> transform_task

# Transform -> Load -> Report -> Email (последовательно)
transform_task >> load_task >> report_task >> email_task
