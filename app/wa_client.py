from __future__ import annotations

import logging
import requests


class WhatsAppClient:
    def __init__(self, token: str, phone_number_id: str) -> None:
        self._token = token
        self._phone_number_id = phone_number_id
        self._base_url = f"https://graph.facebook.com/v20.0/{self._phone_number_id}/messages"

    def send_text(self, to_phone: str, text: str) -> dict:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": text},
        }
        response = requests.post(self._base_url, headers=headers, json=payload, timeout=20)
        try:
            response.raise_for_status()
        except Exception as exc:  # keep concise logging
            logging.exception("Failed sending WhatsApp message to %s: %s", to_phone, response.text)
            raise exc
        return response.json()

