from __future__ import annotations

from pathlib import Path
import pandas as pd


def autosize_columns(writer, sheet_name: str, df: pd.DataFrame) -> None:
    worksheet = writer.sheets[sheet_name]

    for idx, col in enumerate(df.columns):
        max_len = max(
            len(str(col)),
            *(len(str(value)) for value in df[col].head(200).values),
        )
        worksheet.set_column(idx, idx, min(max_len + 2, 28))


def write_model_workbook(
    output_path: str | Path,
    historical_model: pd.DataFrame,
    dcf_summary: pd.DataFrame,
    dcf_results: dict,
    wacc_terminal_growth: pd.DataFrame,
    revenue_margin: pd.DataFrame,
) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        workbook = writer.book

        title_format = workbook.add_format(
            {
                "bold": True,
                "font_size": 14,
                "bg_color": "#D9EAF7",
                "border": 1,
            }
        )

        header_format = workbook.add_format(
            {
                "bold": True,
                "bg_color": "#E2F0D9",
                "border": 1,
            }
        )

        number_format = workbook.add_format({"num_format": "#,##0.0"})
        multiple_format = workbook.add_format({"num_format": "0.0x"})
        percent_format = workbook.add_format({"num_format": "0.0%"})
        price_format = workbook.add_format({"num_format": "#,##0.00"})

        summary = pd.DataFrame(
            {
                "Metric": [
                    "Company",
                    "Model type",
                    "Output",
                    "Note",
                ],
                "Value": [
                    "Saab AB",
                    "Institutional valuation workbench",
                    "Historical model, DCF, scenarios and sensitivities",
                    "Illustrative placeholder financials until public reported data is inserted",
                ],
            }
        )

        summary.to_excel(writer, sheet_name="Summary", index=False, startrow=2)
        ws = writer.sheets["Summary"]
        ws.write(0, 0, "Investment Banking Analyst Workbench", title_format)
        autosize_columns(writer, "Summary", summary)

        historical_model.to_excel(writer, sheet_name="Historical Model", index=False)
        autosize_columns(writer, "Historical Model", historical_model)

        dcf_summary.to_excel(writer, sheet_name="DCF Summary", index=False)
        autosize_columns(writer, "DCF Summary", dcf_summary)

        for case_name, result in dcf_results.items():
            sheet_name = case_name.replace("_case", "").title() + " DCF"
            result.forecast.to_excel(writer, sheet_name=sheet_name, index=False)
            autosize_columns(writer, sheet_name, result.forecast)

        wacc_terminal_growth.to_excel(writer, sheet_name="WACC Sensitivity", index=False)
        autosize_columns(writer, "WACC Sensitivity", wacc_terminal_growth)

        revenue_margin.to_excel(writer, sheet_name="Growth Margin Sens", index=False)
        autosize_columns(writer, "Growth Margin Sens", revenue_margin)

        for sheet_name, worksheet in writer.sheets.items():
            worksheet.freeze_panes(1, 0)

        for sheet_name in [
            "Historical Model",
            "DCF Summary",
            "Bear DCF",
            "Base DCF",
            "Bull DCF",
            "WACC Sensitivity",
            "Growth Margin Sens",
        ]:
            if sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_row(0, None, header_format)
