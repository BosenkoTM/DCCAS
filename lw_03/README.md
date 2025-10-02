# Лабораторная работа №3. Оркестрация ETL-процессов с Apache Airflow

## Цель работы
Освоить практические навыки проектирования и автоматизации ETL-процессов (Extract, Transform, Load) с использованием Apache Airflow. Научиться создавать конвейеры данных (DAG), которые извлекают информацию из разнородных источников, выполняют их консолидацию и трансформацию с помощью Python, и загружают результат в целевую базу данных с отправкой уведомлений.

## Оборудование и ПО
- Система контейнеризации Docker и Docker Compose
- Apache Airflow (разворачивается в Docker)
- База данных SQLite
- Python 3.x с библиотеками pandas, openpyxl
- Email-сервис для настройки уведомлений (MailHog)

## Вариант задания №30. Мобильные приложения - Коэффициент удержания

### Описание задачи
Рассчитать "коэффициент удержания" (Retention Rate) для каждой категории приложений на основе данных:
- **Файл 1 (CSV)**: Мобильные приложения - `app_id`, `category`
- **Файл 2 (Excel)**: Установки - `app_id`, `installs_count`
- **Файл 3 (JSON)**: Удаления - `app_id`, `uninstalls_count`

**Формула коэффициента удержания**: `Retention Rate = (Installs - Uninstalls) / Installs * 100%`

## Пошаговая инструкция выполнения

### Шаг 1: Подготовка окружения

1. **Клонирование репозитория** (если еще не сделано):
   ```bash
   git clone https://github.com/BosenkoTM/DCCAS.git
   cd DCCAS/lw_03
   ```

2. **Запуск всех сервисов**:
   ```bash
   # Для Docker Compose v2 (рекомендуется)
   docker compose up -d
   
   # Для Docker Compose v1
   docker-compose up -d
   
   # Если нужны права администратора (Linux)
   sudo docker compose up -d
   ```

3. **Проверка доступности сервисов**:
   - Apache Airflow: http://localhost:8080 (admin/admin)
   - MailHog (почтовый сервис): http://localhost:8025
   - PostgreSQL: localhost:5432

### Шаг 2: Создание тестовых данных

Создайте папку `dags/data` и поместите в неё тестовые файлы:

#### apps.csv
```csv
app_id,category
1,Games
2,Social
3,Games
4,Productivity
5,Social
6,Games
7,Education
8,Productivity
9,Games
10,Education
```

#### installs.xlsx
Создайте Excel файл с данными:
```
app_id | installs_count
1      | 10000
2      | 5000
3      | 8000
4      | 3000
5      | 7000
6      | 12000
7      | 2000
8      | 4000
9      | 9000
10     | 1500
```

#### uninstalls.json
```json
[
  {"app_id": 1, "uninstalls_count": 2000},
  {"app_id": 2, "uninstalls_count": 1500},
  {"app_id": 3, "uninstalls_count": 1600},
  {"app_id": 4, "uninstalls_count": 600},
  {"app_id": 5, "uninstalls_count": 2100},
  {"app_id": 6, "uninstalls_count": 2400},
  {"app_id": 7, "uninstalls_count": 400},
  {"app_id": 8, "uninstalls_count": 800},
  {"app_id": 9, "uninstalls_count": 1800},
  {"app_id": 10, "uninstalls_count": 300}
]
```

### Шаг 3: Создание DAG для варианта №30

Создайте файл `dags/mobile_apps_retention_dag.py` с реализацией ETL-процесса.

### Шаг 4: Тестирование и запуск

1. **Активация DAG**:
   - Откройте веб-интерфейс Airflow: http://localhost:8080
   - Найдите DAG `mobile_apps_retention_analysis`
   - Включите его переключателем слева от названия

2. **Запуск DAG**:
   - Нажмите на название DAG
   - Нажмите кнопку "Trigger DAG" для ручного запуска

3. **Мониторинг выполнения**:
   - Следите за статусом задач в Graph View
   - Проверяйте логи в случае ошибок (кликните на задачу → View Log)

4. **Проверка результатов**:
   - Убедитесь, что данные загрузились в SQLite
   - Проверьте email-уведомление в MailHog: http://localhost:8025

### Работа с MailHog (проверка email-уведомлений)

MailHog - это инструмент для тестирования email-отправки без реальной доставки писем.

#### Как проверить email-уведомления:

1. **Откройте веб-интерфейс MailHog**:
   ```
   http://localhost:8025
   ```

2. **После успешного выполнения DAG** вы увидите:
   - 📧 **Новое письмо** в списке сообщений
   - **От**: `airflow@example.com`
   - **Кому**: `test@example.com`
   - **Тема**: "Анализ коэффициента удержания мобильных приложений - Завершен"

