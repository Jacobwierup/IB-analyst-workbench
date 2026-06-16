# Investment Banking Analyst Workbench

A Raspberry Pi hosted institutional style valuation and corporate finance modelling project.

This project converts structured company financials into investment banking style outputs.

## Features

1. Historical company model
2. Enterprise value bridge
3. Valuation multiples
4. DCF valuation
5. Bear, base and bull scenario analysis
6. WACC and terminal growth sensitivity tables
7. Revenue growth and EBIT margin sensitivity tables
8. Excel valuation workbook
9. Investment committee style memo

## Current Case Study

The current version uses Saab AB as the first company case study.

## Run the Full Model

Activate the virtual environment:

    source venv/bin/activate

Run the complete model:

    python run_full_model.py

## Outputs

Outputs are saved to:

    outputs/SAAB_B/

Main output files:

    saab_valuation_model.xlsx
    investment_committee_memo.md
    dcf_summary_raw.csv
    historical_model_raw.csv
    sensitivity_wacc_terminal_growth_raw.csv
    sensitivity_revenue_margin_raw.csv

## Important Data Note

The current financial inputs are placeholder values used to validate the model architecture.

Before using the project for real analysis, replace the input files with verified reported figures from annual reports, interim reports, company filings and public market data sources.

## Disclaimer

This project is for educational and portfolio purposes only. It is not investment advice, financial advice, or a recommendation to buy or sell securities.
