
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Literal, Union


class BaseAction(BaseModel):

    action: str

    id: Optional[str] = Field(None, description="Optional unique identifier for this action instance")




class OpenWorkbookAction(BaseAction):

    action: Literal["open_workbook"] = "open_workbook"

    path: str = Field(..., description="The absolute or relative path to the Excel file to open")


class CreateWorkbookAction(BaseAction):

    action: Literal["create_workbook"] = "create_workbook"


class SaveWorkbookAction(BaseAction):

    action: Literal["save_workbook"] = "save_workbook"


class SaveWorkbookAsAction(BaseAction):

    action: Literal["save_workbook_as"] = "save_workbook_as"

    path: str = Field(..., description="The absolute path where the workbook should be saved")


class CloseWorkbookAction(BaseAction):

    action: Literal["close_workbook"] = "close_workbook"




class CreateSheetAction(BaseAction):

    action: Literal["create_sheet"] = "create_sheet"

    name: str = Field(..., description="The name of the sheet to create")


class RenameSheetAction(BaseAction):

    action: Literal["rename_sheet"] = "rename_sheet"

    old_name: str = Field(..., description="The current name of the sheet to rename")

    new_name: str = Field(..., description="The new name of the sheet")


class DeleteSheetAction(BaseAction):

    action: Literal["delete_sheet"] = "delete_sheet"

    name: str = Field(..., description="The name of the sheet to delete")


class ActivateSheetAction(BaseAction):

    action: Literal["activate_sheet"] = "activate_sheet"

    name: str = Field(..., description="The name of the sheet to activate")




class WriteCellAction(BaseAction):

    action: Literal["write_cell"] = "write_cell"

    cell: str = Field(..., description="The cell coordinate/address, e.g. A1")

    value: Any = Field(..., description="The value to write into the cell")


class WriteRangeAction(BaseAction):

    action: Literal["write_range"] = "write_range"

    range: str = Field(..., description="The target range or start cell coordinate, e.g. A1 or A1:C3")

    data: List[List[Any]] = Field(..., description="The 2D array of values to write")


class ClearCellsAction(BaseAction):

    action: Literal["clear_cells"] = "clear_cells"

    range: str = Field(..., description="The range of cells to clear, e.g. A1:B10")




class ApplyFormulaAction(BaseAction):

    action: Literal["apply_formula"] = "apply_formula"

    cell: str = Field(..., description="The cell coordinate to apply the formula to")

    formula: str = Field(..., description="The formula string starting with =, e.g. =SUM(A1:A10)")


class FillFormulaAction(BaseAction):

    action: Literal["fill_formula"] = "fill_formula"

    range: str = Field(..., description="The range to populate with the formula, e.g. A1:A10")

    formula: str = Field(..., description="The base formula to fill, e.g. =SUM(B1:C1)")


class RemoveFormulaAction(BaseAction):

    action: Literal["remove_formula"] = "remove_formula"

    cell: str = Field(..., description="The cell address to strip the formula from, retaining its value")




class SetBoldAction(BaseAction):

    action: Literal["set_bold"] = "set_bold"

    range: str = Field(..., description="The range of cells to format")

    bold: bool = Field(True, description="Whether the font should be bold")


class SetItalicAction(BaseAction):

    action: Literal["set_italic"] = "set_italic"

    range: str = Field(..., description="The range of cells to format")

    italic: bool = Field(True, description="Whether the font should be italic")


class SetFontSizeAction(BaseAction):

    action: Literal["set_font_size"] = "set_font_size"

    range: str = Field(..., description="The range of cells to format")

    size: float = Field(..., description="The font size in points, e.g. 12")


class SetFontColorAction(BaseAction):

    action: Literal["set_font_color"] = "set_font_color"

    range: str = Field(..., description="The range of cells to format")

    color: str = Field(..., description="The color name or HEX code for font")


class SetBackgroundColorAction(BaseAction):

    action: Literal["set_background_color"] = "set_background_color"

    range: str = Field(..., description="The range of cells to format")

    color: str = Field(..., description="The color name or HEX code for background")


class AutoFitColumnsAction(BaseAction):

    action: Literal["auto_fit_columns"] = "auto_fit_columns"

    range: str = Field(..., description="The range/columns to auto fit")



class CreateChartAction(BaseAction):
    action: Literal["create_chart"] = "create_chart"
    data_range: str = Field(..., description="The cell range containing chart data, e.g. A1:E4")
    chart_type: str = Field("column", description="Chart type: column, bar, line, pie, scatter, area, doughnut, line_markers, column_stacked, bar_stacked")
    title: Optional[str] = Field(None, description="Optional chart title")
    sheet: Optional[str] = Field(None, description="Sheet name to insert chart on (defaults to active sheet)")
    left: Optional[float] = Field(None, description="Left position in points (auto-placed below data if omitted)")
    top: Optional[float] = Field(None, description="Top position in points (auto-placed below data if omitted)")
    width: float = Field(375, description="Chart width in points")
    height: float = Field(225, description="Chart height in points")

class DeleteChartAction(BaseAction):
    action: Literal["delete_chart"] = "delete_chart"
    name: str = Field(..., description="Name of the chart to delete")
    sheet: Optional[str] = Field(None, description="Sheet name containing the chart (defaults to active sheet)")

class UpdateChartTitleAction(BaseAction):
    action: Literal["update_chart_title"] = "update_chart_title"
    name: str = Field(..., description="Name of the chart to update")
    title: str = Field(..., description="New title text for the chart")
    sheet: Optional[str] = Field(None, description="Sheet name containing the chart (defaults to active sheet)")

class SortRangeAction(BaseAction):
    action: Literal["sort_range"] = "sort_range"
    range: str = Field(..., description="The range of the data table to sort, e.g. A1:C50")
    key_column: int = Field(..., description="The 1-based column index to sort by (relative to sheet or range), e.g. 2 for column B or second column")
    ascending: bool = Field(True, description="Whether to sort in ascending order (default true)")
    has_headers: bool = Field(True, description="Whether the data range has a header row (default true)")

ExcelAction = Union[
    OpenWorkbookAction,
    CreateWorkbookAction,
    SaveWorkbookAction,
    SaveWorkbookAsAction,
    CloseWorkbookAction,
    CreateSheetAction,
    RenameSheetAction,
    DeleteSheetAction,
    ActivateSheetAction,
    WriteCellAction,
    WriteRangeAction,
    ClearCellsAction,
    ApplyFormulaAction,
    FillFormulaAction,
    RemoveFormulaAction,
    SetBoldAction,
    SetItalicAction,
    SetFontSizeAction,
    SetFontColorAction,
    SetBackgroundColorAction,
    AutoFitColumnsAction,
    CreateChartAction,
    DeleteChartAction,
    UpdateChartTitleAction,
    SortRangeAction,
]