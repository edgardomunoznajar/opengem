"""Frequency — observation/release cadence enum."""

from __future__ import annotations

from enum import StrEnum


class Frequency(StrEnum):
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"
    QUARTERLY = "Q"
    ANNUAL = "A"
