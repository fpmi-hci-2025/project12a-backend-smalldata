#!/bin/bash

# Стартовый скрипт для e-commerce backend

echo "🚀 Запуск E-commerce Backend System..."

# Проверим, существует ли сеть
if ! docker network ls | grep -q "app-shared-network"; then
    echo "📡 Создаём Docker сеть..."
    docker network create app-shared-network
else
    echo "📡 Docker сеть уже существует"
fi

# Остановим контейнеры если они запущены
echo "🛑 Остановка существующих контейнеров..."
docker-compose -f docker-compose.main.yml down

# Построим образы
echo "🔨 Сборка образов..."
docker-compose -f docker-compose.main.yml build

# Запустим инфраструктуру первой
echo "⚙️ Запуск инфраструктурных сервисов..."
docker-compose -f docker-compose.main.yml up -d rabbit postgres elasticsearch redis

# Подождём пока инфраструктура запустится
echo "⏳ Ожидание готовности инфраструктуры (30 секунд)..."
sleep 30

# Запустим приложения
echo "🔧 Запуск сервисов приложения..."
docker-compose -f docker-compose.main.yml up -d catalog-service-api order-service-api notification-service

# Подождём пока сервисы запустятся
echo "⏳ Ожидание готовности сервисов (20 секунд)..."
sleep 20

# Запустим gateway
echo "🌐 Запуск API Gateway..."
docker-compose -f docker-compose.main.yml up -d api-gateway

echo "✅ Система запущена!"
echo ""
echo "🔍 Проверка состояния:"
docker-compose -f docker-compose.main.yml ps

echo ""
echo "🌐 API Gateway доступен на: http://localhost:8000"
echo "🏥 Health check: curl http://localhost:8000/health"
echo "📦 Products API: curl http://localhost:8000/api/products"
echo ""
echo "📋 Логи: docker-compose -f docker-compose.main.yml logs -f"