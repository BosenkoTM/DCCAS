# Анализ данных авиакомпаний - Задание 30

Практическая работа по консолидации и аналитической обработке данных авиакомпаний с использованием Docker Compose, Jupyter Notebook и PostgreSQL на Ubuntu 20+.

## 🎯 Цель работы

Рассчитать общую выручку для каждой авиакомпании на основе консолидации данных из трех источников:
- **airlines.csv** - данные об авиакомпаниях (airline_id, name)
- **flights.xlsx** - данные о рейсах (flight_id, airline_id, passengers_count)
- **tickets.json** - данные о билетах (flight_id, avg_ticket_price)

## 🏗️ Архитектура

- **Docker Compose v2** для оркестрации контейнеров
- **Jupyter Lab** для анализа данных и визуализации
- **PostgreSQL 15** для хранения и обработки данных
- **Python** с библиотеками: pandas, numpy, matplotlib, seaborn, plotly

## 📋 Требования

- Ubuntu 20+ 
- Docker и Docker Compose v2 (см. [dockerhelp.md](dockerhelp.md) для установки)
- Python 3.8+
- Свободные порты: 8888 (Jupyter), 5432 (PostgreSQL)

## 🚀 Запуск на Ubuntu 20+

### 1. Подготовка системы

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip (если не установлены)
sudo apt install python3 python3-pip -y

# Установка библиотек для генерации данных
pip3 install pandas numpy openpyxl
```

**Установка Docker:** Если Docker не установлен, следуйте инструкциям в [dockerhelp.md](dockerhelp.md)

### 2. Клонирование проекта

```bash
git clone <repository-url>
cd pw_03
```

### 3. Генерация тестовых данных

```bash
python3 data_generator.py
```

**Если возникает ошибка с папкой 'data':**
```bash
# Создать папку вручную и повторить
mkdir -p data
chmod 755 data
python3 data_generator.py
```

### 4. Запуск Docker Compose

```bash
sudo docker compose up -d
```

Или используйте готовый скрипт:
```bash
chmod +x start.sh
./start.sh
```

### 5. Доступ к сервисам

- **Jupyter Lab**: http://localhost:8888 (без пароля)
- **PostgreSQL**: localhost:5432
  - База данных: `airline_analytics`
  - Пользователь: `analyst`
  - Пароль: `analyst123`

### 6. Выполнение анализа

1. Откройте браузер и перейдите на http://localhost:8888
2. Перейдите в папку `work/notebooks`
3. Откройте `airline_analysis.ipynb`
4. Выполните все ячейки последовательно (Shift+Enter)

## 📊 Структура проекта

```
programmETL/
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Образ Jupyter с библиотеками
├── data_generator.py          # Генератор тестовых данных
├── README.md                  # Документация
├── sql/
│   └── 01_init_schema.sql     # SQL схема для PostgreSQL
├── notebooks/
│   └── airline_analysis.ipynb # Основной анализ
└── data/
    ├── airlines.csv           # Данные авиакомпаний
    ├── flights.xlsx           # Данные рейсов
    └── tickets.json           # Данные билетов
```

## 📈 Этапы анализа

1. **Загрузка данных** из CSV, Excel и JSON файлов
2. **Предварительная обработка** и аудит данных
3. **Очистка данных** и приведение к единому формату
4. **Консолидация данных** через JOIN операции
5. **Feature Engineering** - создание производных признаков
6. **Расчет выручки** для каждой авиакомпании
7. **Визуализация результатов** с помощью matplotlib, seaborn, plotly
8. **Формирование выводов** и рекомендаций

## 📊 Визуализации

- Столбчатая диаграмма общей выручки авиакомпаний
- Круговая диаграмма долей рынка
- Сравнительный анализ количества рейсов и средних цен
- Интерактивные графики с Plotly
- Тепловая карта выручки по месяцам

## 🗄️ База данных PostgreSQL

Автоматически создается схема с таблицами:
- `airlines` - авиакомпании
- `flights` - рейсы
- `tickets` - билеты
- `airline_revenue` - представление для расчета выручки

## 📁 Результаты

Все результаты сохраняются в папке `data/`:
- `consolidated_airline_data.csv` - консолидированные данные
- `airline_revenue_summary.csv` - итоговая выручка по авиакомпаниям
- `monthly_revenue_analysis.csv` - анализ по месяцам

## 🛠️ Управление контейнерами

```bash
# Запуск сервисов
sudo docker compose up -d

