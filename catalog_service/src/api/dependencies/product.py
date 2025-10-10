from fastapi import Depends
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch

from config import Settings
from api.dependencies.stubs import get_redis_gateway, get_config, get_elasticsearch_gateway
from services.product import ProductService


def get_product_service(
    es: AsyncElasticsearch = Depends(get_elasticsearch_gateway),
    redis: Redis = Depends(get_redis_gateway),
    config: Settings = Depends(get_config),
):
    return ProductService(
        es=es,
        redis=redis,
        index_name=config.products_elastic_index_name,
        redis_product_by_id_ttl=config.redis_product_by_id_ttl,
    )
