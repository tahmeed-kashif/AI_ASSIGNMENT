from __future__ import annotations

import logging
from flask import Flask, request, jsonify

from .config import load_settings
from .db import get_connection, init_db, add_subscriber, set_active
from .wa_client import WhatsAppClient
from .scheduler import build_scheduler, register_daily_job, make_send_job


def default_message_generator(name: str | None, phone: str) -> str:
    who = name or phone
    return f"Good morning, {who}! Wishing you a productive day."


def create_app() -> Flask:
    settings = load_settings()
    app = Flask(__name__)
    app.config["SETTINGS"] = settings

    conn = get_connection(settings.db_path)
    init_db(conn)
    app.config["DB_CONN"] = conn

    wa_client = WhatsAppClient(settings.whatsapp_token, settings.whatsapp_phone_number_id)
    app.config["WA_CLIENT"] = wa_client

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/webhook/whatsapp")
    def whatsapp_verify():
        # Meta verification flow
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == settings.verify_token:
            return challenge, 200
        return "forbidden", 403

    @app.post("/webhook/whatsapp")
    def whatsapp_inbound():
        data = request.get_json(force=True, silent=True) or {}
        # Minimal parsing: handle text messages with 'subscribe' / 'stop'
        try:
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    for msg in value.get("messages", []) or []:
                        if msg.get("type") == "text":
                            text = (msg.get("text", {}) or {}).get("body", "").strip().lower()
                            from_ = msg.get("from")
                            contacts = (value.get("contacts", []) or [])
                            name = ((contacts[0].get("profile", {}) or {}).get("name") if contacts else None)
                            if not from_:
                                continue
                            if text in {"subscribe", "start", "join"}:
                                add_subscriber(app.config["DB_CONN"], from_, name)
                                app.config["WA_CLIENT"].send_text(from_, "You are subscribed. You'll receive a good morning at 9am.")
                            elif text in {"stop", "unsubscribe", "quit"}:
                                set_active(app.config["DB_CONN"], from_, False)
                                app.config["WA_CLIENT"].send_text(from_, "You have been unsubscribed. Reply 'subscribe' to join again.")
        except Exception:
            logging.exception("Error handling webhook payload")
        return jsonify({"received": True})

    return app


def start_scheduler(app: Flask) -> None:
    settings = app.config["SETTINGS"]
    scheduler = build_scheduler(settings.timezone)
    job = make_send_job(app, app.config["DB_CONN"], app.config["WA_CLIENT"], default_message_generator)
    register_daily_job(scheduler, app, job)
    scheduler.start()

