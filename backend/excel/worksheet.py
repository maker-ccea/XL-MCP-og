
import xlwings as xw

from typing import List, Optional

from excel.workbook import get_active_workbook

def get_active_sheet() -> xw.Sheet:
    """
    Returns the currently active worksheet of the active workbook.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook is open. Cannot get active sheet.")

    return book.sheets.active

def get_sheets() -> List[str]:
    """
    Returns a list of names of all worksheets in the active workbook.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook is open. Cannot list sheets.")

    return [sheet.name for sheet in book.sheets]

def create_sheet(name: str) -> xw.Sheet:
    """
    Creates a new worksheet with the specified name in the active workbook.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook is open. Cannot create sheet.")

    sheet = book.sheets.add(name=name)

    return sheet

def rename_sheet(old_name: str, new_name: str) -> xw.Sheet:
    """
    Renames a sheet in the active workbook from old_name to new_name.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook is open. Cannot rename sheet.")

    sheet = book.sheets[old_name]

    sheet.name = new_name

    return sheet

def delete_sheet(name: str) -> None:
    """
    Deletes the worksheet with the specified name in the active workbook.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook is open. Cannot delete sheet.")

    book.sheets[name].delete()

def activate_sheet(name: str) -> xw.Sheet:
    """
    Activates the worksheet with the specified name.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook is open. Cannot activate sheet.")

    sheet = book.sheets[name]

    sheet.activate()

    return sheet