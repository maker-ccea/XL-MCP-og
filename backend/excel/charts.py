import xlwings as xw
from typing import Optional
from excel.excel_connection import excel_conn
import logging

logger = logging.getLogger("excel_charts")


CHART_TYPE_MAP: dict[str, int] = {
    "column":           51,
    "column_clustered": 51,
    "column_stacked":   52,
    "column_100":       53,
    "bar":              57,
    "bar_clustered":    57,
    "bar_stacked":      58,
    "bar_100":          59,
    "line":             4,
    "line_markers":     65,
    "line_stacked":     63,
    "pie":              5,
    "pie_exploded":     69,
    "scatter":         -4169,
    "scatter_lines":    74,
    "area":             1,
    "area_stacked":     76,
    "doughnut":        -4120,
    "radar":           -4151,
    "bubble":           15,
}


def _get_sheet(sheet_name: Optional[str] = None) -> xw.Sheet:
    app = excel_conn.get_excel_app()
    wb = app.books.active
    if sheet_name:
        return wb.sheets[sheet_name]
    return wb.sheets.active


def create_chart(
    data_range: str,
    chart_type: str = "column",
    title: Optional[str] = None,
    sheet_name: Optional[str] = None,
    left: Optional[float] = None,
    top: Optional[float] = None,
    width: float = 375,
    height: float = 225,
) -> str:
    """
    Creates an embedded chart on the sheet sourced from data_range.
    Uses raw COM API to avoid xlwings abstraction gaps on Windows.
    Returns the name Excel assigned to the chart object.
    """
    sheet = _get_sheet(sheet_name)


    sheet.activate()

    src_range = sheet.range(data_range)

    # Automatically detect and summarize categorical (text) data
    try:
        values = src_range.value
        flat_values = []
        if isinstance(values, list):
            for val in values:
                if isinstance(val, list):
                    flat_values.extend(val)
                else:
                    flat_values.append(val)
        else:
            flat_values.append(values)

        flat_values = [v for v in flat_values if v is not None and str(v).strip() != ""]

        def is_numeric(v):
            try:
                float(str(v))
                return True
            except ValueError:
                return False

        non_numeric_count = sum(1 for v in flat_values if not is_numeric(v))

        if len(flat_values) > 0 and (non_numeric_count / len(flat_values)) > 0.7:
            from collections import Counter
            counts = Counter(flat_values)

            # Determine where to put the summary table (leave a gap of 2 columns after used range)
            used_range = sheet.used_range
            start_col = used_range.last_cell.column + 2
            start_row = 1

            def col_to_letter(col_idx):
                letter = ""
                while col_idx > 0:
                    col_idx, remainder = divmod(col_idx - 1, 26)
                    letter = chr(65 + remainder) + letter
                return letter

            summary_col_letter = col_to_letter(start_col)
            end_col_letter = col_to_letter(start_col + 1)
            summary_range_str = f"{summary_col_letter}{start_row}"

            header_label = title or "Category"
            summary_data = [[header_label, "Count"]]
            for k, v in counts.items():
                summary_data.append([k, v])

            sheet.range(summary_range_str).value = summary_data
            sheet.range(f"{summary_col_letter}:{end_col_letter}").autofit()

            num_rows = len(summary_data)
            src_range = sheet.range(f"{summary_col_letter}{start_row}:{end_col_letter}{start_row + num_rows - 1}")
    except Exception as ex:
        logger.warning(f"Failed to auto-summarize chart data: {ex}")

    chart_left = left if left is not None else src_range.left
    chart_top  = top  if top  is not None else src_range.top + src_range.height + 12

    ct = CHART_TYPE_MAP.get(chart_type.lower().replace(" ", "_"), 51)



    chart_obj: xw.Chart = sheet.charts.add(
        left=chart_left,
        top=chart_top,
        width=width,
        height=height,
    )


    if isinstance(chart_obj.api, tuple):
        com_chart = chart_obj.api[1]
    else:
        com_chart = chart_obj.api.Chart


    com_chart.ChartType = ct


    com_chart.SetSourceData(src_range.api)


    if title:
        com_chart.HasTitle = True
        com_chart.ChartTitle.Text = title


    if title:
        chart_obj.name = title

    chart_name = chart_obj.name
    logger.info(f"Created chart '{chart_name}' (type={chart_type}, ct={ct}) from {data_range}")
    return chart_name


def delete_chart(name: str, sheet_name: Optional[str] = None) -> None:

    sheet = _get_sheet(sheet_name)
    for ch in sheet.charts:
        if ch.name == name:
            ch.delete()
            logger.info(f"Deleted chart '{name}'")
            return
    raise ValueError(f"Chart '{name}' not found on sheet '{sheet.name}'")


def update_chart_title(name: str, title: str, sheet_name: Optional[str] = None) -> None:

    sheet = _get_sheet(sheet_name)
    for ch in sheet.charts:
        if ch.name == name:
            if isinstance(ch.api, tuple):
                com_chart = ch.api[1]
            else:
                com_chart = ch.api.Chart
            com_chart.HasTitle = True
            com_chart.ChartTitle.Text = title
            logger.info(f"Updated chart '{name}' title → '{title}'")
            return
    raise ValueError(f"Chart '{name}' not found on sheet '{sheet.name}'")