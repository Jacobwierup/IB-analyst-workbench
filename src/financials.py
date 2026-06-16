from pathlib import Path
import pandas as pd
import yaml


def load_company_data(company_dir: str | Path) -> dict:
    company_dir = Path(company_dir)

    income_statement = pd.read_csv(company_dir / "income_statement.csv")
    balance_sheet = pd.read_csv(company_dir / "balance_sheet.csv")
    cash_flow = pd.read_csv(company_dir / "cash_flow.csv")
    market_data = pd.read_csv(company_dir / "market_data.csv")

    with open(company_dir / "assumptions.yaml", "r") as f:
        assumptions = yaml.safe_load(f)

    return {
        "income_statement": income_statement,
        "balance_sheet": balance_sheet,
        "cash_flow": cash_flow,
        "market_data": market_data,
        "assumptions": assumptions,
    }


def build_historical_model(data: dict) -> pd.DataFrame:
    income = data["income_statement"]
    balance = data["balance_sheet"]
    cash_flow = data["cash_flow"]
    market = data["market_data"].iloc[0]

    df = income.merge(balance, on="year").merge(cash_flow, on="year")
    df = df.sort_values("year").reset_index(drop=True)

    df["revenue_growth"] = df["revenue"].pct_change()
    df["ebitda_margin"] = df["ebitda"] / df["revenue"]
    df["ebit_margin"] = df["ebit"] / df["revenue"]
    df["net_income_margin"] = df["net_income"] / df["revenue"]

    df["net_debt"] = df["total_debt"] + df["lease_liabilities"] - df["cash"]
    df["market_cap"] = float(market["share_price"]) * df["shares_outstanding"] / 1_000_000
    df["enterprise_value"] = (
        df["market_cap"]
        + df["total_debt"]
        + df["lease_liabilities"]
        + df["minority_interest"]
        + df["preferred_equity"]
        - df["cash"]
    )

    df["ev_revenue"] = df["enterprise_value"] / df["revenue"]
    df["ev_ebitda"] = df["enterprise_value"] / df["ebitda"]
    df["ev_ebit"] = df["enterprise_value"] / df["ebit"]
    df["pe"] = df["market_cap"] / df["net_income"]
    df["net_debt_ebitda"] = df["net_debt"] / df["ebitda"]

    df["capex_pct_revenue"] = df["capex"] / df["revenue"]
    df["da_pct_revenue"] = df["depreciation_amortization"] / df["revenue"]

    return df


def format_model_for_output(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()

    pct_cols = [
        "revenue_growth",
        "ebitda_margin",
        "ebit_margin",
        "net_income_margin",
        "capex_pct_revenue",
        "da_pct_revenue",
    ]

    multiple_cols = [
        "ev_revenue",
        "ev_ebitda",
        "ev_ebit",
        "pe",
        "net_debt_ebitda",
    ]

    for col in pct_cols:
        output[col] = output[col].apply(lambda x: "" if pd.isna(x) else f"{x:.1%}")

    for col in multiple_cols:
        output[col] = output[col].apply(lambda x: "" if pd.isna(x) else f"{x:.1f}x")

    return output
