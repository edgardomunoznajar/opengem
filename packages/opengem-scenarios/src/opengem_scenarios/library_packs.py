"""Default canonical scenario packs — the IOC library.

Per R10 / R20 / R23 of the design dossier and the program-owner direction that
OPENGEM's headline product is a scenario engine for a geopolitics YouTuber whose
comp-set is "ChatGPT and nothing else."

Each pack is a curated, cited, structurally-identified shock specification. Packs
are templates; runtime scaling and country additions happen at ScenarioInvocation.
"""

from __future__ import annotations

from datetime import date

from opengem_types import Country, Identification, ScenarioSpec, Shock, ShockType, Variable

from opengem_scenarios.pack import ScenarioPack


def _ref_date() -> date:
    # Reference start period — invocation overrides this at runtime
    return date(2026, 7, 1)


def _pack_russia_ukraine_energy() -> ScenarioPack:
    return ScenarioPack(
        pack_id="russia-ukraine-energy",
        title="Russia-Ukraine energy disruption",
        summary=(
            "Continuation or escalation of Russia-Ukraine conflict produces a "
            "sustained shock to European natural gas and global oil prices. "
            "Effects: EU GDP down, OECD inflation up, ECB rate path higher."
        ),
        tags=("russia", "ukraine", "energy", "oil", "gas", "europe", "war"),
        regions=(Country.EA, Country.DE, Country.IT, Country.ES, Country.FR, Country.NL, Country.RU),
        rationale=(
            "Caldara-Iacoviello GPR for RU is a leading indicator; historical "
            "oil-price shocks of $20-40/bbl produce -0.3 to -0.8pp Euro Area "
            "GDP at 4Q (Hamilton 2003; IEA energy-shock literature). "
            "Identification: oil-supply shock + EU gas-import disruption "
            "Cholesky-ordered to allow demand-side response."
        ),
        references=(
            "Caldara-Iacoviello (2022) GPR Index",
            "Hamilton (2003) JoE oil-price shocks",
            "IEA World Energy Outlook scenario library",
        ),
        template=ScenarioSpec(
            scenario_id="russia-ukraine-energy",
            shocks=(
                Shock(
                    country=Country.RU,
                    variable=Variable.EQUITY_INDEX,
                    magnitude=-15.0,
                    unit="pct",
                    start_period=_ref_date(),
                    length_quarters=2,
                ),
                # Surrogate oil price shock via EA terms-of-trade proxy
                Shock(
                    country=Country.EA,
                    variable=Variable.GDP_DEFLATOR,
                    magnitude=2.0,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.STRUCTURAL,
            target_countries=(Country.EA, Country.DE, Country.IT, Country.UK, Country.US),
            target_variables=(Variable.GDP_REAL, Variable.CPI_HEADLINE, Variable.POLICY_RATE),
            target_horizons_q=(1, 4, 8),
        ),
    )


def _pack_china_taiwan_disruption() -> ScenarioPack:
    return ScenarioPack(
        pack_id="china-taiwan-disruption",
        title="China-Taiwan strategic disruption",
        summary=(
            "Escalation in the Taiwan Strait (blockade, sanctions, or limited "
            "kinetic action) disrupts semiconductor supply chains globally. "
            "Effects: US/EU/JP tech sectors contract; global supply chain "
            "pressure spikes; CN GDP slows; KR/JP semiconductors directly hit."
        ),
        tags=("china", "taiwan", "semiconductors", "supply-chain", "tech", "asia"),
        regions=(Country.CN, Country.JP, Country.KR, Country.US, Country.DE),
        rationale=(
            "TSMC produces ~90% of leading-edge semiconductors. Sustained "
            "disruption maps to GSCPI spike of +2 to +4 sigma (similar to "
            "2021-2022 supply-chain crisis). NY Fed Liberty Street estimates "
            "supply-chain stress of this magnitude adds ~1pp to PPI inflation "
            "in the US and EA at 4Q."
        ),
        references=(
            "NY Fed SR1017 (GSCPI methodology)",
            "Boehm-Flaaen-Pandalai-Nayar (2019) — Japan tsunami supply-chain effects",
        ),
        template=ScenarioSpec(
            scenario_id="china-taiwan-disruption",
            shocks=(
                Shock(
                    country=Country.CN,
                    variable=Variable.GDP_REAL,
                    magnitude=-2.0,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
                # GSCPI proxy shock: feed into supply-chain pressure via terms-of-trade
                Shock(
                    country=Country.US,
                    variable=Variable.GDP_DEFLATOR,
                    magnitude=1.0,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.STRUCTURAL,
            target_countries=(Country.US, Country.JP, Country.KR, Country.DE, Country.EA, Country.CN),
            target_variables=(
                Variable.GDP_REAL,
                Variable.CPI_HEADLINE,
                Variable.INDUSTRIAL_PRODUCTION,
            ),
            target_horizons_q=(1, 4, 8),
        ),
    )


def _pack_iran_israel_escalation() -> ScenarioPack:
    return ScenarioPack(
        pack_id="iran-israel-escalation",
        title="Iran-Israel direct escalation",
        summary=(
            "Direct kinetic exchange between Iran and Israel triggers oil-price "
            "spike (Hormuz risk premium), regional GPR surge, and global risk-off."
        ),
        tags=("iran", "israel", "oil", "middle-east", "war", "hormuz"),
        regions=(Country.IL, Country.US, Country.EA, Country.SA, Country.TR),
        rationale=(
            "Strait of Hormuz carries ~20% of global oil. Even partial "
            "disruption produces $30-60/bbl oil-price spike based on historical "
            "Hormuz episodes (1980s tanker war comparator). GPR spikes 50-150 "
            "points (Caldara-Iacoviello)."
        ),
        references=(
            "Caldara-Iacoviello GPR country-specific series for IR and IL",
            "Hamilton oil-price shocks literature",
        ),
        template=ScenarioSpec(
            scenario_id="iran-israel-escalation",
            shocks=(
                Shock(
                    country=Country.IL,
                    variable=Variable.GPR,
                    magnitude=100.0,
                    unit="level",
                    start_period=_ref_date(),
                    length_quarters=2,
                ),
                Shock(
                    country=Country.US,
                    variable=Variable.GDP_DEFLATOR,
                    magnitude=1.5,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=2,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.NARRATIVE,
            target_countries=(Country.US, Country.EA, Country.UK, Country.JP, Country.IL),
            target_variables=(Variable.GDP_REAL, Variable.CPI_HEADLINE, Variable.EQUITY_INDEX),
            target_horizons_q=(1, 2, 4),
        ),
    )


def _pack_fed_plus_100bp() -> ScenarioPack:
    return ScenarioPack(
        pack_id="fed-plus-100bp",
        title="Fed surprise +100bp tightening",
        summary=(
            "FOMC surprise upward shift of policy rate by 100bp above curve. "
            "Effects: US GDP contracts, USD strengthens, EM sovereign spreads widen."
        ),
        tags=("fed", "monetary", "us", "rates", "tightening"),
        regions=(Country.US, Country.EA, Country.JP, Country.MX, Country.BR),
        rationale=(
            "Romer-Romer monetary shocks and Gertler-Karadi high-frequency shock "
            "literature: +100bp shock reduces US real GDP by ~1pp at 4Q, ~1.5pp "
            "at 8Q, with persistent dollar strength."
        ),
        references=(
            "Romer & Romer (2004) AER monetary shocks",
            "Gertler & Karadi (2015) AEJ-Macro",
        ),
        template=ScenarioSpec(
            scenario_id="fed-plus-100bp",
            shocks=(
                Shock(
                    country=Country.US,
                    variable=Variable.POLICY_RATE,
                    magnitude=1.0,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.STRUCTURAL,
            target_countries=(Country.US, Country.EA, Country.JP, Country.UK, Country.MX, Country.BR),
            target_variables=(Variable.GDP_REAL, Variable.CPI_HEADLINE, Variable.FX_NOMINAL),
            target_horizons_q=(1, 4, 8),
        ),
    )


def _pack_opec_supply_cut() -> ScenarioPack:
    return ScenarioPack(
        pack_id="opec-supply-cut",
        title="OPEC+ aggressive supply cut",
        summary="OPEC+ announces a >2mbpd production cut; oil prices spike $20+/bbl.",
        tags=("opec", "oil", "supply", "saudi", "energy"),
        regions=(Country.SA, Country.US, Country.EA, Country.JP, Country.CN),
        rationale=(
            "Historical OPEC supply-cut shocks of similar magnitude (1979, 2008, "
            "2022) produce 2-4 quarters of elevated inflation in oil-importing "
            "OECD economies. EM oil importers see growth drag."
        ),
        references=("Hamilton (2003) JoE", "IEA Oil Market Reports"),
        template=ScenarioSpec(
            scenario_id="opec-supply-cut",
            shocks=(
                Shock(
                    country=Country.SA,
                    variable=Variable.GDP_DEFLATOR,
                    magnitude=3.0,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.STRUCTURAL,
            target_countries=(Country.US, Country.EA, Country.JP, Country.IN, Country.CN),
            target_variables=(Variable.CPI_HEADLINE, Variable.GDP_REAL),
            target_horizons_q=(1, 4, 8),
        ),
    )


def _pack_eu_energy_shock() -> ScenarioPack:
    return ScenarioPack(
        pack_id="eu-energy-shock",
        title="EU gas-price shock",
        summary="Sustained doubling of European TTF gas prices (Russia, Algeria, or LNG disruption).",
        tags=("eu", "europe", "energy", "gas", "ttf"),
        regions=(Country.DE, Country.IT, Country.FR, Country.NL, Country.EA),
        rationale=(
            "ECB working papers estimate EA real GDP drag of 0.5-1.5pp per "
            "doubling of gas prices for 1 year, with Germany hit hardest due "
            "to industrial gas intensity."
        ),
        references=("ECB Economic Bulletin energy-shock analyses 2022-2024",),
        template=ScenarioSpec(
            scenario_id="eu-energy-shock",
            shocks=(
                Shock(
                    country=Country.EA,
                    variable=Variable.GDP_DEFLATOR,
                    magnitude=2.5,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.STRUCTURAL,
            target_countries=(Country.DE, Country.IT, Country.FR, Country.NL, Country.EA),
            target_variables=(Variable.GDP_REAL, Variable.CPI_HEADLINE, Variable.INDUSTRIAL_PRODUCTION),
            target_horizons_q=(1, 4, 8),
        ),
    )


def _pack_us_election_fiscal_regime() -> ScenarioPack:
    return ScenarioPack(
        pack_id="us-election-fiscal-regime",
        title="US election fiscal regime change",
        summary=(
            "Post-election shift in US fiscal stance (large stimulus or large "
            "consolidation). Models a structural change in the fiscal-policy "
            "reaction function."
        ),
        tags=("us", "election", "fiscal", "politics", "regime"),
        regions=(Country.US, Country.EA, Country.MX, Country.CA),
        rationale=(
            "Romer-Romer fiscal-shock identification. ±1% of GDP unanticipated "
            "fiscal impulse produces 0.5-1.5pp GDP response."
        ),
        references=("Romer & Romer (2010) AER tax shocks",),
        template=ScenarioSpec(
            scenario_id="us-election-fiscal-regime",
            shocks=(
                Shock(
                    country=Country.US,
                    variable=Variable.GDP_REAL,
                    magnitude=1.5,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=8,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.NARRATIVE,
            target_countries=(Country.US, Country.MX, Country.CA, Country.EA),
            target_variables=(Variable.GDP_REAL, Variable.POLICY_RATE, Variable.FISCAL_BALANCE),
            target_horizons_q=(1, 4, 8, 20),
        ),
    )


def _pack_china_stimulus() -> ScenarioPack:
    return ScenarioPack(
        pack_id="china-stimulus",
        title="China large fiscal+monetary stimulus",
        summary=(
            "PBOC + MoF coordinated stimulus producing CN growth lift; spillovers "
            "to commodity exporters (BR, AU, CL) via terms of trade."
        ),
        tags=("china", "stimulus", "commodities", "asia", "emerging-markets"),
        regions=(Country.CN, Country.AU, Country.BR, Country.CL),
        rationale=(
            "Chinese stimulus episodes (2008-09, 2015-16) lifted commodity "
            "prices 10-30% with corresponding CA improvement in commodity "
            "exporters."
        ),
        references=("BIS WP on China spillovers", "IMF WEO chapters on China"),
        template=ScenarioSpec(
            scenario_id="china-stimulus",
            shocks=(
                Shock(
                    country=Country.CN,
                    variable=Variable.GDP_REAL,
                    magnitude=1.5,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.STRUCTURAL,
            target_countries=(Country.CN, Country.AU, Country.BR, Country.CL, Country.DE),
            target_variables=(Variable.GDP_REAL, Variable.CPI_HEADLINE, Variable.CURRENT_ACCOUNT),
            target_horizons_q=(1, 4, 8),
        ),
    )


def _pack_global_recession() -> ScenarioPack:
    return ScenarioPack(
        pack_id="global-recession-trigger",
        title="Global recession trigger (financial conditions tightening)",
        summary=(
            "Composite financial-conditions tightening + risk-off across DM and EM. "
            "Models a 2008-style global recession trigger."
        ),
        tags=("recession", "global", "credit", "financial", "spillover"),
        regions=(Country.US, Country.EA, Country.JP, Country.UK, Country.BR, Country.IN),
        rationale=(
            "Gilchrist-Zakrajsek excess bond premium shock literature: +1 sigma "
            "EBP shock reduces global IP by 1-2% over 4Q."
        ),
        references=("Gilchrist-Zakrajsek (2012) AER", "IMF WEO recession chapters"),
        template=ScenarioSpec(
            scenario_id="global-recession-trigger",
            shocks=(
                Shock(
                    country=Country.US,
                    variable=Variable.EQUITY_INDEX,
                    magnitude=-25.0,
                    unit="pct",
                    start_period=_ref_date(),
                    length_quarters=2,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.STRUCTURAL,
            target_countries=(Country.US, Country.EA, Country.JP, Country.UK, Country.BR, Country.IN),
            target_variables=(Variable.GDP_REAL, Variable.INDUSTRIAL_PRODUCTION, Variable.UNEMPLOYMENT_RATE),
            target_horizons_q=(1, 4, 8),
        ),
    )


def _pack_tech_export_controls() -> ScenarioPack:
    return ScenarioPack(
        pack_id="sanctions-on-tech",
        title="Tightened US tech-export controls on China",
        summary=(
            "Expansion of US (and allied) chip-export controls hits Chinese "
            "tech sector and global semiconductor supply chains."
        ),
        tags=("sanctions", "tech", "semiconductors", "china", "us", "export-controls"),
        regions=(Country.US, Country.CN, Country.KR, Country.JP, Country.NL),
        rationale=(
            "Chad Bown / PIIE estimates: comprehensive chip-export controls "
            "could reduce Chinese semiconductor output by 15-25% in affected "
            "tiers; spillover to KR/JP equipment producers."
        ),
        references=("Chad Bown PIIE working papers on export controls",),
        template=ScenarioSpec(
            scenario_id="sanctions-on-tech",
            shocks=(
                Shock(
                    country=Country.CN,
                    variable=Variable.INDUSTRIAL_PRODUCTION,
                    magnitude=-3.0,
                    unit="pp",
                    start_period=_ref_date(),
                    length_quarters=4,
                ),
            ),
            shock_type=ShockType.STRUCTURAL_SHOCK,
            identification=Identification.NARRATIVE,
            target_countries=(Country.CN, Country.KR, Country.JP, Country.US, Country.NL, Country.DE),
            target_variables=(Variable.INDUSTRIAL_PRODUCTION, Variable.GDP_REAL),
            target_horizons_q=(1, 4, 8),
        ),
    )


def build_default_packs() -> list[ScenarioPack]:
    """The 10 canonical packs for IOC."""
    return [
        _pack_russia_ukraine_energy(),
        _pack_china_taiwan_disruption(),
        _pack_iran_israel_escalation(),
        _pack_fed_plus_100bp(),
        _pack_opec_supply_cut(),
        _pack_eu_energy_shock(),
        _pack_us_election_fiscal_regime(),
        _pack_china_stimulus(),
        _pack_global_recession(),
        _pack_tech_export_controls(),
    ]
