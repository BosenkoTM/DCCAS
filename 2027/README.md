# Практические и лабораторные работы — 2027

Дисциплина: **«Программные средства сбора, консолидации и аналитики данных»**. Магистратура **38.04.05 «Бизнес-информатика»**.

В этом каталоге размещены **только выполняемые работы и связанные с ними вспомогательные файлы**. Лекции, литература, полные задания, сроки и сдача работ находятся **на EnvLab**.

## Практические работы

| Работа | Каталог и файлы | Задание |
|---|---|---|
| ПР № 1. Открытые API, HTML (BeautifulSoup, XPath), регулярные выражения | [`pw_01/`](pw_01/) — Colab-ноутбук | [EnvLab № 415](https://envlab.ru/mod/assign/view.php?id=415) |

## Лабораторные работы

| Работа | Каталог и файлы | Задание | Максимум по актуализированным материалам |
|---|---|---|---|
| ЛР № 1. Динамический веб-парсинг | [`lw_01/`](lw_01/) — Colab-ноутбук, `market_stand.html` | [EnvLab № 418](https://envlab.ru/mod/assign/view.php?id=418) | 10 |
| ЛР № 2. Консолидация CSV + Excel + JSON → SQLite | [`lw_02/`](lw_02/) — Colab-ноутбук | [EnvLab № 424](https://envlab.ru/mod/assign/view.php?id=424) | 10, дополнительно до +2 |
| ЛР № 3. ETL-конвейер и аналитический дашборд | [`lw_03/`](lw_03/) — пояснения, шаблон отчёта, заготовки кода | [EnvLab № 427](https://envlab.ru/mod/assign/view.php?id=427) | **20** |
| ЛР № 4. GenAI/RAG для поддержки управленческого решения | [`lw_04/`](lw_04/) — Colab-ноутбук | [EnvLab № 423](https://envlab.ru/mod/assign/view.php?id=423) | 10, дополнительно до +2 |

ПР № 1 — максимум **10 баллов**. Баллы указываются для ориентира и не меняют опубликованные критерии EnvLab.

## Лекции и литература — только на образовательном портале

**Тема 1 — сбор:** [HTML и XML](https://envlab.ru/mod/lesson/view.php?id=409), [RegEx в Python](https://envlab.ru/mod/lesson/view.php?id=410), [BeautifulSoup I](https://envlab.ru/mod/lesson/view.php?id=411), [BeautifulSoup II](https://envlab.ru/mod/lesson/view.php?id=412), [BeautifulSoup III](https://envlab.ru/mod/lesson/view.php?id=413); [документация Playwright](https://envlab.ru/mod/url/view.php?id=420), [книга Р. Митчелл](https://envlab.ru/mod/resource/view.php?id=421).

**Тема 2 — консолидация:** [лекция](https://envlab.ru/mod/lesson/view.php?id=1623); [Cleanlab](https://envlab.ru/mod/url/view.php?id=425), [Харенслак, де Руйтер — Apache Airflow и конвейеры обработки данных](https://envlab.ru/mod/resource/view.php?id=426).

**Тема 3 — аналитика:** [лекция](https://envlab.ru/mod/lesson/view.php?id=1622); [Apache Superset](https://envlab.ru/mod/url/view.php?id=428).

**Тема 4 — GenAI:** [лабораторная и учебные указания на EnvLab](https://envlab.ru/mod/assign/view.php?id=423).

Некоторые ресурсы EnvLab требуют авторизации. Литература не копируется в публичный репозиторий по соображениям авторских прав.

## Сквозной кейс

`API / HTML / CSV / Excel / JSON → pandas + QA → SQLite / PostgreSQL → Airflow + SQL VIEW → Superset → RAG + оценка качества/рисков/экономики → бизнес-решение`.

**Важно:** не объединять работы № 3 и № 4: № 3 посвящена бизнес-аналитике и визуализации, № 4 — оценке применимости RAG/GenAI для бизнеса.

**Безопасность:** исключите `kaggle.json`, `.env`, токены и другие секреты из Git. Архивный `lpw_04/` из корня репозитория не следует копировать целиком: он использует Airflow 2.5 и PostgreSQL 12, а его конфигурацию требуется актуализировать перед запуском.
