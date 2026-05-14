import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.v1.trades import router as trade_router
from src.config import settings
from src.tools.scheduler import create_scheduler, shutdown_scheduler, start_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

api_router = APIRouter()
api_router.include_router(trade_router)

scheduler = create_scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kraken DCA API")
    logger.info(
    "Scheduler config | enabled=%s | day=%s | time=%s:%s | btc=%s | eth=%s | tz=%s",
    settings.ENABLE_SCHEDULER,
    settings.TRADE_DAY,
    settings.TRADE_HOUR,
    settings.TRADE_MIN,
    settings.BTC_EUR,
    settings.ETH_EUR,
    settings.TZ,
)
    if settings.ENABLE_SCHEDULER:
        start_scheduler(scheduler)
    else:
        logger.info("Scheduler disabled")

    yield

    shutdown_scheduler(scheduler)
    logger.info("Shutting down Kraken DCA API")


app = FastAPI(
    title="Kraken DCA Scheduler API",
    description="Local API for scheduled and manual Kraken Pro trades.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/v1")


@app.get("/", include_in_schema=False)
def status_check():
    return {
        "status": "running",
        "service": "kraken-dca",
        "docs": "/docs",
        "scheduler_enabled": settings.ENABLE_SCHEDULER,
    }


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "error": str(exc),
        },
    )