3. **Кликните на письмо** для просмотра:
   - HTML-содержимое с отчетом о выполнении
   - Дата и время отправки
   - Детали выполнения DAG

4. **Если письмо не пришло**:
   - Проверьте, что DAG выполнился до конца (все задачи зеленые)
   - Убедитесь, что MailHog запущен: `docker ps | grep mailhog`
   - Проверьте логи задачи `send_email_notification`

#### Интерфейс MailHog:
```
┌─────────────────────────────────────────┐
│  MailHog Web Interface                  │
│  http://localhost:8025                  │
├─────────────────────────────────────────┤
│  📧 Inbox (1)                          │
│  ┌─────────────────────────────────────┐ │
│  │ ✉️  Анализ коэффициента удержания   │ │
│  │     airflow@example.com             │ │
│  │     2024-10-02 15:30:45            │ │
│  └─────────────────────────────────────┘ │
│                                         │
│  📄 Message Preview:                    │
│  Анализ завершен успешно!              │
│  Все задачи выполнены без ошибок.      │
└─────────────────────────────────────────┘
```

**💡 Совет**: MailHog сохраняет все письма до перезапуска контейнера, поэтому вы можете просматривать историю всех тестовых отправок.

### Шаг 5: Проверка результатов в базе данных

Подключитесь к контейнеру и проверьте данные в SQLite:

```bash
# Подключение к контейнеру scheduler
docker exec -it <scheduler_container_id> bash

# Проверка данных в SQLite
sqlite3 /opt/airflow/mobile_apps_retention.db
.tables
SELECT * FROM retention_analysis;
.quit
```

### Шаг 6: Проверка результатов (дополнительно)

Для удобной проверки результатов можно использовать скрипт:

```bash
# Установка зависимостей (если еще не установлены)
pip install -r requirements.txt

# Запуск скрипта проверки результатов
python check_results.py
```

### Шаг 7: Остановка сервисов

После завершения работы остановите все сервисы:

```bash
# Для Docker Compose v2
docker compose down

# Для Docker Compose v1
docker-compose down
```

## Полная очистка проекта после работы

### Быстрая очистка (сохранить данные)

Если вы хотите остановить контейнеры, но сохранить данные для будущих запусков:

```bash
# Остановка всех сервисов
docker compose down

# Проверка, что контейнеры остановлены
docker ps -a
```

### Полная очистка (удалить все данные)

⚠️ **ВНИМАНИЕ**: Следующие команды полностью удалят все данные проекта!

#### 1. Остановка и удаление контейнеров с томами

```bash
# Остановка и удаление контейнеров вместе с томами
docker compose down -v

# Альтернативно для полной очистки
docker compose down --volumes --remove-orphans
```

#### 2. Удаление Docker образов (опционально)

```bash
# Просмотр используемых образов
docker images | grep -E "(airflow|postgres|mailhog)"

# Удаление конкретных образов (замените на актуальные IMAGE ID)
docker rmi apache/airflow:2.5.0-python3.8
docker rmi postgres:12-alpine
docker rmi mailhog/mailhog:latest

# Или удаление всех неиспользуемых образов
docker image prune -a
```

#### 3. Очистка системы Docker

```bash
# Удаление всех остановленных контейнеров
docker container prune

# Удаление всех неиспользуемых томов
docker volume prune

# Удаление всех неиспользуемых сетей
docker network prune

# Полная очистка системы Docker (осторожно!)
docker system prune -a --volumes
```

#### 4. Удаление файлов проекта

```bash
# Удаление созданных во время работы файлов
rm -f *.db                    # SQLite базы данных
rm -f mobile_apps_retention.db
rm -rf logs/                  # Логи (если создавались локально)

# Удаление всей папки проекта (если больше не нужна)
cd ..
rm -rf lw_03/
```

### Проверка полной очистки

После выполнения команд очистки проверьте:

```bash
# Проверка контейнеров
docker ps -a

# Проверка образов
docker images

# Проверка томов
docker volume ls

# Проверка сетей
docker network ls

# Проверка общего использования места
docker system df
```

### Скрипт автоматической очистки

Создайте файл `cleanup.sh` для автоматической очистки:

```bash
#!/bin/bash
echo "🧹 Начинаем полную очистку проекта..."

echo "1. Остановка и удаление контейнеров..."
docker compose down -v --remove-orphans

echo "2. Удаление образов проекта..."
docker rmi apache/airflow:2.5.0-python3.8 postgres:12-alpine mailhog/mailhog:latest 2>/dev/null || true

echo "3. Очистка системы Docker..."
docker system prune -f

echo "4. Удаление локальных файлов..."
rm -f *.db
rm -rf logs/ 2>/dev/null || true

echo "✅ Очистка завершена!"
echo "📊 Текущее использование Docker:"
docker system df
```

Сделайте скрипт исполняемым и запустите:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

