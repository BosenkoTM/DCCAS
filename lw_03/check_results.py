#!/usr/bin/env python3
"""
Скрипт для проверки результатов анализа в SQLite базе данных
"""

import sqlite3
import pandas as pd
import os

DB_PATH = 'mobile_apps_retention.db'

def check_database():
    """Проверка результатов в базе данных"""
    
    if not os.path.exists(DB_PATH):
        print(f"База данных {DB_PATH} не найдена!")
        print("Убедитесь, что DAG был выполнен успешно.")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Проверка существования таблицы
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Найденные таблицы в базе данных:")
        for table in tables:
            print(f"  - {table[0]}")
        
        if ('retention_analysis',) not in tables:
            print("\nТаблица 'retention_analysis' не найдена!")
            return
        
        # Чтение результатов анализа
        query = """
        SELECT 
            category,
            total_installs,
            total_uninstalls,
            retained_users,
            retention_rate,
            churn_rate,
            analysis_date
        FROM retention_analysis 
        ORDER BY retention_rate DESC
        """
        
        df = pd.read_sql_query(query, conn)
        
        print(f"\nРезультаты анализа коэффициента удержания:")
        print("=" * 80)
        print(df.to_string(index=False))
        
        # Общая статистика
        total_installs = df['total_installs'].sum()
        total_uninstalls = df['total_uninstalls'].sum()
        overall_retention = (total_installs - total_uninstalls) / total_installs * 100
        
        print(f"\nОбщая статистика:")
        print(f"  Общее количество установок: {total_installs:,}")
        print(f"  Общее количество удалений: {total_uninstalls:,}")
        print(f"  Общий коэффициент удержания: {overall_retention:.2f}%")
        
        # Лучшая и худшая категории
        best_category = df.iloc[0]
        worst_category = df.iloc[-1]
        
        print(f"\nЛучший показатель удержания:")
        print(f"  {best_category['category']}: {best_category['retention_rate']:.2f}%")
        
        print(f"\nТребует внимания:")
        print(f"  {worst_category['category']}: {worst_category['retention_rate']:.2f}%")
        
        conn.close()
        
    except Exception as e:
        print(f"Ошибка при проверке базы данных: {str(e)}")

if __name__ == "__main__":
    check_database()
