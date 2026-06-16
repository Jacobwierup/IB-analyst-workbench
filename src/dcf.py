from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass
class DCFResult:
    case_name: str
    forecast: pd.DataFrame
    enterprise_value: float
    equity_value: float
    implied_share_price: float
    terminal_value: float
    pv_terminal_value: float
    pv_fcf: float


def build_dcf_case(
    historical_model: pd.DataFrame,
    assumptions: dict,
    case_name: str,
) -> DCFResult:
    case = assumptions[case_name]
    forecast_years = assumptions["forecast_years"]

    wacc = float(assumptions["wacc"])
    terminal_growth = float(assumptions["terminal_growth"])
    tax_rate = float(assumptions["tax_rate"])

    last_year = historical_model.sort_values("year").iloc[-1]
    latest_revenue = float(last_year["revenue"])
    net_debt = float(last_year["net_debt"])
    shares_outstanding = float(last_year["shares_outstanding"])

    rows = []
    prior_revenue = latest_revenue

    for idx, year in enumerate(forecast_years):
        revenue_growth = float(case["revenue_growth"][idx])
        ebit_margin = float(case["ebit_margin"][idx])
        da_pct_revenue = float(case["depreciation_amortization_pct_revenue"][idx])
        capex_pct_revenue = float(case["capex_pct_revenue"][idx])
        nwc_pct_revenue_change = float(case["nwc_pct_revenue_change"][idx])

        revenue = prior_revenue * (1 + revenue_growth)
        ebit = revenue * ebit_margin
        tax_on_ebit = ebit * tax_rate
        nopat = ebit - tax_on_ebit
        depreciation_amortization = revenue * da_pct_revenue
        capex = revenue * capex_pct_revenue
        change_nwc = (revenue - prior_revenue) * nwc_pct_revenue_change

        unlevered_fcf = nopat + depreciation_amortization - capex - change_nwc
        discount_factor = 1 / ((1 + wacc) ** (idx + 1))
        pv_fcf = unlevered_fcf * discount_factor

        rows.append(
            {
                "year": year,
                "revenue": revenue,
                "revenue_growth": revenue_growth,
                "ebit_margin": ebit_margin,
                "ebit": ebit,
                "tax_on_ebit": tax_on_ebit,
                "nopat": nopat,
                "depreciation_amortization": depreciation_amortization,
                "capex": capex,
                "change_nwc": change_nwc,
                "unlevered_fcf": unlevered_fcf,
                "discount_factor": discount_factor,
                "pv_fcf": pv_fcf,
            }
        )

        prior_revenue = revenue

    forecast = pd.DataFrame(rows)

    final_fcf = float(forecast.iloc[-1]["unlevered_fcf"])
    terminal_value = final_fcf * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / ((1 + wacc) ** len(forecast_years))

    pv_fcf_total = float(forecast["pv_fcf"].sum())
    enterprise_value = pv_fcf_total + pv_terminal_value
    equity_value = enterprise_value - net_debt
    implied_share_price = equity_value * 1_000_000 / shares_outstanding

    return DCFResult(
        case_name=case_name,
        forecast=forecast,
        enterprise_value=enterprise_value,
        equity_value=equity_value,
        implied_share_price=implied_share_price,
        terminal_value=terminal_value,
        pv_terminal_value=pv_terminal_value,
        pv_fcf=pv_fcf_total,
    )


def build_all_dcf_cases(historical_model: pd.DataFrame, assumptions: dict) -> tuple[pd.DataFrame, dict[str, DCFResult]]:
    results = {}

    for case_name in ["bear_case", "base_case", "bull_case"]:
        results[case_name] = build_dcf_case(historical_model, assumptions, case_name)

    summary_rows = []

    for case_name, result in results.items():
        summary_rows.append(
            {
                "case": case_name.replace("_case", "").title(),
                "enterprise_value": result.enterprise_value,
                "equity_value": result.equity_value,
                "implied_share_price": result.implied_share_price,
                "pv_fcf": result.pv_fcf,
                "pv_terminal_value": result.pv_terminal_value,
                "terminal_value": result.terminal_value,
            }
        )

    return pd.DataFrame(summary_rows), results


def format_dcf_summary(summary: pd.DataFrame) -> pd.DataFrame:
    output = summary.copy()

    value_cols = [
        "enterprise_value",
        "equity_value",
        "pv_fcf",
        "pv_terminal_value",
        "terminal_value",
    ]

    for col in value_cols:
        output[col] = output[col].apply(lambda x: f"{x:,.0f}")

    output["implied_share_price"] = output["implied_share_price"].apply(lambda x: f"{x:,.2f}")

    return output
