
import xlwings as xw

from excel.worksheet import get_active_sheet

def apply_formula(cell: str, formula: str) -> None:
    """
    Applies an Excel formula to a specific cell.
    """

    sheet = get_active_sheet()

    if not formula.startswith("="):

        formula = "=" + formula

    sheet.range(cell).formula = formula

def fill_formula(range_address: str, formula: str) -> None:
    """
    Applies a formula to a range of cells, allowing Excel to auto-adjust relative references.
    """

    sheet = get_active_sheet()

    if not formula.startswith("="):

        formula = "=" + formula

    sheet.range(range_address).formula = formula

def get_formula(cell: str) -> str:
    """
    Gets the formula string from a cell. Returns None/empty if it's a value.
    """

    sheet = get_active_sheet()

    return sheet.range(cell).formula

def remove_formula(cell: str) -> None:
    """
    Removes the formula from a cell but keeps its calculated value.
    """

    sheet = get_active_sheet()

    val = sheet.range(cell).value

    sheet.range(cell).value = val