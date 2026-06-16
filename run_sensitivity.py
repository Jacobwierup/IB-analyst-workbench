from pathlib import Path

from src.financials import load_company_data, build_historical_model
from src.sensitivity import (
    build_wacc_terminal_growth_sensitivity,
    build_revenue_margin_sensitivity,
    format_sensitivity_table,
)


def main():
    company_dir = Path("data/companies/SAAB_B")
    output_dir = Path("outputs/SAAB_B")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_company_data(company_dir)
    historical_model = build_historical_model(data)

    wacc_tg = build_wacc_terminal_growth_sensitivity(
        historical_model=historical_model,
        assumptions=data["assumptions"],
        case_name="base_case",
    )

    rev_margin = build_revenue_margin_sensitivity(
        historical_model=historical_model,
        assumptions=data["assumptions"],
        case_name="base_case",
    )

    wacc_tg.to_csv(output_dir / "sensitivity_wacc_terminal_growth_raw.csv", index=False)
    rev_margin.to_csv(output_dir / "sensitivity_revenue_margin_raw.csv", index=False)

    format_sensitivity_table(wacc_tg, "terminal_growth").to_csv(
        output_dir / "sensitivity_wacc_terminal_growth_formatted.csv",
        index=False,
    )

    format_sensitivity_table(rev_margin, "ebit_margin_adjustment").to_csv(
        output_dir / "sensitivity_revenue_margin_formatted.csv",
        index=False,
    )

    print("\nWACC vs Terminal Growth Sensitivity, implied share price\n")
    print(format_sensitivity_table(wacc_tg, "terminal_growth").to_string(index=False))

    print("\nRevenue Growth vs EBIT Margin Sensitivity, implied share price\n")
    print(format_sensitivity_table(rev_margin, "ebit_margin_adjustment").to_string(index=False))

    print("\nSaved sensitivity outputs to outputs/SAAB_B/")


if __name__ == "__main__":
    main()
