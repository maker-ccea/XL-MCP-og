
import xlwings as xw

from typing import Any, List

from excel.worksheet import get_active_sheet

def read_cell(cell: str) -> Any:
    """
    Reads the value of a single cell on the active sheet.
    """

    sheet = get_active_sheet()

    return sheet.range(cell).value

def read_range(range_address: str) -> Any:
    """
    Reads the values of a range of cells on the active sheet.
    """

    sheet = get_active_sheet()

    return sheet.range(range_address).value

def write_cell(cell: str, value: Any) -> None:
    """
    Writes a value to a single cell on the active sheet.
    """

    sheet = get_active_sheet()

    sheet.range(cell).value = value

def write_range(range_address: str, data: Any) -> None:
    """
    Writes a value or a list/matrix of values to a range on the active sheet.
    """

    sheet = get_active_sheet()

    sheet.range(range_address).value = data

def clear_cells(range_address: str) -> None:
    """
    Clears the contents of a range of cells on the active sheet, leaving formatting intact.
    """

    sheet = get_active_sheet()

    sheet.range(range_address).clear_contents()