# Import xlwings for cell interaction
import xlwings as xw
# Import the active sheet retriever
from excel.worksheet import get_active_sheet

def apply_formula(cell: str, formula: str) -> None:
    """
    Applies an Excel formula to a specific cell.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Ensure the formula starts with an equal sign for Excel to recognize it
    if not formula.startswith("="):
        # Prepend '=' if the user or parser omitted it
        formula = "=" + formula
    # Set the .formula property of the target cell range
    sheet.range(cell).formula = formula

def fill_formula(range_address: str, formula: str) -> None:
    """
    Applies a formula to a range of cells, allowing Excel to auto-adjust relative references.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Format formula appropriately
    if not formula.startswith("="):
        # Prepend '=' if omitted
        formula = "=" + formula
    # Write the formula string to the range.formula property to fill the range
    sheet.range(range_address).formula = formula

def get_formula(cell: str) -> str:
    """
    Gets the formula string from a cell. Returns None/empty if it's a value.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Access the .formula property of the cell and return it
    return sheet.range(cell).formula

def remove_formula(cell: str) -> None:
    """
    Removes the formula from a cell but keeps its calculated value.
    """
    # Retrieve the active sheet reference
    sheet = get_active_sheet()
    # Read the current evaluated/calculated value of the cell
    val = sheet.range(cell).value
    # Write the evaluated value back to the cell, which overwrites/removes the formula
    sheet.range(cell).value = val
