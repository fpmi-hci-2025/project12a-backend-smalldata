from dotenv import find_dotenv

from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_file_encoding="utf-8"
    )

    api_token: str = "token"

    elastic_host: str
    elastic_port: int
    elastic_user: str
    elastic_password: str

    products_elastic_index_name: str = "products"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_user: str = "default"
    redis_password: str = "password"

    @property
    def redis_url(self) -> RedisDsn:
        return f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/0"

    redis_product_by_id_ttl: int = 10
