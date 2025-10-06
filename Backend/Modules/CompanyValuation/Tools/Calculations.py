"""
Asset-Based Valuation tools.

This module exposes two callable tools that can be attached to an agent:
1) calculate_book_value: Computes Book Value = Total Assets - Total Liabilities
2) estimate_liquidation_value: Computes Liquidation Value using discounted assets minus liabilities

Both tools can:
- Work directly from provided numeric inputs, OR
- Fetch required data from Airtable via helper functions in `CompanyValuationDB`.

Return payloads are structured dicts with numeric results, confidence, and notes.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Optional

try:
    # Prefer local module (within CompanyValuation/Tools)
    from .CompanyValuationDB import get_financial_statements, get_industry_multiples
except Exception:  # pragma: no cover - fallback to sibling Tools placement
    # Fallback to Backend/Tools if imported from another context
    from ..Tools.CompanyValuationDB import get_financial_statements, get_industry_multiples  # type: ignore


# -------------------------------
# Helpers
# -------------------------------

def _safe_lower_keys(d: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(k).lower(): v for k, v in d.items()}


def _extract_fields(record: Mapping[str, Any]) -> Dict[str, Any]:
    """Extracts Airtable-like record fields; supports plain dicts too."""
    if not isinstance(record, Mapping):
        return {}
    if "fields" in record and isinstance(record["fields"], Mapping):
        return _safe_lower_keys(record["fields"])  # Airtable format
    return _safe_lower_keys(record)


def _select_record(
    records: Iterable[Mapping[str, Any]],
    company: Optional[str] = None,
    period: Optional[str] = None,
) -> Optional[Mapping[str, Any]]:
    """Select a single financial statement record.

    Preference order:
    1) Matches both company and period (if provided)
    2) Matches company only
    3) First record
    """
    records_list = list(records) if records is not None else []
    if not records_list:
        return None

    def matches(rec: Mapping[str, Any], key: str, value: str) -> bool:
        fields = _extract_fields(rec)
        return str(fields.get(key, "")).strip().lower() == value.strip().lower()

    if company and period:
        for rec in records_list:
            if matches(rec, "company", company) and matches(rec, "period", period):
                return rec

    if company:
        for rec in records_list:
            if matches(rec, "company", company):
                return rec

    return records_list[0]


def _get_number(fields: Mapping[str, Any], *keys: str, default: float = 0.0) -> float:
    for key in keys:
        if key in fields and isinstance(fields[key], (int, float)):
            return float(fields[key])
    return float(default)


# -------------------------------
# Tool 1: Book Value Calculator
# -------------------------------

def calculate_book_value(
    company: Optional[str] = None,
    period: Optional[str] = None,
    records: Optional[Iterable[Mapping[str, Any]]] = None,
    total_assets: Optional[float] = None,
    total_liabilities: Optional[float] = None,
) -> Dict[str, Any]:
    """Compute Book Value = Total Assets - Total Liabilities.

    Inputs can be provided directly (total_assets/total_liabilities),
    or inferred from financial statement records (Airtable or dict-like).
    
    Returns a structured payload suitable for agent consumption.
    """
    # Prefer explicit inputs if provided
    if total_assets is None or total_liabilities is None:
        records_source = records if records is not None else get_financial_statements()
        chosen = _select_record(records_source, company=company, period=period)
        if not chosen:
            return {
                "tool": "calculate_book_value",
                "company": company,
                "period": period,
                "success": False,
                "message": "No financial statement records available.",
            }

        fields = _extract_fields(chosen)
        total_assets = _get_number(fields, "total_assets", "assets") if total_assets is None else total_assets
        total_liabilities = _get_number(fields, "total_liabilities", "liabilities") if total_liabilities is None else total_liabilities

    book_value = float(total_assets) - float(total_liabilities)

    notes = []
    if book_value < 0:
        notes.append("Negative equity; liabilities exceed assets.")
    notes.append("Book value may undervalue intangibles and going-concern value.")

    # Heuristic confidence: higher when explicit inputs are provided
    confidence = 0.9 if (total_assets is not None and total_liabilities is not None and records is None) else 0.75

    return {
        "tool": "calculate_book_value",
        "company": company,
        "period": period,
        "success": True,
        "inputs": {
            "total_assets": float(total_assets),
            "total_liabilities": float(total_liabilities),
        },
        "result": {
            "book_value": book_value,
        },
        "confidence": confidence,
        "notes": "; ".join(notes),
    }


# -------------------------------------
# Tool 2: Liquidation Value Estimator
# -------------------------------------

DEFAULT_LIQUIDATION_DISCOUNTS: Dict[str, float] = {
    # Conservative defaults; can be overridden via discounts param
    "cash": 1.00,
    "cash_and_equivalents": 1.00,
    "marketable_securities": 0.95,
    "accounts_receivable": 0.70,
    "receivables": 0.70,
    "inventory": 0.50,
    "prepaid_expenses": 0.10,
    "pp&e": 0.40,
    "ppe": 0.40,
    "property_plant_equipment": 0.40,
    "intangibles": 0.10,
    "goodwill": 0.00,
    "other_assets": 0.30,
}


def estimate_liquidation_value(
    company: Optional[str] = None,
    period: Optional[str] = None,
    records: Optional[Iterable[Mapping[str, Any]]] = None,
    asset_breakdown: Optional[Mapping[str, float]] = None,
    total_liabilities: Optional[float] = None,
    discounts: Optional[Mapping[str, float]] = None,
) -> Dict[str, Any]:
    """Estimate liquidation value by discounting asset categories and subtracting liabilities.

    If `asset_breakdown` is not provided, this function attempts to infer asset categories
    from the selected financial statement record fields. If only `total_assets` is present
    without a breakdown, a blanket discount (0.70) is applied as a fallback.
    """
    discounts_map = _safe_lower_keys(discounts or DEFAULT_LIQUIDATION_DISCOUNTS)

    # Source data
    chosen_fields: Dict[str, Any] = {}
    if asset_breakdown is None or total_liabilities is None:
        records_source = records if records is not None else get_financial_statements()
        chosen = _select_record(records_source, company=company, period=period)
        if chosen:
            chosen_fields = _extract_fields(chosen)

    # Determine liabilities
    if total_liabilities is None:
        total_liabilities = _get_number(chosen_fields, "total_liabilities", "liabilities", default=0.0)

    # Determine asset breakdown
    inferred_breakdown: Dict[str, float] = {}
    if asset_breakdown is not None:
        inferred_breakdown = {str(k).lower(): float(v) for k, v in asset_breakdown.items()}
    else:
        # Try to infer common categories
        candidate_keys = set(discounts_map.keys()) | {
            "assets",
            "total_assets",
            "cash",
            "cash_and_equivalents",
            "marketable_securities",
            "accounts_receivable",
            "receivables",
            "inventory",
            "prepaid_expenses",
            "pp&e",
            "ppe",
            "property_plant_equipment",
            "intangibles",
            "goodwill",
            "other_assets",
        }
        total_assets_value = None
        for key in candidate_keys:
            if key in chosen_fields and isinstance(chosen_fields[key], (int, float)):
                value = float(chosen_fields[key])
                if key in ("assets", "total_assets"):
                    total_assets_value = value
                else:
                    inferred_breakdown[key] = value

        # If no breakdown found but total assets present, apply blanket discount as proxy
        if not inferred_breakdown and total_assets_value is not None:
            inferred_breakdown = {"total_assets": total_assets_value}
            # Use a conservative blanket discount for forced sale
            if "total_assets" not in discounts_map:
                discounts_map["total_assets"] = 0.70

    # Compute discounted asset value
    discounted_total = 0.0
    applied_discounts: Dict[str, float] = {}
    for category, value in inferred_breakdown.items():
        category_key = str(category).lower()
        discount = float(discounts_map.get(category_key, 0.50))  # default mid-range discount
        applied_discounts[category_key] = discount
        discounted_total += float(value) * discount

    liquidation_value = discounted_total - float(total_liabilities or 0.0)

    # Confidence heuristics
    has_breakdown = len(inferred_breakdown) > 1 or (len(inferred_breakdown) == 1 and "total_assets" not in inferred_breakdown)
    confidence = 0.85 if has_breakdown else 0.65

    notes = []
    if not has_breakdown:
        notes.append("Used blanket discount due to missing asset breakdown.")
    notes.append("Liquidation discounts approximate forced-sale conditions and vary by sector.")

    return {
        "tool": "estimate_liquidation_value",
        "company": company,
        "period": period,
        "success": True,
        "inputs": {
            "asset_breakdown": inferred_breakdown,
            "total_liabilities": float(total_liabilities or 0.0),
            "discounts": applied_discounts or discounts_map,
        },
        "result": {
            "discounted_asset_value": discounted_total,
            "liquidation_value": liquidation_value,
        },
        "confidence": confidence,
        "notes": "; ".join(notes),
    }


# -------------------------------
# MARKET-BASED VALUATION TOOLS
# -------------------------------

def calculate_market_cap(
    company: Optional[str] = None,
    period: Optional[str] = None,
    records: Optional[Iterable[Mapping[str, Any]]] = None,
    share_price: Optional[float] = None,
    shares_outstanding: Optional[float] = None,
) -> Dict[str, Any]:
    """Calculate Market Capitalization = Share Price × Shares Outstanding.
    
    For public companies, this provides a direct market-based valuation.
    """
    # Prefer explicit inputs if provided
    if share_price is None or shares_outstanding is None:
        records_source = records if records is not None else get_financial_statements()
        chosen = _select_record(records_source, company=company, period=period)
        if not chosen:
            return {
                "tool": "calculate_market_cap",
                "company": company,
                "period": period,
                "success": False,
                "message": "No financial statement records available.",
            }

        fields = _extract_fields(chosen)
        share_price = _get_number(fields, "share_price", "price") if share_price is None else share_price
        shares_outstanding = _get_number(fields, "shares_outstanding", "shares") if shares_outstanding is None else shares_outstanding

    if share_price is None or shares_outstanding is None or share_price <= 0 or shares_outstanding <= 0:
        return {
            "tool": "calculate_market_cap",
            "company": company,
            "period": period,
            "success": False,
            "message": "Invalid share price or shares outstanding data.",
        }

    market_cap = float(share_price) * float(shares_outstanding)

    notes = []
    if market_cap <= 0:
        notes.append("Invalid market cap calculation.")
    notes.append("Market cap reflects current market sentiment and may be volatile.")

    confidence = 0.9 if (share_price is not None and shares_outstanding is not None and records is None) else 0.75

    return {
        "tool": "calculate_market_cap",
        "company": company,
        "period": period,
        "success": True,
        "inputs": {
            "share_price": float(share_price),
            "shares_outstanding": float(shares_outstanding),
        },
        "result": {
            "market_cap": market_cap,
        },
        "confidence": confidence,
        "notes": "; ".join(notes),
    }


def calculate_comparable_multiples(
    company: Optional[str] = None,
    period: Optional[str] = None,
    records: Optional[Iterable[Mapping[str, Any]]] = None,
    revenue: Optional[float] = None,
    ebitda: Optional[float] = None,
    net_income: Optional[float] = None,
    ev_ebitda_multiple: Optional[float] = None,
    pe_multiple: Optional[float] = None,
    ev_sales_multiple: Optional[float] = None,
    industry_multiples: Optional[Mapping[str, float]] = None,
) -> Dict[str, Any]:
    """Calculate company value using comparable industry multiples.
    
    Supports EV/EBITDA, P/E, and EV/Sales multiples.
    """
    # Prefer explicit inputs if provided
    if any(x is None for x in [revenue, ebitda, net_income]):
        records_source = records if records is not None else get_financial_statements()
        chosen = _select_record(records_source, company=company, period=period)
        if not chosen:
            return {
                "tool": "calculate_comparable_multiples",
                "company": company,
                "period": period,
                "success": False,
                "message": "No financial statement records available.",
            }

        fields = _extract_fields(chosen)
        revenue = _get_number(fields, "revenue", "total_revenue") if revenue is None else revenue
        ebitda = _get_number(fields, "ebitda", "operating_income") if ebitda is None else ebitda
        net_income = _get_number(fields, "net_income", "net_profit") if net_income is None else net_income

    # Get industry multiples if not provided
    if industry_multiples is None:
        try:
            multiples_records = get_industry_multiples()
            if multiples_records:
                # Use first available industry multiple record
                multiples_fields = _extract_fields(multiples_records[0])
                industry_multiples = {
                    "ev_ebitda": _get_number(multiples_fields, "ev_ebitda", "ev_ebitda_multiple", default=8.0),
                    "pe": _get_number(multiples_fields, "pe", "pe_multiple", default=15.0),
                    "ev_sales": _get_number(multiples_fields, "ev_sales", "ev_sales_multiple", default=2.0),
                }
            else:
                # Default industry multiples
                industry_multiples = {
                    "ev_ebitda": 8.0,
                    "pe": 15.0,
                    "ev_sales": 2.0,
                }
        except Exception:
            industry_multiples = {
                "ev_ebitda": 8.0,
                "pe": 15.0,
                "ev_sales": 2.0,
            }

    # Override with explicit multiples if provided
    if ev_ebitda_multiple is not None:
        industry_multiples["ev_ebitda"] = ev_ebitda_multiple
    if pe_multiple is not None:
        industry_multiples["pe"] = pe_multiple
    if ev_sales_multiple is not None:
        industry_multiples["ev_sales"] = ev_sales_multiple

    # Calculate valuations
    valuations = {}
    
    if ebitda and ebitda > 0 and industry_multiples.get("ev_ebitda"):
        valuations["ev_ebitda"] = float(ebitda) * industry_multiples["ev_ebitda"]
    
    if net_income and net_income > 0 and industry_multiples.get("pe"):
        valuations["pe"] = float(net_income) * industry_multiples["pe"]
    
    if revenue and revenue > 0 and industry_multiples.get("ev_sales"):
        valuations["ev_sales"] = float(revenue) * industry_multiples["ev_sales"]

    if not valuations:
        return {
            "tool": "calculate_comparable_multiples",
            "company": company,
            "period": period,
            "success": False,
            "message": "Insufficient data for multiple calculations.",
        }

    # Calculate average valuation
    avg_valuation = sum(valuations.values()) / len(valuations)

    notes = []
    if len(valuations) < 3:
        notes.append(f"Only {len(valuations)} multiple(s) calculated due to missing data.")
    notes.append("Multiples should be adjusted for company-specific risk factors.")

    confidence = 0.8 if len(valuations) >= 2 else 0.6

    return {
        "tool": "calculate_comparable_multiples",
        "company": company,
        "period": period,
        "success": True,
        "inputs": {
            "revenue": float(revenue or 0),
            "ebitda": float(ebitda or 0),
            "net_income": float(net_income or 0),
            "industry_multiples": industry_multiples,
        },
        "result": {
            "valuations": valuations,
            "average_valuation": avg_valuation,
        },
        "confidence": confidence,
        "notes": "; ".join(notes),
    }


# -------------------------------
# EARNING-BASED VALUATION TOOLS
# -------------------------------

def calculate_dcf(
    company: Optional[str] = None,
    period: Optional[str] = None,
    records: Optional[Iterable[Mapping[str, Any]]] = None,
    free_cash_flows: Optional[list[float]] = None,
    wacc: Optional[float] = None,
    terminal_growth_rate: Optional[float] = None,
    forecast_years: int = 5,
) -> Dict[str, Any]:
    """Calculate Discounted Cash Flow (DCF) valuation.
    
    DCF = Σ(FCF_t / (1+WACC)^t) + TV / (1+WACC)^n
    TV = FCF_n × (1+g) / (WACC - g)
    """
    # Prefer explicit inputs if provided
    if free_cash_flows is None or wacc is None:
        records_source = records if records is not None else get_financial_statements()
        chosen = _select_record(records_source, company=company, period=period)
        if not chosen:
            return {
                "tool": "calculate_dcf",
                "company": company,
                "period": period,
                "success": False,
                "message": "No financial statement records available.",
            }

        fields = _extract_fields(chosen)
        if free_cash_flows is None:
            # Try to extract FCF or calculate from available data
            fcf = _get_number(fields, "free_cash_flow", "fcf")
            if fcf == 0:
                # Calculate FCF = Operating Cash Flow - CapEx
                ocf = _get_number(fields, "operating_cash_flow", "ocf")
                capex = _get_number(fields, "capital_expenditures", "capex")
                fcf = ocf - capex
            if fcf != 0:
                # Project FCF for forecast years with simple growth assumption
                growth = 0.05  # 5% default growth
                free_cash_flows = [fcf * (1 + growth) ** i for i in range(forecast_years)]
            else:
                free_cash_flows = [0] * forecast_years

        if wacc is None:
            wacc = _get_number(fields, "wacc", "discount_rate", default=0.10)

    if terminal_growth_rate is None:
        terminal_growth_rate = 0.03  # 3% default terminal growth

    if not free_cash_flows or len(free_cash_flows) == 0:
        return {
            "tool": "calculate_dcf",
            "company": company,
            "period": period,
            "success": False,
            "message": "No free cash flow data available.",
        }

    # Ensure we have the right number of years
    if len(free_cash_flows) < forecast_years:
        # Extend with last year's growth
        last_fcf = free_cash_flows[-1] if free_cash_flows else 0
        growth = 0.05  # 5% default growth
        while len(free_cash_flows) < forecast_years:
            free_cash_flows.append(last_fcf * (1 + growth))
            last_fcf = free_cash_flows[-1]

    # Calculate present value of cash flows
    pv_cash_flows = []
    for i, fcf in enumerate(free_cash_flows[:forecast_years]):
        pv = float(fcf) / ((1 + float(wacc)) ** (i + 1))
        pv_cash_flows.append(pv)

    # Calculate terminal value
    final_fcf = free_cash_flows[forecast_years - 1]
    terminal_value = (final_fcf * (1 + float(terminal_growth_rate))) / (float(wacc) - float(terminal_growth_rate))
    pv_terminal_value = terminal_value / ((1 + float(wacc)) ** forecast_years)

    # Calculate DCF value
    dcf_value = sum(pv_cash_flows) + pv_terminal_value

    notes = []
    if wacc <= terminal_growth_rate:
        notes.append("WACC should be greater than terminal growth rate for valid DCF.")
    notes.append("DCF is sensitive to growth and discount rate assumptions.")

    confidence = 0.8 if wacc > terminal_growth_rate else 0.4

    return {
        "tool": "calculate_dcf",
        "company": company,
        "period": period,
        "success": True,
        "inputs": {
            "free_cash_flows": [float(fcf) for fcf in free_cash_flows[:forecast_years]],
            "wacc": float(wacc),
            "terminal_growth_rate": float(terminal_growth_rate),
            "forecast_years": forecast_years,
        },
        "result": {
            "dcf_value": dcf_value,
            "terminal_value": terminal_value,
            "pv_cash_flows": sum(pv_cash_flows),
            "pv_terminal_value": pv_terminal_value,
        },
        "confidence": confidence,
        "notes": "; ".join(notes),
    }


def calculate_earnings_multiple(
    company: Optional[str] = None,
    period: Optional[str] = None,
    records: Optional[Iterable[Mapping[str, Any]]] = None,
    ebitda: Optional[float] = None,
    revenue: Optional[float] = None,
    ebitda_multiple: Optional[float] = None,
    revenue_multiple: Optional[float] = None,
    industry_multiples: Optional[Mapping[str, float]] = None,
) -> Dict[str, Any]:
    """Calculate company value using earnings and revenue multiples.
    
    Supports EBITDA and Revenue multiples.
    """
    # Prefer explicit inputs if provided
    if ebitda is None or revenue is None:
        records_source = records if records is not None else get_financial_statements()
        chosen = _select_record(records_source, company=company, period=period)
        if not chosen:
            return {
                "tool": "calculate_earnings_multiple",
                "company": company,
                "period": period,
                "success": False,
                "message": "No financial statement records available.",
            }

        fields = _extract_fields(chosen)
        ebitda = _get_number(fields, "ebitda", "operating_income") if ebitda is None else ebitda
        revenue = _get_number(fields, "revenue", "total_revenue") if revenue is None else revenue

    # Get industry multiples if not provided
    if industry_multiples is None:
        try:
            multiples_records = get_industry_multiples()
            if multiples_records:
                multiples_fields = _extract_fields(multiples_records[0])
                industry_multiples = {
                    "ebitda": _get_number(multiples_fields, "ebitda_multiple", "ev_ebitda", default=8.0),
                    "revenue": _get_number(multiples_fields, "revenue_multiple", "ev_sales", default=2.0),
                }
            else:
                industry_multiples = {
                    "ebitda": 8.0,
                    "revenue": 2.0,
                }
        except Exception:
            industry_multiples = {
                "ebitda": 8.0,
                "revenue": 2.0,
            }

    # Override with explicit multiples if provided
    if ebitda_multiple is not None:
        industry_multiples["ebitda"] = ebitda_multiple
    if revenue_multiple is not None:
        industry_multiples["revenue"] = revenue_multiple

    # Calculate valuations
    valuations = {}
    
    if ebitda and ebitda > 0 and industry_multiples.get("ebitda"):
        valuations["ebitda"] = float(ebitda) * industry_multiples["ebitda"]
    
    if revenue and revenue > 0 and industry_multiples.get("revenue"):
        valuations["revenue"] = float(revenue) * industry_multiples["revenue"]

    if not valuations:
        return {
            "tool": "calculate_earnings_multiple",
            "company": company,
            "period": period,
            "success": False,
            "message": "Insufficient data for multiple calculations.",
        }

    # Calculate average valuation
    avg_valuation = sum(valuations.values()) / len(valuations)

    notes = []
    if len(valuations) < 2:
        notes.append(f"Only {len(valuations)} multiple(s) calculated due to missing data.")
    notes.append("Multiples should be adjusted for company-specific factors and growth prospects.")

    confidence = 0.8 if len(valuations) >= 2 else 0.6

    return {
        "tool": "calculate_earnings_multiple",
        "company": company,
        "period": period,
        "success": True,
        "inputs": {
            "ebitda": float(ebitda or 0),
            "revenue": float(revenue or 0),
            "industry_multiples": industry_multiples,
        },
        "result": {
            "valuations": valuations,
            "average_valuation": avg_valuation,
        },
        "confidence": confidence,
        "notes": "; ".join(notes),
    }