### Восстановление после очистки

Если вы хотите снова запустить проект после полной очистки:

```bash
# Клонирование проекта заново (если удалили папку)
git clone <repository_url>
cd lw_03

# Или просто перезапуск (если папка осталась)
docker compose up -d
```

### Мониторинг использования ресурсов

Для контроля использования ресурсов Docker:

```bash
# Просмотр использования места
docker system df

# Детальная информация о томах
docker volume ls -q | xargs docker volume inspect

# Размер конкретного тома
docker volume inspect <volume_name> | grep Mountpoint
du -sh <mountpoint_path>
```

## Структура проекта

```
lw_03/
├── dags/
│   ├── data/                          # Папка с исходными данными
│   │   ├── apps.csv                   # Приложения и категории (20 записей)
│   │   ├── installs.xlsx              # Данные об установках (20 записей)
│   │   └── uninstalls.json            # Данные об удалениях (20 записей)
│   ├── 01_umbrella.py                 # Пример DAG (оригинальный)
│   ├── aggreg.py                      # Пример агрегации (оригинальный)
│   └── mobile_apps_retention_dag.py   # DAG для варианта №30 ⭐
├── docker-compose.yml                 # Конфигурация Docker Compose (обновлена)
├── requirements.txt                   # Зависимости Python (справочно)
├── check_results.py                   # Скрипт для проверки результатов
├── cleanup.sh                         # Скрипт автоматической очистки 🧹
└── README.md                          # Данная инструкция
```

### Описание файлов

| Файл | Описание | Статус |
|------|----------|--------|
| `mobile_apps_retention_dag.py` | Основной DAG для варианта №30 | ⭐ **Главный файл** |
| `docker-compose.yml` | Конфигурация с Airflow, PostgreSQL, MailHog | ✅ Готов к использованию |
| `dags/data/` | Тестовые данные (CSV, Excel, JSON) | 📊 20 записей в каждом файле |
| `check_results.py` | Проверка результатов анализа в SQLite | 🔍 Утилита для отладки |
| `cleanup.sh` | Автоматическая очистка проекта | 🧹 Безопасное удаление |
| `requirements.txt` | Зависимости Python (pandas, openpyxl) | 📦 Справочная информация |

## Ожидаемые результаты

После успешного выполнения DAG вы получите:

1. **Таблицу в SQLite** с результатами анализа коэффициента удержания по категориям
2. **Email-уведомление** об успешном завершении процесса
3. **Логи выполнения** всех этапов ETL-процесса

### Пример результата анализа:

| category     | total_installs | total_uninstalls | retention_rate |
|--------------|----------------|------------------|----------------|
| Games        | 39000          | 7800             | 80.00%         |
| Social       | 12000          | 3600             | 70.00%         |
| Productivity | 7000           | 1400             | 80.00%         |
| Education    | 3500           | 700              | 80.00%         |

## Возможные проблемы и решения

### Проблема: Permission denied при запуске Docker (Linux)
**Ошибка**: `permission denied while trying to connect to the Docker daemon socket`

**Решения**:
```bash
# Способ 1: Запуск с sudo (быстро)
sudo docker compose up -d

# Способ 2: Добавление в группу docker (рекомендуется)
sudo usermod -aG docker $USER
newgrp docker
docker compose up -d

# Способ 3: Временное изменение прав
sudo chmod 666 /var/run/docker.sock
```

### Проблема: Missing optional dependency 'openpyxl'
**Ошибка**: `ImportError: Missing optional dependency 'openpyxl'. Use pip or conda to install openpyxl.`

**Решение**: Зависимости устанавливаются автоматически при запуске контейнеров:
```bash
# Остановите существующие контейнеры
docker compose down

# Запустите все сервисы (зависимости установятся автоматически)
docker compose up -d
```

**Примечание**: При первом запуске контейнеры могут стартовать дольше из-за установки зависимостей.

### Проблема: Предупреждение "version is obsolete"
**Решение**: Атрибут `version` удален из docker-compose.yml в новых версиях

### Проблема: DAG не появляется в интерфейсе
**Решение**: Проверьте синтаксис Python-файла и логи scheduler'а

### Проблема: Ошибки при чтении файлов
**Решение**: Убедитесь, что файлы находятся в папке `dags/data` и имеют правильный формат

### Проблема: Email не отправляется
**Решение**: Проверьте настройки SMTP в конфигурации Airflow и доступность MailHog

### Проблема: Ошибки с SQLite
**Решение**: Убедитесь, что путь к базе данных доступен для записи в контейнере

## Архитектура проекта

