# Kraken DCA Scheduler

Dockerized FastAPI application for automated and manual Kraken Pro DCA trading.

---

## Features

- Weekly automated DCA scheduler using APScheduler
- Manual BTC / ETH / DCA trade endpoints
- FastAPI Swagger UI
- Dockerized deployment
- Environment-based configuration
- Optional dry-run mode
- Structured logging
- Kraken REST API integration

---

# Stack

- Python 3.12
- FastAPI
- APScheduler
- Docker
- Uvicorn

---

# Project Structure

```text
.
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── src/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── models/
│   │   └── v1/
│   │       └── trades.py
│   └── tools/
│       ├── jobs.py
│       ├── kraken_api.py
│       └── scheduler.py
└── data/
```

---

# Requirements

Install:

- Docker
- Docker Compose
- Git

---

# Clone Repository

```bash
git clone https://github.com/blauwe-oehoe/kraken-dca-scheduler.git

cd kraken-dca-scheduler
```

---

# Environment Configuration

Create `.env` file in project root:

```env
# Kraken API
KRAKEN_API_KEY=YOUR_API_KEY
KRAKEN_API_SECRET=YOUR_API_SECRET

# Scheduler
ENABLE_SCHEDULER=true

TRADE_DAY=mon
TRADE_HOUR=1
TRADE_MIN=58

TZ=Europe/Amsterdam

# Trade amounts
BTC_EUR_AMOUNT=160
ETH_EUR_AMOUNT=40

# Safety
DRY_RUN=false
```

---

# Dry Run

When:

```env
DRY_RUN=true
```

orders are simulated and not sent to Kraken.

---

# Build and Start

## Initial build

```bash
docker compose up -d --build
```

## Start existing container

```bash
docker compose up -d
```

## Restart container

```bash
docker compose restart kraken-dca
```

---

# Swagger UI

After startup:

```text
http://localhost:8000/docs
```

OpenAPI schema:

```text
http://localhost:8000/openapi.json
```

---

# Available Endpoints

## Buy BTC

```http
POST /v1/trades/btc
```

Body:

```json
{
  "amount": 50
}
```

---

## Buy ETH

```http
POST /v1/trades/eth
```

Body:

```json
{
  "amount": 25
}
```

---

## Execute DCA

```http
POST /v1/trades/dca
```

Body:

```json
{
  "btc_amount": 160,
  "eth_amount": 40
}
```

---

# Logs

View logs:

```bash
docker logs -f kraken-dca
```

---

# Updating Code

Because the source folder is bind-mounted:

```yaml
volumes:
  - ./src:/app/src
```

code changes become available immediately inside the container.

After code changes:

```bash
docker compose restart kraken-dca
```

No rebuild required.

---

# Rebuild Required When

Rebuild is only required when changing:

- Dockerfile
- requirements.txt
- system dependencies

Then run:

```bash
docker compose up -d --build
```

---

# Example Workflow

## Start app

```bash
docker compose up -d
```

## Open Swagger

```text
http://localhost:8000/docs
```

## Execute manual trade

Use Swagger UI or:

```bash
curl -X POST http://localhost:8000/v1/trades/btc \
-H "Content-Type: application/json" \
-d '{"amount":25}'
```

---

# Security Notes

Never commit:

- `.env`
- Kraken API keys
- secrets

Use API keys with:

- trading permissions only
- no withdrawal permissions

---

# Future Improvements

- Database-backed trade history
- Persistent order tracking
- Telegram notifications
- Health monitoring
- Unit tests
- Authentication middleware
- Multi-asset support
- Exchange abstraction layer