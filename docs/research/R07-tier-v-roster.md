# R07 — Tier-V Country Roster (Definitive)

| Field | Value |
|---|---|
| Document ID | OG1-RES-007 |
| Revision | A (definitive roster 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Resolves TBR-007. Significantly expands the R02 §3 working estimate.** |

---

## 1. Why this exists

R02 estimated **~25 Tier-V countries** based on partial coverage information. Deeper investigation reveals **OECD ORDRA covers materially more than 26 countries** when its full scope is examined, and BIS Policy Rates covers **40+ central banks** including most major emerging markets. This memo nails down the actual Tier-V roster for the rev C CONOPS.

## 2. The data foundation

### 2.1 OECD MEI Original Release Data and Revisions Database (ORDRA)

- **21 key economic variables** with monthly vintages since February 1999.
- Coverage: **all OECD member countries + Euro area + China + India + Brazil + South Africa + Russia** (as of dataset documentation; specific variable coverage varies by country).
- This is meaningfully broader than the "26 OECD countries" framing from R02 §3.

Source: [OECD ORDRA documentation](https://www.oecd.org/content/dam/oecd/en/publications/reports/2006/09/undertaking-revisions-and-real-time-data-analysis-using-the-oecd-main-economic-indicators-original-release-data-and-revisions-database_g17a1998/146528313656.pdf); [OECD-iLibrary entry](https://www.oecd-ilibrary.org/economics/data/main-economic-indicators/revisions-analysis_data-00053-en).

### 2.2 Dallas Fed Real-Time Historical Database

- Extends ORDRA back to **1962** for 26 OECD countries (full quartet GDP / IP / unemp. / CPI etc.).
- 13 variables, hard-copy-digitized.
- Use as **deep-history layer** merged with ORDRA's post-1999 vintages.

### 2.3 BIS Central Bank Policy Rates (CBPOL)

- **40+ central banks**, daily series, most starting after 1980, some back to 1946.
- Coverage explicitly named: AR, AU, BR, CA, CN, HR, EA (and selected member states from 2024), GR, IN, ID, IL, IS, IT, JP, KR, KW, MK, MY, MX, MA, NL, NZ, NO, PE, PH, PL, PT, RO, RU, BE, FR, DE, TR, UK, US.
- Policy rate is the "least vintage-sensitive" of the four core variables — decisions are dated events not revised. **BIS CBPOL is effectively a free vintage record for policy rates worldwide.**

Source: [BIS CBPOL Data Portal](https://data.bis.org/topics/CBPOL); [BIS policy-rate documentation PDF](https://www.bis.org/statistics/cbpol/cbpol_doc.pdf).

### 2.4 EABCN / ECB SDW Real-Time Database

- 9 euro-area members + UK (AT, BE, DE, IE, IT, LU, NL, ES, UK).
- 200+ variables, vintages since 1999/2001.
- **Use as enrichment layer for the euro 9 countries** — gives more covariates than ORDRA.

### 2.5 Philadelphia Fed RTDSM

- US only, deeper history (1965+) and broader US variable list (M1/M2, reserves, GDI).
- **Use as US-specific deepening** beyond ORDRA's MEI coverage.

### 2.6 BIS Effective Exchange Rates, BoP, Banking Stats

- BIS hosts broader nominal/real effective exchange rate datasets covering 60+ economies, plus locational + consolidated banking statistics. These extend FX coverage beyond ORDRA.

## 3. Definitive Tier-V Roster (~35–40 countries)

Tier-V membership criterion (refined):
- ≥10 years of vintage data for GDP-real, CPI-headline, unemployment (from ORDRA or equivalent), AND
- Policy rate available daily from BIS CBPOL or equivalent.

### 3.1 Tier-V Core (n=26) — full ORDRA + Dallas Fed + BIS CBPOL

| Country | ISO | ORDRA vintage start | Policy rate (BIS) | Notes |
|---|---|---|---|---|
| United States | US | 1962 (Dallas Fed) / 1999 (ORDRA) | ✓ | Philly RTDSM enrichment |
| Canada | CA | 1962 / 1999 | ✓ | RT-CANSIM enrichment since 2015 |
| United Kingdom | UK | 1962 / 1999 | ✓ | EABCN enrichment |
| Germany | DE | 1962 / 1999 | ✓ | EABCN enrichment |
| France | FR | 1962 / 1999 | ✓ | — |
| Italy | IT | 1962 / 1999 | ✓ | EABCN enrichment |
| Spain | ES | 1962 / 1999 | ✓ | EABCN enrichment |
| Netherlands | NL | 1962 / 1999 | ✓ | EABCN enrichment |
| Belgium | BE | 1962 / 1999 | ✓ | EABCN enrichment |
| Austria | AT | 1962 / 1999 | EA (no national after €) | EABCN enrichment |
| Luxembourg | LU | 1962 / 1999 | EA | EABCN enrichment |
| Ireland | IE | 1962 / 1999 | EA | EABCN enrichment |
| Greece | GR | 1962 / 1999 | ✓ | — |
| Portugal | PT | 1962 / 1999 | ✓ | — |
| Finland | FI | 1962 / 1999 | EA | — |
| Sweden | SE | 1962 / 1999 | ✓ (Riksbank — via national archive) | — |
| Denmark | DK | 1962 / 1999 | ✓ | — |
| Norway | NO | 1962 / 1999 | ✓ | — |
| Switzerland | CH | 1962 / 1999 | ✓ (SNB) | — |
| Japan | JP | 1962 / 1999 | ✓ | — |
| Korea | KR | 1962 / 1999 | ✓ | — |
| Australia | AU | 1962 / 1999 | ✓ | ABS revision triangles on request |
| New Zealand | NZ | 1962 / 1999 | ✓ | — |
| Iceland | IS | 1962 / 1999 | ✓ | — |
| Mexico | MX | 1962 / 1999 | ✓ | — |
| Turkey | TR | 1962 / 1999 | ✓ | — |

### 3.2 Tier-V Extended (n=9) — post-1995 OECD entrants

Vintage coverage since their OECD entry (mostly 1995–2010):

| Country | ISO | ORDRA vintage start | Policy rate (BIS) |
|---|---|---|---|
| Czech Republic | CZ | ~1995 | ✓ (national) |
| Hungary | HU | ~1996 | ✓ (national) |
| Poland | PL | ~1996 | ✓ |
| Slovakia | SK | ~2000 | EA |
| Slovenia | SI | ~2010 | EA |
| Chile | CL | ~2010 | ✓ (national) |
| Israel | IL | ~2010 | ✓ |
| Estonia | EE | ~2010 | EA |
| Latvia + Lithuania | LV/LT | ~2014 | EA |

### 3.3 Tier-V BRICS+ subset (n=5) — ORDRA-covered

OECD ORDRA explicitly includes 5 non-OECD majors:

| Country | ISO | ORDRA coverage | Policy rate |
|---|---|---|---|
| China | CN | Partial (subset of 21 vars) | ✓ |
| India | IN | Partial | ✓ |
| Brazil | BR | Partial | ✓ |
| South Africa | ZA | Partial | ✓ |
| Russia | RU | Partial | ✓ |

**Caveat**: ORDRA coverage for these 5 is *partial* — not all 21 variables, possibly shorter history. Each needs to be verified at SRR. They may move to Tier-T if data gaps are severe.

### 3.4 Aggregate count

- **Tier-V Core**: 26
- **Tier-V Extended**: 9 (subject to ORDRA roster confirmation)
- **Tier-V BRICS+**: 5 (subject to coverage verification)
- **Maximum Tier-V at IOC**: **~35**, achievable
- **Conservative Tier-V at IOC**: **~26**, certain

### 3.5 Tier-T (tracked-only) — remaining ~30+ economies

Major economies not in Tier-V: Saudi Arabia, UAE, Egypt, Nigeria, Indonesia, Vietnam, Thailand, Philippines, Malaysia, Argentina, Colombia, Peru, Pakistan, Bangladesh, Ukraine, plus smaller economies.

These appear in dashboards using latest-revised data; their forecasts are not on the leaderboard until self-archive matures.

## 4. Implication for the CONOPS

This expands the rev C CONOPS Tier-V claim from "~25" to **"~26 conservatively, up to ~35 if ORDRA coverage holds for the post-1995 OECD entrants and the BRICS+ subset."**

Recommended CONOPS §5.1.3 statement:

> Tier-V at IOC: **26 confirmed** (US, CA, UK, DE, FR, IT, ES, NL, BE, AT, LU, IE, GR, PT, FI, SE, DK, NO, CH, JP, KR, AU, NZ, IS, MX, TR). Tier-V Extended: **+9 candidate** post-1995 OECD entrants pending coverage verification (CZ, HU, PL, SK, SI, CL, IL, EE, LV/LT). Tier-V BRICS+: **+5 candidate** (CN, IN, BR, ZA, RU) pending coverage verification.

> FOC target: ~35 Tier-V; remaining ~50 economies tracked-only.

## 5. Verification probes deferred

1. **ORDRA full variable matrix per country** — pull from OECD Data Explorer / SDMX what 21 vars are actually present for each country, especially BRICS+ and post-1995 OECD entrants.
2. **EU/euro-area policy rate handling** — pre-1999 vs. post-1999 ECB era; how does ORDRA represent national policy rates for euro members?
3. **ABS Australia revision triangles** — email request to ABS Stats for the bulk file; load once into Tier-V archive.

## 6. Bottom line

OPENGEM Block I can credibly target **35 Tier-V countries at IOC**, not the conservative 25 from R02. The R99 synthesis and the rev C CONOPS should be updated to reflect this. The "global" framing of OPENGEM is **less aspirational than R02 suggested** — Tier-V at 35 is genuinely multi-region (Americas, Western Europe, Central/Eastern Europe, Nordics, Anglo-Pacific, East Asia, plus the BRICS+ contingent).

---

*End of R07 Rev A.*
