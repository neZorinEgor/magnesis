from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.geomagnesis.config import settings
from src.geomagnesis.presentations.http_api.lifespan import asgi_lifespan
from src.geomagnesis.presentations.http_api.middleware.prometheus_metrics import (
    PrometheusMetricsMiddleware,
)
from src.geomagnesis.presentations.http_api.routers.healthcheck import (
    router as healthcheck_router,
)
from src.geomagnesis.presentations.http_api.routers.metrics import router as metrics_router
from src.geomagnesis.presentations.http_api.routers.swagger import router as swagger_router
from src.geomagnesis.presentations.http_api.routers.frontend import router as frontend_router


def make_asgi() -> FastAPI:
    app = FastAPI(
        **settings.swagger_ui_kwargs,
        docs_url=None,   # include in swagger router
        redoc_url=None,  # include in swagger router
        lifespan=asgi_lifespan,
    )
    app.mount("/static", StaticFiles(directory=settings.STATIC_PATH), name="static")
    # swagger/redoc only in 'dev' mode
    if settings.app.ENV == "dev":
        app.include_router(swagger_router)
    app.include_router(metrics_router)
    app.include_router(healthcheck_router)
    app.include_router(frontend_router)
    app.add_middleware(PrometheusMetricsMiddleware, app_name=settings.swagger_ui.TITLE.lower())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.ALLOW_ORIGINS,
        allow_methods=settings.cors.ALLOW_METHODS,
        allow_headers=settings.cors.ALLOW_HEADERS,
        allow_credentials=settings.cors.ALLOW_CREDENTIALS,
    )
    return app

