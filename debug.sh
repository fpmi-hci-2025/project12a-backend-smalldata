#!/bin/bash

# Скрипт для отладки проблем

echo "🔍 Диагностика E-commerce Backend System"
echo "========================================"

echo ""
echo "📡 Проверка Docker сети:"
docker network ls | grep app-shared-network

echo ""
echo "📋 Статус контейнеров:"
docker-compose -f docker-compose.main.yml ps

echo ""
echo "🏥 Проверка здоровья:"
echo "API Gateway:"
curl -s http://localhost:8000/health 2>/dev/null && echo " ✅ Gateway OK" || echo " ❌ Gateway недоступен"

echo ""
echo "🔍 Последние логи сервисов:"
echo "--- API Gateway ---"
docker logs api-gateway --tail 5 2>/dev/null || echo "Контейнер не найден"

echo ""
echo "--- Catalog Service ---"
docker logs catalog-service-api --tail 5 2>/dev/null || echo "Контейнер не найден"

echo ""
echo "--- Order Service ---"
docker logs order-service-api --tail 5 2>/dev/null || echo "Контейнер не найден"

echo ""
echo "--- Notification Service ---"
docker logs notification-service --tail 5 2>/dev/null || echo "Контейнер не найден"

echo ""
echo "🔧 Рекомендации по исправлению:"
echo "1. Если сервисы не запускаются: ./start.sh"
echo "2. Если Gateway не работает: docker-compose -f docker-compose.main.yml restart api-gateway"
echo "3. Полная перезагрузка: docker-compose -f docker-compose.main.yml down && ./start.sh"
echo "4. Логи реального времени: docker-compose -f docker-compose.main.yml logs -f"