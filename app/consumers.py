"""Kafka consumers for ai-invocations-service.

One handler per subscribed topic. Handlers are best-effort logging plus
audit — services override this file to implement real cross-domain behavior.
"""
from __future__ import annotations

import logging

from healthcare_common.audit import emit_audit

log = logging.getLogger("ai-invocations-service.consumers")


def register(svc) -> None:
    bus = svc.bus

    @bus.on("lab.result.available")
    def _on_lab_result_available(envelope: dict) -> None:
        log.info("ai-invocations-service: received lab.result.available id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.lab.result.available", actor="system:ai-invocations-service",
                   target=None, details={"envelope_id": envelope.get("id")})

    @bus.on("encounter.started")
    def _on_encounter_started(envelope: dict) -> None:
        log.info("ai-invocations-service: received encounter.started id=%s", envelope.get("id"))
        emit_audit(bus, action="consume.encounter.started", actor="system:ai-invocations-service",
                   target=None, details={"envelope_id": envelope.get("id")})

