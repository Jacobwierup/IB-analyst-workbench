from __future__ import annotations

from pathlib import Path
import pandas as pd


def _fmt_money(value: float) -> str:
    return f"{value:,.0f}"


def _fmt_price(value: float) -> str:
    return f"{value:,.2f}"


def _fmt_pct(value: float) -> str:
    return f"{value:.1%}"


def generate_investment_memo(
    company_name: str,
    ticker: str,
    currency: str,
    historical_model: pd.DataFrame,
    dcf_summary: pd.DataFrame,
    wacc_terminal_growth: pd.DataFrame,
    revenue_margin: pd.DataFrame,
) -> str:
    latest = historical_model.sort_values("year").iloc[-1]

    base = dcf_summary[dcf_summary["case"] == "Base"].iloc[0]
    bear = dcf_summary[dcf_summary["case"] == "Bear"].iloc[0]
    bull = dcf_summary[dcf_summary["case"] == "Bull"].iloc[0]

    latest_year = int(latest["year"])
    latest_revenue = float(latest["revenue"])
    latest_ebitda_margin = float(latest["ebitda_margin"])
    latest_ebit_margin = float(latest["ebit_margin"])
    latest_net_debt = float(latest["net_debt"])
    latest_ev_revenue = float(latest["ev_revenue"])
    latest_ev_ebitda = float(latest["ev_ebitda"])
    latest_pe = float(latest["pe"])
    latest_net_debt_ebitda = float(latest["net_debt_ebitda"])

    memo = f"""# Investment Committee Memo

## Company

**{company_name}**  
Ticker: **{ticker}**  
Currency: **{currency}**  
Model date: generated locally from structured company financials

## Executive Summary

This memo presents an institutional-style valuation overview for {company_name}. The current model includes a historical financial model, enterprise value bridge, valuation multiples, DCF valuation, bull/base/bear scenario analysis, and sensitivity tables.

The base case DCF implies an equity value of **{_fmt_money(float(base["equity_value"]))} {currency}m**, corresponding to an implied share price of **{_fmt_price(float(base["implied_share_price"]))} {currency}**. The scenario range spans **{_fmt_price(float(bear["implied_share_price"]))} {currency}** in the bear case to **{_fmt_price(float(bull["implied_share_price"]))} {currency}** in the bull case.

Important note: the current financials are placeholder inputs used to validate the model architecture. Before using the model for real analysis, the input files should be replaced with reported figures from annual reports, interim reports, company filings, and market data sources.

## Historical Financial Performance

For fiscal year {latest_year}, the model shows:

| Metric | Value |
|---|---:|
| Revenue | {_fmt_money(latest_revenue)} {currency}m |
| EBITDA margin | {_fmt_pct(latest_ebitda_margin)} |
| EBIT margin | {_fmt_pct(latest_ebit_margin)} |
| Net debt | {_fmt_money(latest_net_debt)} {currency}m |
| EV / Revenue | {latest_ev_revenue:.1f}x |
| EV / EBITDA | {latest_ev_ebitda:.1f}x |
| P / E | {latest_pe:.1f}x |
| Net debt / EBITDA | {latest_net_debt_ebitda:.1f}x |

The model indicates improving revenue growth and margin expansion across the historical period. This supports a valuation framework where future revenue growth, EBIT margin sustainability, capital intensity, and working capital requirements are key value drivers.

## Valuation Summary

| Case | Enterprise Value | Equity Value | Implied Share Price |
|---|---:|---:|---:|
| Bear | {_fmt_money(float(bear["enterprise_value"]))} {currency}m | {_fmt_money(float(bear["equity_value"]))} {currency}m | {_fmt_price(float(bear["implied_share_price"]))} {currency} |
| Base | {_fmt_money(float(base["enterprise_value"]))} {currency}m | {_fmt_money(float(base["equity_value"]))} {currency}m | {_fmt_price(float(base["implied_share_price"]))} {currency} |
| Bull | {_fmt_money(float(bull["enterprise_value"]))} {currency}m | {_fmt_money(float(bull["equity_value"]))} {currency}m | {_fmt_price(float(bull["implied_share_price"]))} {currency} |

The DCF valuation is driven primarily by long-term free cash flow generation and terminal value assumptions. As in most DCF models, the output is highly sensitive to WACC, terminal growth, revenue growth, and EBIT margin assumptions.

## Key Value Drivers

1. **Revenue growth:** Higher order intake, structural demand, pricing, and market expansion support higher forecast revenue.
2. **EBIT margin:** Margin expansion has a direct impact on NOPAT and free cash flow.
3. **Capital intensity:** Higher capex reduces free cash flow, especially during high-growth periods.
4. **Working capital:** Growth can consume cash if receivables, inventories, or contract assets increase.
5. **Discount rate:** A higher WACC reduces present value and valuation range.
6. **Terminal value:** Long-term assumptions have a material impact on total enterprise value.

## Scenario Interpretation

### Bear Case

The bear case assumes lower revenue growth, pressure on EBIT margins, higher capital intensity, and less attractive free cash flow conversion. This case is useful for evaluating downside risk if growth expectations weaken or execution becomes more difficult.

### Base Case

The base case assumes continued growth with gradually stabilizing margins and capital intensity. This represents the central valuation case in the current model.

### Bull Case

The bull case assumes stronger growth, margin expansion, and better free cash flow conversion. This case reflects a scenario where the company benefits from strong demand, operational leverage, and disciplined reinvestment.

## Sensitivity Analysis

The WACC versus terminal growth sensitivity table shows that the implied share price is materially affected by relatively small changes in long-term assumptions. This is typical for DCF-based valuation work.

The revenue growth versus EBIT margin sensitivity table highlights the importance of operational performance. A company can justify a higher valuation if it combines above-peer growth with durable or expanding margins.

## Investment Committee Style Conclusion

Based on the selected assumptions, the model generates a base case implied share price of **{_fmt_price(float(base["implied_share_price"]))} {currency}**, with a scenario range of **{_fmt_price(float(bear["implied_share_price"]))} {currency}** to **{_fmt_price(float(bull["implied_share_price"]))} {currency}**.

The valuation is most sensitive to WACC, terminal growth, revenue growth, and EBIT margin. Before drawing any investment conclusion, the model should be updated with verified reported financials, a defensible peer group, actual trading multiples, management guidance, and sector-specific assumptions.

## Model Outputs

Generated outputs include:

- Historical company model
- DCF forecasts for bear, base, and bull cases
- DCF valuation summary
- WACC versus terminal growth sensitivity
- Revenue growth versus EBIT margin sensitivity
- Excel valuation workbook

## Disclaimer

This project is for educational and portfolio purposes only. It is not investment advice, financial advice, or a recommendation to buy or sell securities.
"""
    return memo


def write_memo(output_path: str | Path, memo: str) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(memo, encoding="utf-8")
