"""Country codes — ISO 3166-1 alpha-2 + OPENGEM canonical region codes (EA)."""

from __future__ import annotations

from enum import StrEnum


class Country(StrEnum):
    """ISO 3166-1 alpha-2 country codes, plus EA for the Euro Area aggregate.

    Only the codes OPENGEM actually uses are declared. Adding a new country
    is intentionally a one-line change so the roster is reviewable.
    """

    # Tier-V Core (rev C CONOPS)
    US = "US"
    CA = "CA"
    UK = "UK"
    DE = "DE"
    FR = "FR"
    IT = "IT"
    ES = "ES"
    NL = "NL"
    BE = "BE"
    AT = "AT"
    LU = "LU"
    IE = "IE"
    GR = "GR"
    PT = "PT"
    FI = "FI"
    SE = "SE"
    DK = "DK"
    NO = "NO"
    CH = "CH"
    JP = "JP"
    KR = "KR"
    AU = "AU"
    NZ = "NZ"
    IS = "IS"
    MX = "MX"
    TR = "TR"
    # Tier-V Extended
    CZ = "CZ"
    HU = "HU"
    PL = "PL"
    SK = "SK"
    SI = "SI"
    CL = "CL"
    IL = "IL"
    EE = "EE"
    LV = "LV"
    LT = "LT"
    # Tier-V BRICS+ (subject to ORDRA coverage verification)
    CN = "CN"
    IN = "IN"
    BR = "BR"
    ZA = "ZA"
    RU = "RU"
    # Tier-T scenario-relevant (tracked-only; appear in scenarios but not on V&V leaderboard)
    SA = "SA"  # Saudi Arabia
    AE = "AE"  # UAE
    EG = "EG"  # Egypt
    NG = "NG"  # Nigeria
    UA = "UA"  # Ukraine
    HK = "HK"  # Hong Kong
    SG = "SG"  # Singapore
    TW = "TW"  # Taiwan
    ID = "ID"  # Indonesia
    TH = "TH"  # Thailand
    PH = "PH"  # Philippines
    MY = "MY"  # Malaysia
    VN = "VN"  # Vietnam
    AR = "AR"  # Argentina
    CO = "CO"  # Colombia
    PE = "PE"  # Peru
    VE = "VE"  # Venezuela
    IR = "IR"  # Iran
    # Aggregates
    EA = "EA"  # Euro Area aggregate
    WORLD = "WORLD"

    @classmethod
    def tier_v_core(cls) -> frozenset[Country]:
        return frozenset(
            {
                cls.US, cls.CA, cls.UK, cls.DE, cls.FR, cls.IT, cls.ES, cls.NL,
                cls.BE, cls.AT, cls.LU, cls.IE, cls.GR, cls.PT, cls.FI, cls.SE,
                cls.DK, cls.NO, cls.CH, cls.JP, cls.KR, cls.AU, cls.NZ, cls.IS,
                cls.MX, cls.TR,
            }
        )

    @classmethod
    def tier_v_extended(cls) -> frozenset[Country]:
        return cls.tier_v_core() | frozenset(
            {cls.CZ, cls.HU, cls.PL, cls.SK, cls.SI, cls.CL, cls.IL, cls.EE, cls.LV, cls.LT}
        )
