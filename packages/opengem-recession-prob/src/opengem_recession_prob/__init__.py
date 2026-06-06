"""Bauer-Mertens term-spread recession probability engine."""

from opengem_recession_prob.model import (
    BAUER_MERTENS_US_PARAMS,
    RecessionProbabilityResult,
    TermSpreadModel,
    recession_probability,
)

__all__ = [
    "BAUER_MERTENS_US_PARAMS",
    "RecessionProbabilityResult",
    "TermSpreadModel",
    "recession_probability",
]
__version__ = "0.1.0"