# Просмотр статуса
sudo docker compose ps

# Просмотр логов
sudo docker compose logs -f

# Остановка сервисов
sudo docker compose down

# Полная очистка (включая данные)
sudo docker compose down -v

# Пересборка образов
sudo docker compose build --no-cache
sudo docker compose up -d
```

## 🔧 Подключение к PostgreSQL

```python
import psycopg2
import pandas as pd

# Параметры подключения
conn_params = {
    'host': 'localhost',
    'database': 'airline_analytics',
    'user': 'analyst',
    'password': 'analyst123',
    'port': 5432
}

# Подключение и выполнение запросов
conn = psycopg2.connect(**conn_params)
df = pd.read_sql("SELECT * FROM airline_revenue", conn)
```

## 📋 Основные выводы

После выполнения анализа вы получите:
- Рейтинг авиакомпаний по выручке
- Анализ эффективности по количеству рейсов
- Сезонные тренды в авиаперевозках
- Рекомендации по оптимизации бизнес-процессов

## 🆘 Устранение неполадок

### Порт уже занят
```bash
# Найти процесс на порту 8888
sudo netstat -tulpn | grep :8888

# Остановить все Docker контейнеры
sudo docker stop $(sudo docker ps -aq)
```

### Проблемы с Docker
```bash
# Пересборка образов
sudo docker compose build --no-cache
sudo docker compose up -d

# Очистка Docker системы
sudo docker system prune -a
```

### Ошибки подключения к PostgreSQL
```bash
# Проверка статуса контейнера
sudo docker compose ps

# Просмотр логов PostgreSQL
sudo docker compose logs postgres

# Подключение к контейнеру PostgreSQL
sudo docker compose exec postgres psql -U analyst -d airline_analytics
```

## 👥 Авторы

Практическая работа выполнена в рамках курса "Программные средства консолидации данных" МГПУ.

## 📄 Лицензия

Конечно, вот короткий раздел для `README.md` на GitHub, описывающий материалы и критерии оценки.

---

### ##  сда и оценка работы

Варианты заданий для выполнения практической работы доступны по ссылке:
**[Скачать варианты заданий](http://95.131.149.21/moodle/pluginfile.php/3452/mod_assign/introattachment/0/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%203.pdf?forcedownload=1)**

### 📁 Материалы для оценки

Для проверки работы необходимо предоставить **ссылку на публичный репозиторий GitHub**, содержащий:

1.  **`README.md`** — файл с описанием вашего варианта задания, инструкциями по запуску проекта и краткими выводами по результатам анализа.
2.  **Jupyter Notebook (`.ipynb`)** — полностью выполненный ноутбук с кодом, комментариями, выводом ячеек и всеми визуализациями.
3.  **Исходный код проекта** — все файлы, необходимые для запуска (`docker-compose.yml`, `Dockerfile`, `.py` скрипты, `.sql` файлы и т.д.).
4.  **Папка с результатами** — итоговые файлы (`.csv`, `.png`/`.jpeg` для графиков), полученные в ходе анализа.

### 📊 Критерии оценки

Итоговая оценка формируется на основе следующих критериев:

*   **Корректность выполнения (20%)**
    *   Решение соответствует заданию, указанному в варианте.
    *   Конечные расчеты и выводы верны.

*   **Качество кода и структура проекта (30%)**
    *   Логичная и понятная структура проекта (разделение на папки `notebooks`, `data`, `sql`).
    *   Читаемый и комментированный код в Jupyter Notebook.
    *   Корректное использование Docker для обеспечения воспроизводимости.

*   **Глубина анализа и визуализация (30%)**
    *   Проведены необходимые этапы очистки и предобработки данных.
    *   Логика консолидации данных реализована корректно.
    *   Визуализации наглядны, информативны и соответствуют данным.
    *   Сформулированы обоснованные выводы на основе полученных результатов.

*   **Качество документации (20%)**
    *   `README.md` содержит четкие и полные инструкции по запуску.
    *   Ясно описана цель работы и итоговые выводы.
