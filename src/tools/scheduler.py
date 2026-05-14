import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from src.config import settings
from src.tools.jobs import job_dca

logger = logging.getLogger(__name__)


def create_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone=settings.TZ)

    scheduler.add_job(
        lambda: job_dca(
            btc_amount=settings.BTC_EUR,
            eth_amount=settings.ETH_EUR,
        ),
        CronTrigger(
            day_of_week=settings.TRADE_DAY,
            hour=settings.TRADE_HOUR,
            minute=settings.TRADE_MIN,
            timezone=settings.TZ,
        ),
        id="weekly_dca_buy",
        replace_existing=True,
        misfire_grace_time=300,
        max_instances=1,
        coalesce=True,
    )

    return scheduler


def start_scheduler(scheduler: BackgroundScheduler) -> None:
    if scheduler.running:
        logger.info("Scheduler already running")
        return

    scheduler.start()
    logger.info("Scheduler started")


def shutdown_scheduler(scheduler: BackgroundScheduler) -> None:
    if not scheduler.running:
        logger.info("Scheduler already stopped")
        return

    scheduler.shutdown(wait=False)
    logger.info("Scheduler stopped")