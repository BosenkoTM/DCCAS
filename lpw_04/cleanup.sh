#!/bin/bash

# Скрипт для очистки Docker-окружения после работы
# Л+П №4 - Анализ президентов США

echo "🧹 ОЧИСТКА DOCKER-ОКРУЖЕНИЯ ЛАБОРАТОРНОЙ РАБОТЫ №4"
echo "=================================================="

# Функция для подтверждения действия
confirm() {
    read -p "Вы уверены, что хотите продолжить? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Операция отменена"
        exit 1
    fi
}

# Проверка прав доступа
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  Этот скрипт требует прав администратора"
    echo "Запустите с sudo: sudo ./cleanup.sh"
    exit 1
fi

echo "📋 Что будет очищено:"
echo "  - Остановка всех контейнеров проекта"
echo "  - Удаление контейнеров проекта"
echo "  - Удаление образов проекта"
echo "  - Удаление томов проекта"
echo "  - Удаление сетей проекта"
echo ""

# Показать текущие контейнеры проекта
echo "🔍 Текущие контейнеры проекта:"
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | grep -E "(lpw_04|postgres|superset|redis)" || echo "Контейнеры проекта не найдены"
echo ""

# Показать текущие образы
echo "🔍 Текущие образы проекта:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(airflow|postgres|superset|redis)" || echo "Образы проекта не найдены"
echo ""

# Показать текущие тома
echo "🔍 Текущие тома проекта:"
docker volume ls --format "table {{.Name}}\t{{.Driver}}" | grep -E "(lpw_04|postgres|superset)" || echo "Тома проекта не найдены"
echo ""

# Подтверждение
confirm

echo "🛑 Остановка контейнеров..."
docker compose down

echo "🗑️  Удаление контейнеров проекта..."
docker container prune -f

echo "🗑️  Удаление образов проекта..."
# Удаляем только образы, связанные с проектом
docker images --format "{{.Repository}}:{{.Tag}}" | grep -E "(airflow|postgres|superset|redis)" | xargs -r docker rmi -f

echo "🗑️  Удаление томов проекта..."
# Удаляем только тома проекта
docker volume ls --format "{{.Name}}" | grep -E "(lpw_04|postgres|superset)" | xargs -r docker volume rm -f

echo "🗑️  Удаление сетей проекта..."
docker network prune -f

echo "🧹 Очистка неиспользуемых ресурсов..."
docker system prune -f

echo ""
echo "✅ Очистка завершена!"
echo ""

# Проверка результатов
echo "📊 Результаты очистки:"
echo "====================="

echo "Контейнеры:"
docker ps -a --format "table {{.Names}}\t{{.Status}}" | grep -E "(lpw_04|postgres|superset|redis)" || echo "Контейнеры проекта удалены"

echo ""
echo "Образы:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E "(airflow|postgres|superset|redis)" || echo "Образы проекта удалены"

echo ""
echo "Тома:"
docker volume ls --format "table {{.Name}}\t{{.Driver}}" | grep -E "(lpw_04|postgres|superset)" || echo "Тома проекта удалены"

echo ""
echo "💡 Для повторного запуска проекта выполните:"
echo "   sudo docker compose up -d"
echo ""
echo "🎯 Очистка Docker-окружения завершена успешно!"
