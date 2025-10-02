# 🐳 Установка Docker и Docker Compose v2 на Ubuntu 20+

## Системные требования

- Ubuntu 20.04 LTS или новее
- Архитектура: x86_64/amd64, armhf, arm64, s390x
- Минимум 4 ГБ RAM
- Минимум 20 ГБ свободного места на диске

## 1. Подготовка системы

### Обновление пакетов
```bash
sudo apt update && sudo apt upgrade -y
```

### Установка необходимых пакетов
```bash
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common
```

## 2. Установка Docker Engine

### Удаление старых версий (если есть)
```bash
sudo apt remove -y docker docker-engine docker.io containerd runc
```

### Добавление официального GPG ключа Docker
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

### Добавление репозитория Docker
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Установка Docker Engine
```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 3. Настройка Docker

### Добавление пользователя в группу docker
```bash
sudo usermod -aG docker $USER
```

### Применение изменений группы
```bash
newgrp docker
```

### Автозапуск Docker при загрузке системы
```bash
sudo systemctl enable docker
sudo systemctl start docker
```

## 4. Проверка установки

### Проверка версии Docker
```bash
docker --version
```
Ожидаемый вывод: `Docker version 24.x.x, build ...`

### Проверка версии Docker Compose v2
```bash
docker compose version
```
Ожидаемый вывод: `Docker Compose version v2.x.x`

### Тестовый запуск
```bash
docker run hello-world
```

## 5. Альтернативный способ установки (через скрипт)

### Автоматическая установка
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

## 6. Настройка производительности (опционально)

### Увеличение лимитов файловых дескрипторов
```bash
echo '* soft nofile 65536' | sudo tee -a /etc/security/limits.conf
echo '* hard nofile 65536' | sudo tee -a /etc/security/limits.conf
```

### Настройка логирования Docker
```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json > /dev/null <<EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF
```

### Перезапуск Docker с новыми настройками
```bash
sudo systemctl restart docker
```

## 7. Проверка работоспособности

### Информация о системе Docker
```bash
docker info
```

### Список запущенных контейнеров
```bash
docker ps
```

### Проверка Docker Compose v2
```bash
docker compose --help
```

## 8. Устранение проблем

### Если Docker не запускается
```bash
# Проверка статуса службы
sudo systemctl status docker

# Просмотр логов
sudo journalctl -u docker.service

# Перезапуск службы
sudo systemctl restart docker
```

### Если нет прав на выполнение команд Docker
```bash
# Проверка принадлежности к группе docker
groups $USER

# Если группы docker нет, добавить снова
sudo usermod -aG docker $USER
newgrp docker

# Или перезайти в систему
logout
```

### Очистка Docker системы
```bash
# Удаление неиспользуемых контейнеров, сетей, образов
docker system prune -a

# Удаление всех томов
docker volume prune
```

## 9. Полезные команды

### Управление Docker службой
```bash
# Запуск
sudo systemctl start docker

# Остановка
sudo systemctl stop docker

# Перезапуск
sudo systemctl restart docker

# Статус
sudo systemctl status docker
```

### Информация о ресурсах
```bash
# Использование дискового пространства
docker system df

# Мониторинг ресурсов контейнеров
docker stats
```

## 10. Проверка готовности для проекта

После установки выполните эти команды для проверки:

```bash
# Проверка Docker
docker --version

# Проверка Docker Compose v2
docker compose version

# Тест запуска контейнера
docker run --rm hello-world

# Проверка портов (должны быть свободны)
sudo netstat -tulpn | grep -E ':8888|:5432'
```

Если все команды выполнились успешно, Docker готов для работы с проектом анализа авиакомпаний!

## 🚀 Следующий шаг

После успешной установки Docker переходите к основному README.md для запуска проекта анализа данных авиакомпаний.
