from logging import getLogger

import httpx

from config import config


logger = getLogger(__name__)


class CatalogClient:

    @staticmethod
    async def check_product_exists(product_id: int) -> bool:
        url = f"{config.catalog_service_url}/api/products/{product_id}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                logger.info(response.json())
                return response.status_code == 200
            except httpx.RequestError:
                return False
