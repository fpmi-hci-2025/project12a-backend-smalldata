from fastapi import FastAPI

from api.routes import (
    product,
)


def setup_routes(app: FastAPI) -> None:
    app.include_router(product.router)
