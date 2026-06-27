
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

def sort_range(range_address: str, key_column: int, ascending: bool = True, has_headers: bool = True) -> None:
    """
    Sorts the data rows within a specified range on the active sheet by a key column.
    """
    sheet = get_active_sheet()
    rng = sheet.range(range_address)
    values = rng.value

    if not values:
        return

    # If it is a 1D list (e.g. single column or single row), wrap it or handle it simply
    if not isinstance(values, list):
        return
    if len(values) > 0 and not isinstance(values[0], list):
        # 1D row or column
        values = [[item] for item in values]

    if has_headers:
        headers = values[0]
        data_rows = values[1:]
    else:
        headers = None
        data_rows = values

    col_idx = key_column - 1

    def get_sort_key(row):
        if col_idx < len(row):
            val = row[col_idx]
            if val is None:
                return (1, "")
            # Return tuple to keep numbers sorted properly and compare strings safely
            if isinstance(val, (int, float)):
                return (0, val)
            return (0, str(val))
        return (2, "")

    data_rows.sort(key=get_sort_key, reverse=not ascending)

    sorted_values = []
    if headers:
        sorted_values.append(headers)
    sorted_values.extend(data_rows)

    rng.value = sorted_values