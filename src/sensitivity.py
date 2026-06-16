from __future__ import annotations

import pandas as pd

from src.dcf import build_dcf_case


def build_wacc_terminal_growth_sensitivity(
    historical_model: pd.DataFrame,
    assumptions: dict,
    case_name: str = "base_case",
    wacc_values: list[float] | None = None,
    terminal_growth_values: list[float] | None = None,
) -> pd.DataFrame:
    if wacc_values is None:
        wacc_values = [0.075, 0.080, 0.085, 0.090, 0.095]

    if terminal_growth_values is None:
        terminal_growth_values = [0.015, 0.020, 0.025, 0.030, 0.035]

    rows = []

    for terminal_growth in terminal_growth_values:
        row = {"terminal_growth": terminal_growth}

        for wacc in wacc_values:
            temp_assumptions = assumptions.copy()
            temp_assumptions["wacc"] = wacc
            temp_assumptions["terminal_growth"] = terminal_growth

            result = build_dcf_case(
                historical_model=historical_model,
                assumptions=temp_assumptions,
                case_name=case_name,
            )

            row[f"wacc_{wacc:.1%}"] = result.implied_share_price

        rows.append(row)

    return pd.DataFrame(rows)


def build_revenue_margin_sensitivity(
    historical_model: pd.DataFrame,
    assumptions: dict,
    case_name: str = "base_case",
    revenue_growth_adjustments: list[float] | None = None,
    ebit_margin_adjustments: list[float] | None = None,
) -> pd.DataFrame:
    if revenue_growth_adjustments is None:
        revenue_growth_adjustments = [-0.03, -0.015, 0.00, 0.015, 0.03]

    if ebit_margin_adjustments is None:
        ebit_margin_adjustments = [-0.015, -0.0075, 0.00, 0.0075, 0.015]

    rows = []

    for margin_adj in ebit_margin_adjustments:
        row = {"ebit_margin_adjustment": margin_adj}

        for growth_adj in revenue_growth_adjustments:
            temp_assumptions = assumptions.copy()
            temp_case = assumptions[case_name].copy()

            temp_case["revenue_growth"] = [
                max(0.0, x + growth_adj) for x in assumptions[case_name]["revenue_growth"]
            ]
            temp_case["ebit_margin"] = [
                max(0.0, x + margin_adj) for x in assumptions[case_name]["ebit_margin"]
            ]

            temp_assumptions[case_name] = temp_case

            result = build_dcf_case(
                historical_model=historical_model,
                assumptions=temp_assumptions,
                case_name=case_name,
            )

            row[f"growth_adj_{growth_adj:.1%}"] = result.implied_share_price

        rows.append(row)

    return pd.DataFrame(rows)


def format_sensitivity_table(df: pd.DataFrame, label_col: str) -> pd.DataFrame:
    output = df.copy()

    output[label_col] = output[label_col].apply(lambda x: f"{x:.1%}")

    for col in output.columns:
        if col != label_col:
            output[col] = output[col].apply(lambda x: f"{x:,.2f}")

    return output
