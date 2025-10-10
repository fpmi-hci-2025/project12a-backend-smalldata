from fastapi import FastAPI
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from config import Settings
from api.dependencies.stubs import get_config, get_elasticsearch_gateway, get_redis_gateway


def setup_dependencies(
    app: FastAPI,
    config: Settings,
    redis_gateway: Redis,
    elasticsearch_gateway: AsyncElasticsearch,
) -> None:
    app.dependency_overrides[get_config] = lambda: config
    app.dependency_overrides[get_redis_gateway] = lambda: redis_gateway
    app.dependency_overrides[get_elasticsearch_gateway] = lambda: elasticsearch_gateway
