import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis

from api.dependencies import setup_dependencies
from api.routes import setup_routes
from config import Settings
from elastic.init import init_product_index



def create_app() -> FastAPI:

    config = Settings()

    es = AsyncElasticsearch(
        f"http://{config.elastic_host}:{config.elastic_port}",
        basic_auth=(config.elastic_user, config.elastic_password)
    )

    redis = Redis(
        host=config.redis_host,
        password=config.redis_password,
        username=config.redis_user,
        port=config.redis_port,
    )

    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_product_index(es, config.products_elastic_index_name)
        yield
        await es.close()
        await redis.aclose()

    app = FastAPI(
        title="Catalog service API",
        version="1.0",
        docs_url="/api/docs",
        lifespan=lifespan,
    )

    setup_dependencies(
        app=app,
        elasticsearch_gateway=es,
        redis_gateway=redis,
        config=config,
    )
    setup_routes(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return app


app = create_app()
