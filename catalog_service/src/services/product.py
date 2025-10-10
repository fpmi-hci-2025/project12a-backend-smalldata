from datetime import datetime
from uuid import UUID
from typing import Optional, List

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from redis.asyncio import Redis

from dto.product import ProductDTO
from exceptions.product import ProductDoesNotExistError
from serializers.product import serialize_product, deserialize_product


class ProductService:

    def __init__(
        self,
        es: AsyncElasticsearch,
        index_name: str,
        redis: Redis,
        redis_product_by_id_ttl: int,
    ):
        self.es = es
        self.index = index_name
        self.redis = redis
        self.redis_product_by_id_ttl = redis_product_by_id_ttl

    async def get_products(
        self,
        title: Optional[str] = None,
        category_id: Optional[int] = None,
        price: Optional[float] = None,
        description: Optional[str] = None,
    ) -> List[ProductDTO]:
        must_clauses = []

        if title is not None:
            must_clauses.append({"match": {"title": title}})
        if category_id is not None:
            must_clauses.append({"term": {"category_id": category_id}})
        if price is not None:
            must_clauses.append({"term": {"price": price}})
        if description is not None:
            must_clauses.append({"match": {"description": description}})

        query = {
            "size": 100,
            "query": {
                "bool": {
                    "must": must_clauses
                }
            }
        }

        response = await self.es.search(index=self.index, body=query)
        return [
            self._map_hit_to_dto(hit["_source"]) for hit in response["hits"]["hits"]
        ]

    async def create_product(
        self,
        id: UUID,
        title: str,
        category_id: int,
        description: str,
        characteristics: dict,
        created_at: datetime,
        amount: int,
        price: float,
    ) -> ProductDTO:
        product = {
            "id": str(id),
            "title": title,
            "category_id": category_id,
            "description": description,
            "characteristics": characteristics,
            "created_at": created_at.isoformat(),
            "amount": amount,
            "price": price,
        }

        await self.es.index(index=self.index, id=str(id), document=product)

        return ProductDTO(
            id=id,
            title=title,
            category_id=category_id,
            description=description,
            characteristics=characteristics,
            created_at=created_at,
            amount=amount,
            price=price
        )

    async def delete_product(self, product_id: UUID) -> None:
        try:
            await self.es.delete(index=self.index, id=str(product_id))
        except NotFoundError:
            raise ProductDoesNotExistError
        else:
            await self.redis.delete(f"product:{product_id.hex}")

    async def update_product(
        self,
        product_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        price: Optional[float] = None,
    ) -> None:
        updates = {}

        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        if amount is not None:
            updates["amount"] = amount
        if price is not None:
            updates["price"] = price

        try:
            await self.es.update(
                index=self.index,
                id=str(product_id),
                body={"doc": updates}
            )
        except NotFoundError:
            raise ProductDoesNotExistError

    async def get_product_by_id(self, product_id: UUID, from_cache: bool = True) -> Optional[ProductDTO]:
        cache_key = f"product:{product_id.hex}"

        if from_cache:
            cached = await self.redis.get(cache_key)
            if cached:
                product_dict = deserialize_product(cached)
                return self._map_hit_to_dto(product_dict)

        try:
            response = await self.es.get(index=self.index, id=str(product_id))
            product = response["_source"]
            dto = self._map_hit_to_dto(product)

            await self.redis.set(
                cache_key,
                serialize_product(dto.__dict__),
                ex=self.redis_product_by_id_ttl,
            )
            return dto
        except NotFoundError:
            raise ProductDoesNotExistError

    async def is_product_available(self, product_id: UUID) -> bool:
        try:
            product = await self.get_product_by_id(
                product_id=product_id,
                from_cache=False,
            )
        except ProductDoesNotExistError:
            return False

        return True if product.amount > 0 else False

    def _map_hit_to_dto(self, hit: dict) -> ProductDTO:
        return ProductDTO(
            id=hit["id"],
            title=hit["title"],
            category_id=hit["category_id"],
            description=hit["description"],
            characteristics=hit["characteristics"],
            created_at=hit["created_at"],
            amount=hit["amount"],
            price=hit["price"],
        )
