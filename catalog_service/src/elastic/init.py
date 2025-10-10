from elasticsearch import AsyncElasticsearch


product_index_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "title": {"type": "text"},
            "category_id": {"type": "integer"},
            "description": {"type": "text"},
            "characteristics": {"type": "object", "enabled": True},
            "created_at": {"type": "date"},
            "amount": {"type": "integer"},
            "price": {"type": "float"},
        }
    }
}


async def init_product_index(es: AsyncElasticsearch, index_name: str):
    exists = await es.indices.exists(index=index_name)
    if not exists:
        await es.indices.create(index=index_name, body=product_index_mapping)
