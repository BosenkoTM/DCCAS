#!/bin/bash

# Скрипт для проверки окружения в Ubuntu 20.04
# Проверяет наличие необходимых компонентов для запуска проекта

echo "🔍 ПРОВЕРКА ОКРУЖЕНИЯ ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ №4"
echo "=================================================="

# Проверка операционной системы
echo "📋 Операционная система:"
lsb_release -a 2>/dev/null || echo "Не удалось определить версию ОС"

# Проверка Docker
echo ""
echo "🐳 Проверка Docker:"
if command -v docker &> /dev/null; then
    echo "✅ Docker установлен: $(docker --version)"
    
    # Проверка прав доступа к Docker
    if docker ps &> /dev/null; then
        echo "✅ Права доступа к Docker: OK"
    else
        echo "❌ Нет прав доступа к Docker. Выполните:"
        echo "   sudo usermod -aG docker \$USER"
        echo "   newgrp docker"
    fi
else
    echo "❌ Docker не установлен. Установите Docker:"
    echo "   sudo apt update"
    echo "   sudo apt install docker.io docker-compose"
fi

# Проверка Docker Compose
echo ""
echo "🔧 Проверка Docker Compose:"
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose установлен: $(docker-compose --version)"
elif docker compose version &> /dev/null; then
    echo "✅ Docker Compose (новая версия) установлен: $(docker compose version)"
else
    echo "❌ Docker Compose не установлен"
fi

# Проверка файлов проекта
echo ""
echo "📁 Проверка файлов проекта:"

files_to_check=(
    "docker-compose.yml"
    "requirements.txt"
    "dags/us_presidents_dag.py"
    "dags/datamart_variant_30.sql"
    "README.md"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file - файл не найден"
    fi
done

# Проверка kaggle.json
echo ""
echo "🔑 Проверка Kaggle API:"
if [ -f "kaggle.json" ]; then
    echo "✅ kaggle.json найден"
    
    # Проверка прав доступа
    if [ -r "kaggle.json" ]; then
        echo "✅ Права на чтение: OK"
    else
        echo "❌ Нет прав на чтение. Выполните:"
        echo "   chmod 600 kaggle.json"
    fi
    
    # Проверка содержимого
    if grep -q "username" kaggle.json && grep -q "key" kaggle.json; then
        echo "✅ Структура kaggle.json корректна"
    else
        echo "❌ Неверная структура kaggle.json"
    fi
else
    echo "❌ kaggle.json не найден"
    echo "   Скачайте файл с Kaggle.com и поместите в корень проекта"
fi

# Проверка портов
echo ""
echo "🌐 Проверка портов:"
ports_to_check=(8080 8088 5432 5433 6379)

for port in "${ports_to_check[@]}"; do
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        echo "⚠️  Порт $port занят"
    else
        echo "✅ Порт $port свободен"
    fi
done

# Проверка Docker контейнеров
echo ""
echo "📦 Проверка Docker контейнеров:"
if docker ps -a --format "table {{.Names}}\t{{.Status}}" 2>/dev/null | grep -q "lpw_04"; then
    echo "Контейнеры проекта:"
    docker ps -a --format "table {{.Names}}\t{{.Status}}" | grep "lpw_04"
else
    echo "Контейнеры проекта не найдены"
fi

# Рекомендации
echo ""
echo "💡 РЕКОМЕНДАЦИИ:"
echo "================"

if ! docker ps &> /dev/null; then
    echo "1. Добавьте пользователя в группу docker:"
    echo "   sudo usermod -aG docker \$USER"
    echo "   newgrp docker"
fi

if [ ! -f "kaggle.json" ]; then
    echo "2. Скачайте kaggle.json с Kaggle.com"
fi

echo "3. Запустите проект:"
echo "   sudo docker compose up -d"

echo "4. Проверьте статус контейнеров:"
echo "   sudo docker ps"

echo ""
echo "🎯 ГОТОВО! Проверка окружения завершена."
