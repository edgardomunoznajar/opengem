from __future__ import annotations

import random
from datetime import date

import pytest
from opengem_recession_prob import (
    BAUER_MERTENS_US_PARAMS,
    TermSpreadModel,
    recession_probability,
)
from opengem_recession_prob.model import _phi, fit_probit_irls


def test_phi_monotone_at_zero() -> None:
    """Phi(0) = 0.5; Phi is monotone increasing."""
    assert _phi(0.0) == pytest.approx(0.5)
    assert _phi(-1.0) < _phi(0.0) < _phi(1.0)


def test_phi_extremes() -> None:
    assert _phi(-5.0) == pytest.approx(0.0, abs=1e-5)
    assert _phi(5.0) == pytest.approx(1.0, abs=1e-5)


def test_bauer_mertens_at_flat_curve() -> None:
    """At spread = 0bp (flat curve), Phi(alpha) = baseline recession probability."""
    result = recession_probability(spread_bp=0.0, as_of=date(2026, 5, 25))
    # alpha = -0.55 → Phi(-0.55) ≈ 0.29
    assert result.probability == pytest.approx(0.29, abs=0.02)


def test_bauer_mertens_at_inverted_curve() -> None:
    """At spread = -100bp (deeply inverted), probability should be quite high."""
    result = recession_probability(spread_bp=-100.0, as_of=date(2026, 5, 25))
    # z = -0.55 + (-0.014)*(-100) = -0.55 + 1.4 = 0.85 → Phi(0.85) ≈ 0.80
    assert result.probability > 0.7


def test_bauer_mertens_at_steep_curve() -> None:
    """At spread = +200bp (very steep), probability should be very low."""
    result = recession_probability(spread_bp=200.0, as_of=date(2026, 5, 25))
    # z = -0.55 + (-0.014)*200 = -3.35 → Phi(-3.35) ≈ 0.0004
    assert result.probability < 0.05


def test_result_carries_provenance() -> None:
    result = recession_probability(spread_bp=-50.0, as_of=date(2026, 5, 25))
    assert result.term_spread_bp == -50.0
    assert result.horizon_months == 12
    assert result.auc is not None
    assert result.model_id.startswith("us_12m_")


def test_custom_model_can_be_passed() -> None:
    """Users can provide their own calibrated model."""
    custom = TermSpreadModel(
        country=BAUER_MERTENS_US_PARAMS.country,
        horizon_months=6,
        alpha=-0.3,
        beta=-0.01,
    )
    r = recession_probability(spread_bp=0.0, as_of=date(2026, 5, 25), model=custom)
    assert r.horizon_months == 6


def test_fit_probit_irls_recovers_signal() -> None:
    """Synthetic data: probit fit should recover an approximate alpha/beta."""
    rng = random.Random(42)
    true_alpha = -0.5
    true_beta = -0.02
    n = 500
    spreads = [rng.uniform(-200, 300) for _ in range(n)]
    recession = []
    for s in spreads:
        z = true_alpha + true_beta * s
        p = _phi(z)
        recession.append(1 if rng.random() < p else 0)

    alpha_hat, beta_hat = fit_probit_irls(spreads, recession)
    # Should be within rough tolerance — IRLS on noisy synthetic probit data
    assert abs(alpha_hat - true_alpha) < 0.5
    assert abs(beta_hat - true_beta) < 0.015
    # Signs should be correct
    assert beta_hat < 0


def test_fit_probit_rejects_short_data() -> None:
    with pytest.raises(ValueError):
        fit_probit_irls([0.0] * 5, [0] * 5)


def test_fit_probit_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        fit_probit_irls([0.0, 1.0, 2.0], [0, 1])


def test_to_conditional_frames_correctly() -> None:
    """RecessionProbabilityResult.to_conditional renders the epistemic contract."""
    result = recession_probability(spread_bp=-50.0, as_of=date(2026, 5, 25))
    c = result.to_conditional()
    text = c.render_human()
    assert "could happen" in text
    assert "based on" in text
    assert "-50" in text or "50bp" in text
    assert len(c.basis.caveats) >= 1
    assert c.basis.citations
    assert c.conditional_on
