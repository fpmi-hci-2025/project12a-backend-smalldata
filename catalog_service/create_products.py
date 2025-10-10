import asyncio
import random
from datetime import datetime
from uuid import uuid4

from elasticsearch import AsyncElasticsearch, helpers
from faker import Faker


INDEX_NAME = "products"
BATCH_SIZE = 1000
TOTAL_PRODUCTS = 100_000


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

fake = Faker()


def generate_product():
    uid = str(uuid4())
    return {
        "_index": INDEX_NAME,
        "_id": uid,
        "_source": {
            "id": uid,
            "title": fake.sentence(nb_words=3),
            "category_id": random.randint(1, 50),
            "description": fake.text(max_nb_chars=100),
            "characteristics": {
                "color": random.choice(["red", "blue", "green", "black"]),
                "size": random.choice(["S", "M", "L", "XL"]),
            },
            "created_at": datetime.utcnow().isoformat(),
            "amount": random.randint(1, 1000),
            "price": round(random.uniform(5, 500), 2),
        },
    }


async def recreate_index(es: AsyncElasticsearch):
    if await es.indices.exists(index=INDEX_NAME):
        await es.indices.delete(index=INDEX_NAME)
        print(f"Deleted existing index '{INDEX_NAME}'")

    await es.indices.create(index=INDEX_NAME, body=product_index_mapping)
    print(f"Created new index '{INDEX_NAME}'")


async def bulk_insert_products(es: AsyncElasticsearch):
    for i in range(0, TOTAL_PRODUCTS, BATCH_SIZE):
        batch = [generate_product() for _ in range(BATCH_SIZE)]
        await helpers.async_bulk(es, batch)
        print(f"Inserted {i + BATCH_SIZE} products")

async def main():
    es = AsyncElasticsearch("http://localhost:9200", basic_auth=("elastic", "elastic_password_example"))

    await recreate_index(es)
    await bulk_insert_products(es)

    await es.close()


if __name__ == "__main__":
    asyncio.run(main())
