from pathlib import Path

import pandas as pd
import streamlit as st

from src.financials import load_company_data, build_historical_model, format_model_for_output
from src.dcf import build_all_dcf_cases, format_dcf_summary
from src.sensitivity import (
    build_wacc_terminal_growth_sensitivity,
    build_revenue_margin_sensitivity,
    format_sensitivity_table,
)

st.set_page_config(page_title="IB Analyst Workbench", layout="wide")

company_dir = Path("data/companies/SAAB_B")
output_dir = Path("outputs/SAAB_B")

st.title("Investment Banking Analyst Workbench")
st.write("Institutional style valuation, DCF, sensitivity analysis and investment memo dashboard.")

data = load_company_data(company_dir)
assumptions = data["assumptions"]

historical_model = build_historical_model(data)
dcf_summary, dcf_results = build_all_dcf_cases(historical_model, assumptions)

wacc_tg = build_wacc_terminal_growth_sensitivity(historical_model, assumptions)
rev_margin = build_revenue_margin_sensitivity(historical_model, assumptions)

latest = historical_model.sort_values("year").iloc[-1]

st.warning(
    "Current financial inputs are placeholder values used to validate the model architecture. "
    "Replace with verified reported financials before real analysis."
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Company", assumptions["company_name"])
col2.metric("Ticker", assumptions["ticker"])
col3.metric("Revenue", f"{latest['revenue']:,.0f} SEKm")
col4.metric("EV / EBITDA", f"{latest['ev_ebitda']:.1f}x")

st.subheader("DCF Valuation Summary")
st.dataframe(format_dcf_summary(dcf_summary), use_container_width=True)

base = dcf_summary[dcf_summary["case"] == "Base"].iloc[0]
bear = dcf_summary[dcf_summary["case"] == "Bear"].iloc[0]
bull = dcf_summary[dcf_summary["case"] == "Bull"].iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Bear Case", f"{bear['implied_share_price']:,.2f} SEK")
c2.metric("Base Case", f"{base['implied_share_price']:,.2f} SEK")
c3.metric("Bull Case", f"{bull['implied_share_price']:,.2f} SEK")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Historical Model",
    "DCF Forecasts",
    "Sensitivity",
    "Memo",
    "Files",
])

with tab1:
    st.subheader("Historical Company Model")
    st.dataframe(format_model_for_output(historical_model), use_container_width=True)

with tab2:
    st.subheader("Base Case DCF")
    st.dataframe(dcf_results["base_case"].forecast, use_container_width=True)

    st.subheader("Bear Case DCF")
    st.dataframe(dcf_results["bear_case"].forecast, use_container_width=True)

    st.subheader("Bull Case DCF")
    st.dataframe(dcf_results["bull_case"].forecast, use_container_width=True)

with tab3:
    st.subheader("WACC vs Terminal Growth Sensitivity")
    st.dataframe(format_sensitivity_table(wacc_tg, "terminal_growth"), use_container_width=True)

    st.subheader("Revenue Growth vs EBIT Margin Sensitivity")
    st.dataframe(format_sensitivity_table(rev_margin, "ebit_margin_adjustment"), use_container_width=True)

with tab4:
    st.subheader("Investment Committee Memo")
    memo_path = output_dir / "investment_committee_memo.md"
    if memo_path.exists():
        st.markdown(memo_path.read_text(encoding="utf-8"))
    else:
        st.error("Memo not found. Run python run_full_model.py first.")

with tab5:
    st.subheader("Generated Files")

    for file in sorted(output_dir.glob("*")):
        st.write(file.name)

    excel_path = output_dir / "saab_valuation_model.xlsx"
    memo_path = output_dir / "investment_committee_memo.md"

    if excel_path.exists():
        st.download_button(
            "Download Excel valuation model",
            data=excel_path.read_bytes(),
            file_name="saab_valuation_model.xlsx",
        )

    if memo_path.exists():
        st.download_button(
            "Download investment committee memo",
            data=memo_path.read_bytes(),
            file_name="investment_committee_memo.md",
        )

st.caption("Educational portfolio project only. Not investment advice.")
