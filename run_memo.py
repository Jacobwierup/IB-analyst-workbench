from pathlib import Path

from src.financials import load_company_data, build_historical_model
from src.dcf import build_all_dcf_cases
from src.sensitivity import (
    build_wacc_terminal_growth_sensitivity,
    build_revenue_margin_sensitivity,
)
from src.memo import generate_investment_memo, write_memo


def main():
    company_dir = Path("data/companies/SAAB_B")
    output_dir = Path("outputs/SAAB_B")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_company_data(company_dir)
    assumptions = data["assumptions"]

    historical_model = build_historical_model(data)

    dcf_summary, _ = build_all_dcf_cases(
        historical_model=historical_model,
        assumptions=assumptions,
    )

    wacc_tg = build_wacc_terminal_growth_sensitivity(
        historical_model=historical_model,
        assumptions=assumptions,
        case_name="base_case",
    )

    rev_margin = build_revenue_margin_sensitivity(
        historical_model=historical_model,
        assumptions=assumptions,
        case_name="base_case",
    )

    memo = generate_investment_memo(
        company_name=assumptions["company_name"],
        ticker=assumptions["ticker"],
        currency=assumptions["currency"],
        historical_model=historical_model,
        dcf_summary=dcf_summary,
        wacc_terminal_growth=wacc_tg,
        revenue_margin=rev_margin,
    )

    output_path = output_dir / "investment_committee_memo.md"
    write_memo(output_path, memo)

    print(f"\nInvestment committee memo created: {output_path}\n")
    print(memo[:1500])
    print("\n... memo continues in the output file ...")


if __name__ == "__main__":
    main()
