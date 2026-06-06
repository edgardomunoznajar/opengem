"""MarketThresholdDetector — detects events from financial market threshold crosses."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime

from opengem_event_detector.event import Event, EventSeverity, EventSource


@dataclass(frozen=True, slots=True)
class MarketSignal:
    """One observation of a market signal."""

    name: str
    value: float
    as_of: datetime


class MarketThresholdDetector:
    """Emits events when monitored market signals cross documented thresholds.

    Default thresholds (per R06 §2 D-MKT):
    - term spread 10y-3m < 0 → recession risk event
    - VIX > 35 → equity stress event
    - BAA-10y spread > 400bp → credit stress event
    """

    DEFAULT_THRESHOLDS: dict[str, tuple[str, float, EventSeverity, tuple[str, ...]]] = {
        "term_spread_10y_3m": ("<", 0.0, EventSeverity.HIGH, ("recession", "yield-curve")),
        "vix": (">", 35.0, EventSeverity.HIGH, ("volatility", "risk-off", "equity")),
        "baa_10y_spread_bp": (">", 400.0, EventSeverity.MEDIUM, ("credit", "risk-off")),
    }

    def __init__(
        self,
        thresholds: dict[str, tuple[str, float, EventSeverity, tuple[str, ...]]] | None = None,
    ) -> None:
        self._thresholds = thresholds if thresholds is not None else self.DEFAULT_THRESHOLDS

    def detect(self, signals: list[MarketSignal]) -> Iterator[Event]:
        for sig in signals:
            spec = self._thresholds.get(sig.name)
            if spec is None:
                continue
            op, thr, severity, tags = spec
            triggered = (op == "<" and sig.value < thr) or (op == ">" and sig.value > thr)
            if triggered:
                yield Event(
                    event_id=f"market.{sig.name}.{sig.as_of.isoformat()}",
                    detected_at=sig.as_of,
                    source=EventSource.MARKET,
                    severity=severity,
                    title=f"{sig.name} threshold crossed: {sig.value} {op} {thr}",
                    summary=(
                        f"Market signal {sig.name} = {sig.value} crossed threshold "
                        f"{op} {thr} indicating {', '.join(tags)} regime."
                    ),
                    tags=tags,
                    metadata={"signal": sig.name, "value": str(sig.value), "threshold": str(thr)},
                )
