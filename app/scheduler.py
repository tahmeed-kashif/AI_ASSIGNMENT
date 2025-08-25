from __future__ import annotations

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from .db import list_active_subscribers


def build_scheduler(timezone: str) -> BackgroundScheduler:
    tz = pytz.timezone(timezone)
    scheduler = BackgroundScheduler(timezone=tz)
    return scheduler


def register_daily_job(scheduler: BackgroundScheduler, app, job_fn) -> None:
    trigger = CronTrigger(hour=9, minute=0)
    scheduler.add_job(job_fn, trigger, id="send_good_morning", replace_existing=True)
    logging.info("Scheduled daily good morning job at 09:00 in timezone: %s", scheduler.timezone)


def make_send_job(app, conn, wa_client, message_generator):
    def _job():
        with app.app_context():
            recipients = list_active_subscribers(conn)
            for row in recipients:
                text = message_generator(row["name"], row["phone"])  # robust if name is None
                try:
                    wa_client.send_text(row["phone"], text)
                except Exception:
                    logging.exception("Error sending message to %s", row["phone"])
    return _job

