from pathlib import Path
from src.financials import load_company_data, build_historical_model, format_model_for_output


def main():
    company_dir = Path("data/companies/SAAB_B")
    output_dir = Path("outputs/SAAB_B")
    output_dir.mkdir(parents=True, exist_ok=True)

    data = load_company_data(company_dir)
    model = build_historical_model(data)

    model.to_csv(output_dir / "historical_model_raw.csv", index=False)
    format_model_for_output(model).to_csv(output_dir / "historical_model_formatted.csv", index=False)

    selected_cols = [
        "year",
        "revenue",
        "revenue_growth",
        "ebitda",
        "ebitda_margin",
        "ebit",
        "ebit_margin",
        "net_income",
        "net_debt",
        "market_cap",
        "enterprise_value",
        "ev_revenue",
        "ev_ebitda",
        "pe",
        "net_debt_ebitda",
    ]

    print("\nHistorical company model created for Saab AB\n")
    print(format_model_for_output(model)[selected_cols].to_string(index=False))
    print("\nSaved outputs to outputs/SAAB_B/")


if __name__ == "__main__":
    main()
