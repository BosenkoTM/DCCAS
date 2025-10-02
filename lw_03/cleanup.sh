#!/bin/bash

# Скрипт полной очистки проекта лабораторной работы №3
# Apache Airflow ETL Pipeline

echo "🧹 Начинаем полную очистку проекта Airflow ETL..."
echo "⚠️  ВНИМАНИЕ: Все данные проекта будут удалены!"
echo ""

# Запрос подтверждения
read -p "Вы уверены, что хотите продолжить? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Очистка отменена пользователем"
    exit 1
fi

echo "🔄 Начинаем очистку..."
echo ""

# 1. Остановка и удаление контейнеров
echo "1️⃣  Остановка и удаление контейнеров..."
if docker compose down -v --remove-orphans; then
    echo "✅ Контейнеры остановлены и удалены"
else
    echo "⚠️  Ошибка при остановке контейнеров (возможно, они уже остановлены)"
fi
echo ""

# 2. Удаление образов проекта
echo "2️⃣  Удаление образов проекта..."
images_to_remove=(
    "apache/airflow:2.5.0-python3.8"
    "postgres:12-alpine"
    "mailhog/mailhog:latest"
)

for image in "${images_to_remove[@]}"; do
    if docker rmi "$image" 2>/dev/null; then
        echo "✅ Удален образ: $image"
    else
        echo "⚠️  Образ не найден или уже удален: $image"
    fi
done
echo ""

# 3. Очистка системы Docker
echo "3️⃣  Очистка системы Docker..."
if docker system prune -f; then
    echo "✅ Система Docker очищена"
else
    echo "⚠️  Ошибка при очистке системы Docker"
fi
echo ""

# 4. Удаление локальных файлов
echo "4️⃣  Удаление локальных файлов проекта..."

# Удаление SQLite баз данных
if rm -f *.db 2>/dev/null; then
    echo "✅ Удалены файлы баз данных (*.db)"
else
    echo "ℹ️  Файлы баз данных не найдены"
fi

# Удаление логов
if rm -rf logs/ 2>/dev/null; then
    echo "✅ Удалена папка логов"
else
    echo "ℹ️  Папка логов не найдена"
fi

# Удаление временных файлов Python
if find . -name "*.pyc" -delete 2>/dev/null; then
    echo "✅ Удалены временные файлы Python"
fi

if find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null; then
    echo "✅ Удалены кэш-папки Python"
fi

echo ""

# 5. Проверка результатов очистки
echo "5️⃣  Проверка результатов очистки..."
echo ""

echo "📊 Статистика Docker после очистки:"
docker system df
echo ""

echo "📋 Оставшиеся контейнеры:"
container_count=$(docker ps -a -q | wc -l)
if [ "$container_count" -eq 0 ]; then
    echo "✅ Контейнеры не найдены"
else
    docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"
fi
echo ""

echo "📋 Оставшиеся образы проекта:"
project_images=$(docker images | grep -E "(airflow|postgres|mailhog)" | wc -l)
if [ "$project_images" -eq 0 ]; then
    echo "✅ Образы проекта не найдены"
else
    docker images | grep -E "(airflow|postgres|mailhog)"
fi
echo ""

echo "📋 Оставшиеся тома:"
volume_count=$(docker volume ls -q | wc -l)
if [ "$volume_count" -eq 0 ]; then
    echo "✅ Тома не найдены"
else
    docker volume ls
fi
echo ""

# 6. Финальное сообщение
echo "🎉 Очистка проекта завершена!"
echo ""
echo "📁 Структура проекта после очистки:"
ls -la
echo ""

echo "🔄 Для повторного запуска проекта выполните:"
echo "   docker compose up -d"
echo ""

echo "📚 Для полного удаления папки проекта выполните:"
echo "   cd .. && rm -rf lw_03/"
echo ""

echo "✨ Готово! Проект полностью очищен."
