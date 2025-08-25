## WhatsApp Good Morning Bot

Sends a daily "Good morning" message at 9:00 in your configured timezone to selected WhatsApp users using the WhatsApp Cloud API.

### Prerequisites
- Python 3.10+
- A Meta app with WhatsApp Cloud API enabled
- `WHATSAPP_TOKEN` and `WHATSAPP_PHONE_NUMBER_ID` from Meta

### Quick start
1) Copy environment template and fill values:
```bash
cp .env.example .env
```

2) Create virtual environment and install dependencies:
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

3) Initialize the database (creates the SQLite file if needed):
```bash
python -m app.cli init-db
```

4) Add subscribers (phone in international format, digits only):
```bash
python -m app.cli add --phone 15551234567 --name "Alice"
python -m app.cli add --phone 15550987654 --name "Bob"
python -m app.cli list
```

5) Run the server (starts webhook and the background scheduler):
```bash
python run.py
```

6) Expose the webhook publicly (example with ngrok) and set the callback URL in Meta:
```bash
ngrok http http://localhost:5000 | cat
```
Use the public HTTPS URL from ngrok as: `https://<host>/webhook/whatsapp`

Verification token to set in Meta equals your `VERIFY_TOKEN` in `.env`.

### Environment variables
Copy `.env.example` to `.env` and set:

- `WHATSAPP_TOKEN`: WhatsApp Cloud API access token
- `WHATSAPP_PHONE_NUMBER_ID`: Sender phone number ID
- `VERIFY_TOKEN`: Arbitrary secret to verify webhook setup
- `DB_PATH`: Path to SQLite file (default: /workspace/data/bot.db)
- `TIMEZONE`: IANA timezone for 9:00 delivery (default: UTC). Example: `Asia/Kolkata`, `America/New_York`
- `APP_BASE_URL` (optional): Public base URL (used in logs)

### Commands
```bash
python -m app.cli init-db
python -m app.cli add --phone 15551234567 --name "Alice"
python -m app.cli deactivate --phone 15551234567
python -m app.cli activate --phone 15551234567
python -m app.cli list
```

### Notes
- Scheduler uses APScheduler with a cron trigger for 9:00 in `TIMEZONE`.
- Webhook supports `subscribe` and `stop` messages to opt-in/out.
- If you deploy, ensure the process stays running (e.g., systemd, Docker, or a PaaS).

