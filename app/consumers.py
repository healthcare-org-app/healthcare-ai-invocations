"""Kafka consumers for ai-invocations-service.

One handler per subscribed topic. Real handlers write to this service's own
database and/or publish follow-up events; stub handlers just log + audit.
"""
from __future__ import annotations

import logging

from psycopg.types.json import Json

from healthcare_common.audit import emit_audit

log = logging.getLogger("ai-invocations-service.consumers")

TABLE = "ai_invocations"


def register(svc) -> None:
    bus = svc.bus
    db = svc.db
    clients = svc.clients

    @bus.on("lab.result.available")
    def _on_lab_result_available(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    db.execute(f"INSERT INTO {TABLE} (data) VALUES (%s)",
                               (Json({"trigger": "lab.result.available",
                                      "patient_id": data.get("patient_id"),
                                      "state": "queued_for_review"}),))
        except Exception as e:
            log.exception("ai-invocations-service/lab.result.available handler failed: %s", e)
        emit_audit(bus, action="consume.lab.result.available", actor="system:ai-invocations-service",
                   target=None, details={"envelope_id": envelope.get("id")})

    @bus.on("encounter.started")
    def _on_encounter_started(envelope: dict) -> None:
        data = envelope.get("data") or {}
        try:
                    db.execute(f"INSERT INTO {TABLE} (data) VALUES (%s)",
                               (Json({"trigger": "encounter.started",
                                      "patient_id": data.get("patient_id"),
                                      "state": "queued_for_triage"}),))
        except Exception as e:
            log.exception("ai-invocations-service/encounter.started handler failed: %s", e)
        emit_audit(bus, action="consume.encounter.started", actor="system:ai-invocations-service",
                   target=None, details={"envelope_id": envelope.get("id")})

