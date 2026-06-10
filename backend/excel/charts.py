import xlwings as xw
from typing import Optional
from excel.excel_connection import excel_conn
import logging

logger = logging.getLogger("excel_charts")

# Friendly name → Excel ChartType integer constant (COM / VBA values)
CHART_TYPE_MAP: dict[str, int] = {
    "column":           51,    # xlColumnClustered
    "column_clustered": 51,
    "column_stacked":   52,    # xlColumnStacked
    "column_100":       53,    # xlColumnStacked100
    "bar":              57,    # xlBarClustered
    "bar_clustered":    57,
    "bar_stacked":      58,    # xlBarStacked
    "bar_100":          59,    # xlBarStacked100
    "line":             4,     # xlLine
    "line_markers":     65,    # xlLineMarkers
    "line_stacked":     63,    # xlLineStacked
    "pie":              5,     # xlPie
    "pie_exploded":     69,    # xlPieExploded
    "scatter":         -4169,  # xlXYScatter
    "scatter_lines":    74,    # xlXYScatterLines
    "area":             1,     # xlArea
    "area_stacked":     76,    # xlAreaStacked
    "doughnut":        -4120,  # xlDoughnut
    "radar":           -4151,  # xlRadar
    "bubble":           15,    # xlBubble
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

    # Activate the sheet so Excel COM can place the chart correctly
    sheet.activate()

    src_range = sheet.range(data_range)

    # Auto-position: below the source data with a small gap
    chart_left = left if left is not None else src_range.left
    chart_top  = top  if top  is not None else src_range.top + src_range.height + 12

    ct = CHART_TYPE_MAP.get(chart_type.lower().replace(" ", "_"), 51)

    # sheet.charts.add() returns an xw.Chart whose .api is the COM ChartObject.
    # All chart settings live on .api.Chart (the COM Chart object inside ChartObject).
    chart_obj: xw.Chart = sheet.charts.add(
        left=chart_left,
        top=chart_top,
        width=width,
        height=height,
    )

    # Access the inner COM Chart object
    com_chart = chart_obj.api.Chart

    # Set chart type via COM
    com_chart.ChartType = ct

    # Set source data via COM (Range.api gives the COM Range)
    com_chart.SetSourceData(src_range.api)

    # Set title via COM
    if title:
        com_chart.HasTitle = True
        com_chart.ChartTitle.Text = title

    # Give the ChartObject a friendly name (separate from the visible title)
    if title:
        chart_obj.name = title

    chart_name = chart_obj.name
    logger.info(f"Created chart '{chart_name}' (type={chart_type}, ct={ct}) from {data_range}")
    return chart_name


def delete_chart(name: str, sheet_name: Optional[str] = None) -> None:
    """Deletes a named chart from the sheet."""
    sheet = _get_sheet(sheet_name)
    for ch in sheet.charts:
        if ch.name == name:
            ch.delete()
            logger.info(f"Deleted chart '{name}'")
            return
    raise ValueError(f"Chart '{name}' not found on sheet '{sheet.name}'")


def update_chart_title(name: str, title: str, sheet_name: Optional[str] = None) -> None:
    """Updates the visible title of a named chart."""
    sheet = _get_sheet(sheet_name)
    for ch in sheet.charts:
        if ch.name == name:
            com_chart = ch.api.Chart   # inner COM Chart object
            com_chart.HasTitle = True
            com_chart.ChartTitle.Text = title
            logger.info(f"Updated chart '{name}' title → '{title}'")
            return
    raise ValueError(f"Chart '{name}' not found on sheet '{sheet.name}'")
