from pathlib import Path

from src.financials import load_company_data, build_historical_model
from src.dcf import build_all_dcf_cases
from src.sensitivity import (
    build_wacc_terminal_growth_sensitivity,
    build_revenue_margin_sensitivity,
)
from src.excel_export import write_model_workbook


def main():
    company_dir = Path("data/companies/SAAB_B")
    output_dir = Path("outputs/SAAB_B")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_company_data(company_dir)
    historical_model = build_historical_model(data)

    dcf_summary, dcf_results = build_all_dcf_cases(
        historical_model=historical_model,
        assumptions=data["assumptions"],
    )

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

    output_path = output_dir / "saab_valuation_model.xlsx"

    write_model_workbook(
        output_path=output_path,
        historical_model=historical_model,
        dcf_summary=dcf_summary,
        dcf_results=dcf_results,
        wacc_terminal_growth=wacc_tg,
        revenue_margin=rev_margin,
    )

    print(f"\nExcel valuation model created: {output_path}\n")


if __name__ == "__main__":
    main()
