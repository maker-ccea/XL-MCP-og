# Import xlwings for Excel operations
import xlwings as xw
# Import List and Optional type helpers
from typing import List, Optional
# Import get_active_workbook to query sheets on the active book
from excel.workbook import get_active_workbook

def get_active_sheet() -> xw.Sheet:
    """
    Returns the currently active worksheet of the active workbook.
    """
    # Retrieve the active workbook reference
    book = get_active_workbook()
    # Check if a workbook is active
    if book is None:
        # Raise ValueError if no active workbook is found
        raise ValueError("No active workbook is open. Cannot get active sheet.")
    # Return the active sheet from the workbook's sheets collection
    return book.sheets.active

def get_sheets() -> List[str]:
    """
    Returns a list of names of all worksheets in the active workbook.
    """
    # Retrieve the active workbook reference
    book = get_active_workbook()
    # Check if a workbook is active
    if book is None:
        # Raise ValueError if no active workbook is open
        raise ValueError("No active workbook is open. Cannot list sheets.")
    # Extract the name property of every sheet in the workbook
    return [sheet.name for sheet in book.sheets]

def create_sheet(name: str) -> xw.Sheet:
    """
    Creates a new worksheet with the specified name in the active workbook.
    """
    # Retrieve the active workbook reference
    book = get_active_workbook()
    # Check if a workbook is active
    if book is None:
        # Raise ValueError if no active workbook is open
        raise ValueError("No active workbook is open. Cannot create sheet.")
    # Add a sheet to the sheets collection with the specified name
    sheet = book.sheets.add(name=name)
    # Return the newly created Sheet object
    return sheet

def rename_sheet(old_name: str, new_name: str) -> xw.Sheet:
    """
    Renames a sheet in the active workbook from old_name to new_name.
    """
    # Retrieve the active workbook reference
    book = get_active_workbook()
    # Check if a workbook is active
    if book is None:
        # Raise ValueError if no active workbook is open
        raise ValueError("No active workbook is open. Cannot rename sheet.")
    # Retrieve the sheet object using its current name
    sheet = book.sheets[old_name]
    # Set the sheet name property to the new name value
    sheet.name = new_name
    # Return the updated sheet reference
    return sheet

def delete_sheet(name: str) -> None:
    """
    Deletes the worksheet with the specified name in the active workbook.
    """
    # Retrieve the active workbook reference
    book = get_active_workbook()
    # Check if a workbook is active
    if book is None:
        # Raise ValueError if no active workbook is open
        raise ValueError("No active workbook is open. Cannot delete sheet.")
    # Delete the sheet by indexing into the sheets collection
    book.sheets[name].delete()

def activate_sheet(name: str) -> xw.Sheet:
    """
    Activates the worksheet with the specified name.
    """
    # Retrieve the active workbook reference
    book = get_active_workbook()
    # Check if a workbook is active
    if book is None:
        # Raise ValueError if no active workbook is open
        raise ValueError("No active workbook is open. Cannot activate sheet.")
    # Retrieve the target sheet from the workbook
    sheet = book.sheets[name]
    # Activate the sheet to focus it in Excel
    sheet.activate()
    # Return the activated sheet
    return sheet
