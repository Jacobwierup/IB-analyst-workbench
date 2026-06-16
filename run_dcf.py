from pathlib import Path

from src.financials import load_company_data, build_historical_model
from src.dcf import build_all_dcf_cases, format_dcf_summary


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

    dcf_summary.to_csv(output_dir / "dcf_summary_raw.csv", index=False)
    format_dcf_summary(dcf_summary).to_csv(output_dir / "dcf_summary_formatted.csv", index=False)

    for case_name, result in dcf_results.items():
        result.forecast.to_csv(output_dir / f"dcf_forecast_{case_name}.csv", index=False)

    print("\nDCF valuation summary for Saab AB\n")
    print(format_dcf_summary(dcf_summary).to_string(index=False))
    print("\nSaved DCF outputs to outputs/SAAB_B/")


if __name__ == "__main__":
    main()
