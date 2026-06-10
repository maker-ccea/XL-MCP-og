# Import xlwings for Excel application interface
import xlwings as xw
# Import Dict and Optional type helpers
from typing import Dict, Any, Optional
# Import the connection manager to acquire current app reference
from excel.excel_connection import excel_conn
# Import workbook and worksheet helpers
from excel.workbook import get_active_workbook
from excel.worksheet import get_active_sheet, get_sheets

def get_selected_range() -> Optional[str]:
    """
    Returns the address of the currently selected cell range (e.g., "$A$1:$B$5").
    Returns None if no range is selected or no workbook is active.
    """
    try:
        # Retrieve active app instance
        app = excel_conn.get_excel_app()
        # Retrieve the selection property from active Excel application
        selection = app.selection
        # If selection is a valid Range object
        if selection is not None:
            # Return the range address string (e.g. '$A$1')
            return selection.address
        # Return None if selection is empty
        return None
    except Exception:
        # Return None if no workbook or range is selected
        return None

def get_active_sheet_name() -> Optional[str]:
    """
    Returns the name of the currently active sheet.
    """
    try:
        # Retrieve active sheet reference
        sheet = get_active_sheet()
        # Return sheet name property
        return sheet.name
    except Exception:
        # Return None if no sheet is active/available
        return None

def get_workbook_context() -> Dict[str, Any]:
    """
    Aggregates workbook name, sheet name, selected range address,
    and a list of all sheets in the current active workbook.
    """
    # Retrieve active workbook reference
    book = get_active_workbook()
    
    # If no workbook is active, return an empty/default context
    if book is None:
        return {
            "workbook_name": None,
            "sheet_name": None,
            "selected_range": None,
            "available_sheets": []
        }

    # Initialize a list for sheet names
    sheet_list = []
    try:
        # Fetch names of all sheets in the active workbook
        sheet_list = get_sheets()
    except Exception:
        # Fail silently and keep list empty if sheets cannot be retrieved
        pass

    # Build and return the context dictionary
    return {
        "workbook_name": book.name,
        "sheet_name": get_active_sheet_name(),
        "selected_range": get_selected_range(),
        "available_sheets": sheet_list
    }
