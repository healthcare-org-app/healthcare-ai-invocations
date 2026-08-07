# ai-invocations-service

ai-invocations-service — domain: ai_agents

- **Port:** 9101
- **Language:** Python 3.11 + Flask
- **Database:** `ai_agents` (Postgres, table `ai_invocations`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/ai_invocations/`          |
| POST      | `/api/ai_invocations/`          |
| GET       | `/api/ai_invocations/<id>`      |
| PUT/PATCH | `/api/ai_invocations/<id>`      |
| DELETE    | `/api/ai_invocations/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** (none)
**Subscribes:** lab.result.available, encounter.started

## HTTP peer dependencies

- `ai-agents-service`
- `ml-models-service`
- `patient-consent-service`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
