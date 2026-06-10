# Import xlwings for Cell/Range interaction
import xlwings as xw
# Import Any and List type hints
from typing import Any, List
# Import get_active_sheet helper to target active context
from excel.worksheet import get_active_sheet

def read_cell(cell: str) -> Any:
    """
    Reads the value of a single cell on the active sheet.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Read and return the value from the specific cell coordinate (e.g. 'A1')
    return sheet.range(cell).value

def read_range(range_address: str) -> Any:
    """
    Reads the values of a range of cells on the active sheet.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Access the range and return the value (could be a single value, 1D list, or 2D list)
    return sheet.range(range_address).value

def write_cell(cell: str, value: Any) -> None:
    """
    Writes a value to a single cell on the active sheet.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Assign the specified value to the target cell range
    sheet.range(cell).value = value

def write_range(range_address: str, data: Any) -> None:
    """
    Writes a value or a list/matrix of values to a range on the active sheet.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Assign the structured data (like a 2D list or matrix) to the cell range starting at range_address
    sheet.range(range_address).value = data

def clear_cells(range_address: str) -> None:
    """
    Clears the contents of a range of cells on the active sheet, leaving formatting intact.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Call clear_contents() to delete values and formulas without removing formats
    sheet.range(range_address).clear_contents()
