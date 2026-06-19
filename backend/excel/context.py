
import xlwings as xw

from typing import Dict, Any, Optional

from excel.excel_connection import excel_conn

from excel.workbook import get_active_workbook
from excel.worksheet import get_active_sheet, get_sheets

def get_selected_range() -> Optional[str]:
    """
    Returns the address of the currently selected cell range (e.g., "$A$1:$B$5").
    Returns None if no range is selected or no workbook is active.
    """
    try:

        app = excel_conn.get_excel_app()

        selection = app.selection

        if selection is not None:

            return selection.address

        return None
    except Exception:

        return None

def get_active_sheet_name() -> Optional[str]:
    """
    Returns the name of the currently active sheet.
    """
    try:

        sheet = get_active_sheet()

        return sheet.name
    except Exception:

        return None

def get_selected_range_data() -> Optional[Dict[str, Any]]:
    """
    Reads a subset of data from the active selection range (up to 10 rows and 5 columns)
    to provide a lightweight read-only preview grid on the frontend.
    """
    try:
        app = excel_conn.get_excel_app()
        selection = app.selection
        if selection is not None:

            first_row = selection.row
            first_col = selection.column
            num_rows = selection.rows.count
            num_cols = selection.columns.count

            limit_rows = min(num_rows, 10)
            limit_cols = min(num_cols, 5)

            sheet = selection.sheet
            sub_range = sheet.range((first_row, first_col), (first_row + limit_rows - 1, first_col + limit_cols - 1))

            raw_vals = sub_range.value

            if limit_rows == 1 and limit_cols == 1:
                vals = [[raw_vals]]
            elif limit_rows == 1:
                vals = [raw_vals]
            elif limit_cols == 1:
                vals = [[v] for v in raw_vals]
            else:
                vals = raw_vals


            def col_letter(col_idx: int) -> str:
                letter = ""
                while col_idx > 0:
                    col_idx, remainder = divmod(col_idx - 1, 26)
                    letter = chr(65 + remainder) + letter
                return letter

            headers = [col_letter(c) for c in range(first_col, first_col + limit_cols)]
            row_labels = [str(r) for r in range(first_row, first_row + limit_rows)]

            return {
                "headers": headers,
                "row_labels": row_labels,
                "values": vals,
                "total_rows": num_rows,
                "total_cols": num_cols
            }
        return None
    except Exception:
        return None

def get_workbook_context() -> Dict[str, Any]:
    """
    Aggregates workbook name, sheet name, selected range address,
    and a list of all sheets in the current active workbook.
    """

    book = get_active_workbook()


    if book is None:
        return {
            "workbook_name": None,
            "sheet_name": None,
            "selected_range": None,
            "available_sheets": [],
            "selection_data": None
        }


    sheet_list = []
    try:

        sheet_list = get_sheets()
    except Exception:

        pass


    return {
        "workbook_name": book.name,
        "sheet_name": get_active_sheet_name(),
        "selected_range": get_selected_range(),
        "available_sheets": sheet_list,
        "selection_data": get_selected_range_data()
    }