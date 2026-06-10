# Import necessary modules from Pydantic and Python typing library
from pydantic import BaseModel, Field
from typing import Any, List, Optional, Literal, Union

# Define the base action model that all actions will inherit from
class BaseAction(BaseModel):
    # Action name will act as a type discriminator
    action: str

# --- Workbook Actions ---

# Action schema for opening a workbook
class OpenWorkbookAction(BaseAction):
    # The action name field, constrained to literal 'open_workbook'
    action: Literal["open_workbook"] = "open_workbook"
    # File path of the workbook to open
    path: str = Field(..., description="The absolute or relative path to the Excel file to open")

# Action schema for creating a new workbook
class CreateWorkbookAction(BaseAction):
    # The action name field, constrained to literal 'create_workbook'
    action: Literal["create_workbook"] = "create_workbook"

# Action schema for saving the active workbook
class SaveWorkbookAction(BaseAction):
    # The action name field, constrained to literal 'save_workbook'
    action: Literal["save_workbook"] = "save_workbook"

# Action schema for saving the active workbook with a specific name/path
class SaveWorkbookAsAction(BaseAction):
    # The action name field, constrained to literal 'save_workbook_as'
    action: Literal["save_workbook_as"] = "save_workbook_as"
    # Target path to save the workbook
    path: str = Field(..., description="The absolute path where the workbook should be saved")

# Action schema for closing the active workbook
class CloseWorkbookAction(BaseAction):
    # The action name field, constrained to literal 'close_workbook'
    action: Literal["close_workbook"] = "close_workbook"

# --- Worksheet Actions ---

# Action schema for creating a new worksheet
class CreateSheetAction(BaseAction):
    # The action name field, constrained to literal 'create_sheet'
    action: Literal["create_sheet"] = "create_sheet"
    # Name of the worksheet to create
    name: str = Field(..., description="The name of the sheet to create")

# Action schema for renaming an existing worksheet
class RenameSheetAction(BaseAction):
    # The action name field, constrained to literal 'rename_sheet'
    action: Literal["rename_sheet"] = "rename_sheet"
    # Current name of the worksheet
    old_name: str = Field(..., description="The current name of the sheet to rename")
    # New name of the worksheet
    new_name: str = Field(..., description="The new name of the sheet")

# Action schema for deleting a worksheet
class DeleteSheetAction(BaseAction):
    # The action name field, constrained to literal 'delete_sheet'
    action: Literal["delete_sheet"] = "delete_sheet"
    # Name of the sheet to delete
    name: str = Field(..., description="The name of the sheet to delete")

# Action schema for activating/selecting a worksheet
class ActivateSheetAction(BaseAction):
    # The action name field, constrained to literal 'activate_sheet'
    action: Literal["activate_sheet"] = "activate_sheet"
    # Name of the sheet to activate
    name: str = Field(..., description="The name of the sheet to activate")

# --- Cell Actions ---

# Action schema for writing a value to a single cell
class WriteCellAction(BaseAction):
    # The action name field, constrained to literal 'write_cell'
    action: Literal["write_cell"] = "write_cell"
    # The cell address (e.g. A1, B2)
    cell: str = Field(..., description="The cell coordinate/address, e.g. A1")
    # The value to write to the cell (could be number, string, boolean)
    value: Any = Field(..., description="The value to write into the cell")

# Action schema for writing a 2D array of data to a range
class WriteRangeAction(BaseAction):
    # The action name field, constrained to literal 'write_range'
    action: Literal["write_range"] = "write_range"
    # The starting cell or the bounding range (e.g. A1 or A1:C3)
    range: str = Field(..., description="The target range or start cell coordinate, e.g. A1 or A1:C3")
    # 2D list containing row and column values to write
    data: List[List[Any]] = Field(..., description="The 2D array of values to write")

# Action schema for clearing content in a range of cells
class ClearCellsAction(BaseAction):
    # The action name field, constrained to literal 'clear_cells'
    action: Literal["clear_cells"] = "clear_cells"
    # The target range to clear
    range: str = Field(..., description="The range of cells to clear, e.g. A1:B10")

# --- Formula Actions ---

# Action schema for writing a formula to a single cell
class ApplyFormulaAction(BaseAction):
    # The action name field, constrained to literal 'apply_formula'
    action: Literal["apply_formula"] = "apply_formula"
    # Target cell address
    cell: str = Field(..., description="The cell coordinate to apply the formula to")
    # Excel formula string (must start with '=')
    formula: str = Field(..., description="The formula string starting with =, e.g. =SUM(A1:A10)")

# Action schema for filling a formula down/across a range
class FillFormulaAction(BaseAction):
    # The action name field, constrained to literal 'fill_formula'
    action: Literal["fill_formula"] = "fill_formula"
    # Target range to fill the formula into
    range: str = Field(..., description="The range to populate with the formula, e.g. A1:A10")
    # The formula to apply to the range (standard or relative template)
    formula: str = Field(..., description="The base formula to fill, e.g. =SUM(B1:C1)")

# Action schema for removing a formula but keeping the value
class RemoveFormulaAction(BaseAction):
    # The action name field, constrained to literal 'remove_formula'
    action: Literal["remove_formula"] = "remove_formula"
    # Cell address to clear formula from
    cell: str = Field(..., description="The cell address to strip the formula from, retaining its value")

# --- Formatting Actions ---

# Action schema to make font bold
class SetBoldAction(BaseAction):
    # The action name field, constrained to literal 'set_bold'
    action: Literal["set_bold"] = "set_bold"
    # Target range
    range: str = Field(..., description="The range of cells to format")
    # Bold flag (True to apply, False to remove)
    bold: bool = Field(True, description="Whether the font should be bold")

# Action schema to make font italic
class SetItalicAction(BaseAction):
    # The action name field, constrained to literal 'set_italic'
    action: Literal["set_italic"] = "set_italic"
    # Target range
    range: str = Field(..., description="The range of cells to format")
    # Italic flag (True to apply, False to remove)
    italic: bool = Field(True, description="Whether the font should be italic")

# Action schema to change font size
class SetFontSizeAction(BaseAction):
    # The action name field, constrained to literal 'set_font_size'
    action: Literal["set_font_size"] = "set_font_size"
    # Target range
    range: str = Field(..., description="The range of cells to format")
    # Target font size
    size: float = Field(..., description="The font size in points, e.g. 12")

# Action schema to change font color
class SetFontColorAction(BaseAction):
    # The action name field, constrained to literal 'set_font_color'
    action: Literal["set_font_color"] = "set_font_color"
    # Target range
    range: str = Field(..., description="The range of cells to format")
    # Hex or standard color string, e.g. "#FF0000" or "red"
    color: str = Field(..., description="The color name or HEX code for font")

# Action schema to change range background color
class SetBackgroundColorAction(BaseAction):
    # The action name field, constrained to literal 'set_background_color'
    action: Literal["set_background_color"] = "set_background_color"
    # Target range
    range: str = Field(..., description="The range of cells to format")
    # Hex or standard color string, e.g. "#FFFF00" or "yellow"
    color: str = Field(..., description="The color name or HEX code for background")

# Action schema to auto-fit columns based on content size
class AutoFitColumnsAction(BaseAction):
    # The action name field, constrained to literal 'auto_fit_columns'
    action: Literal["auto_fit_columns"] = "auto_fit_columns"
    # Target range
    range: str = Field(..., description="The range/columns to auto fit")

# --- Chart Actions ---

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

# Define a Union type of all possible actions for parsing and validation
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
]