### Общая схема системы

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DOCKER COMPOSE ENVIRONMENT                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   PostgreSQL    │    │   Apache        │    │    MailHog      │         │
│  │   Database      │    │   Airflow       │    │  Email Service  │         │
│  │                 │    │                 │    │                 │         │
│  │ Port: 5432      │    │ ┌─────────────┐ │    │ SMTP: 1025      │         │
│  │ User: airflow   │◄───┤ │ Webserver   │ │    │ Web: 8025       │         │
│  │ DB: airflow     │    │ │ Port: 8080  │ │    │                 │         │
│  │                 │    │ └─────────────┘ │    │                 │         │
│  └─────────────────┘    │ ┌─────────────┐ │    └─────────────────┘         │
│                         │ │ Scheduler   │ │                                │
│                         │ │             │ │                                │
│                         │ └─────────────┘ │                                │
│                         └─────────────────┘                                │
│                                   │                                        │
│                         ┌─────────▼─────────┐                              │
│                         │   DAGs Volume     │                              │
│                         │   ./dags:/opt/    │                              │
│                         │   airflow/dags    │                              │
│                         └───────────────────┘                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              HOST SYSTEM                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐         │
│  │   Data Files    │    │   DAG Files     │    │  Result Files   │         │
│  │                 │    │                 │    │                 │         │
│  │ apps.csv        │    │ mobile_apps_    │    │ *.db (SQLite)   │         │
│  │ installs.xlsx   │    │ retention_dag.py│    │ logs/           │         │
│  │ uninstalls.json │    │                 │    │                 │         │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘         │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Web Interfaces                              │   │
│  │                                                                     │   │
│  │  http://localhost:8080  - Apache Airflow UI                        │   │
│  │  http://localhost:8025  - MailHog Web Interface                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Схема ETL-процесса для варианта №30

```
                    EXTRACT PHASE (Параллельно)
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  extract_apps   │  │extract_installs │  │extract_uninstalls│
│                 │  │                 │  │                 │
│ apps.csv        │  │ installs.xlsx   │  │ uninstalls.json │
│ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ │
│ │app_id       │ │  │ │app_id       │ │  │ │app_id       │ │
│ │category     │ │  │ │installs_    │ │  │ │uninstalls_  │ │
│ │             │ │  │ │count        │ │  │ │count        │ │
│ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    TRANSFORM PHASE
                ┌─────────────────┐
                │ transform_data  │
                │                 │
                │ 1. JOIN данные  │
                │ 2. GROUP BY     │
                │    category     │
                │ 3. CALCULATE    │
                │    retention    │
                │    rate         │
                └─────────────────┘
                         │
                    LOAD PHASE
                ┌─────────────────┐
                │load_to_database │
                │                 │
                │ SQLite DB       │
                │ retention_      │
                │ analysis table  │
                └─────────────────┘
                         │
                 REPORTING PHASE
                ┌─────────────────┐
                │generate_report  │
                │                 │
                │ Detailed        │
                │ Analysis Report │
                └─────────────────┘
                         │
               NOTIFICATION PHASE
                ┌─────────────────┐
                │send_email_      │
                │notification     │
                │                 │
                │ MailHog Email   │
                └─────────────────┘
```

### Формулы расчета метрик

```
Retention Rate = (Total Installs - Total Uninstalls) / Total Installs × 100%

Churn Rate = Total Uninstalls / Total Installs × 100%

Retained Users = Total Installs - Total Uninstalls
```

## Особенности реализации DAG для варианта №30

### Архитектура ETL-процесса

1. **Extract (Извлечение)**:
   - `extract_apps` - чтение CSV файла с приложениями и категориями
   - `extract_installs` - чтение Excel файла с данными об установках
   - `extract_uninstalls` - чтение JSON файла с данными об удалениях

2. **Transform (Трансформация)**:
   - Объединение данных по `app_id`
   - Группировка по категориям приложений
   - Расчет коэффициента удержания: `(Installs - Uninstalls) / Installs * 100%`
   - Расчет дополнительных метрик (churn rate, retained users)

3. **Load (Загрузка)**:
   - Сохранение результатов в SQLite базу данных
   - Создание таблицы `retention_analysis` с результатами

4. **Reporting & Notification**:
   - Генерация детального отчета
   - Отправка email-уведомления через MailHog

### Формулы и метрики

- **Retention Rate** = `(Total Installs - Total Uninstalls) / Total Installs * 100%`
- **Churn Rate** = `Total Uninstalls / Total Installs * 100%`
- **Retained Users** = `Total Installs - Total Uninstalls`

### Зависимости задач

```
[extract_apps, extract_installs, extract_uninstalls] 
    ↓
transform_data 
    ↓
load_to_database 
    ↓
generate_report 
    ↓
send_email_notification
```

## Дополнительные материалы

- [Документация Apache Airflow](https://airflow.apache.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [MailHog Documentation](https://github.com/mailhog/MailHog)

## Контакты и поддержка

При возникновении вопросов обращайтесь к преподавателю или используйте официальную документацию Apache Airflow.