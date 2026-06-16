from pathlib import Path

from src.financials import load_company_data, build_historical_model, format_model_for_output
from src.dcf import build_all_dcf_cases, format_dcf_summary
from src.sensitivity import (
    build_wacc_terminal_growth_sensitivity,
    build_revenue_margin_sensitivity,
    format_sensitivity_table,
)
from src.excel_export import write_model_workbook
from src.memo import generate_investment_memo, write_memo


def main():
    company_dir = Path("data/companies/SAAB_B")
    output_dir = Path("outputs/SAAB_B")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_company_data(company_dir)
    assumptions = data["assumptions"]

    historical_model = build_historical_model(data)
    historical_model.to_csv(output_dir / "historical_model_raw.csv", index=False)
    format_model_for_output(historical_model).to_csv(
        output_dir / "historical_model_formatted.csv",
        index=False,
    )

    dcf_summary, dcf_results = build_all_dcf_cases(
        historical_model=historical_model,
        assumptions=assumptions,
    )

    dcf_summary.to_csv(output_dir / "dcf_summary_raw.csv", index=False)
    format_dcf_summary(dcf_summary).to_csv(
        output_dir / "dcf_summary_formatted.csv",
        index=False,
    )

    for case_name, result in dcf_results.items():
        result.forecast.to_csv(output_dir / f"dcf_forecast_{case_name}.csv", index=False)

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

    write_model_workbook(
        output_path=output_dir / "saab_valuation_model.xlsx",
        historical_model=historical_model,
        dcf_summary=dcf_summary,
        dcf_results=dcf_results,
        wacc_terminal_growth=wacc_tg,
        revenue_margin=rev_margin,
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

    write_memo(output_dir / "investment_committee_memo.md", memo)

    print("\nFull valuation model completed.\n")
    print(f"Company: {assumptions['company_name']}")
    print(f"Ticker: {assumptions['ticker']}")
    print(f"Outputs: {output_dir}")
    print("\nCreated files:")
    for file in sorted(output_dir.iterdir()):
        print(f"  {file.name}")

    print("\nKey valuation output:")
    print(format_dcf_summary(dcf_summary).to_string(index=False))


if __name__ == "__main__":
    main()
