"""Variable kinds — canonical OPENGEM variable identifiers."""

from __future__ import annotations

from enum import StrEnum


class Variable(StrEnum):
    """Canonical OPENGEM variable kinds.

    Note: a SeriesId encodes a specific source's series; a Variable encodes the
    abstract economic concept across sources (e.g., both BLS CPI and Eurostat
    HICP map to Variable.CPI_HEADLINE).
    """

    GDP_REAL = "gdp_real"
    GDP_NOMINAL = "gdp_nominal"
    GDP_DEFLATOR = "gdp_deflator"
    GDP_YOY = "gdp_yoy"  # real GDP growth, year-over-year — a first-class L3 forecast target
    CPI_HEADLINE = "cpi_headline"
    CPI_CORE = "cpi_core"
    CPI_YOY = "cpi_yoy"  # headline CPI inflation, year-over-year — first-class L3 forecast target
    PCE_HEADLINE = "pce_headline"
    PCE_CORE = "pce_core"
    UNEMPLOYMENT_RATE = "unemployment_rate"
    POLICY_RATE = "policy_rate"
    POLICY_RATE_FORWARD = "policy_rate_forward"  # curve-implied
    INDUSTRIAL_PRODUCTION = "industrial_production"
    CAPACITY_UTILIZATION = "capacity_utilization"
    M2 = "m2"
    NONFARM_PAYROLLS = "nonfarm_payrolls"
    YIELD_10Y = "yield_10y"
    YIELD_2Y = "yield_2y"
    YIELD_3M = "yield_3m"
    TERM_SPREAD_10Y_3M = "term_spread_10y_3m"
    EQUITY_INDEX = "equity_index"
    FX_NOMINAL = "fx_nominal"
    FX_REAL_EFFECTIVE = "fx_real_effective"
    CURRENT_ACCOUNT = "current_account"
    TRADE_BALANCE = "trade_balance"
    FISCAL_BALANCE = "fiscal_balance"
    INVENTORY_TO_SALES = "inventory_to_sales"
    # Information-surface
    GSCPI = "gscpi"
    PORT_CONGESTION = "port_congestion"
    GPR = "gpr"
    GDELT_TONE = "gdelt_tone"
    # Derived
    RECESSION_PROB_12M = "recession_prob_12m"
