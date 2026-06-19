
import xlwings as xw

from typing import List, Optional

from excel.excel_connection import excel_conn

def get_active_workbook() -> Optional[xw.Book]:
    """
    Returns the currently active workbook object.
    Returns None if no workbook is currently open.
    """

    app = excel_conn.get_excel_app()
    try:

        if len(app.books) > 0:

            return app.books.active

        return None
    except Exception:

        return None

def get_workbooks() -> List[str]:
    """
    Returns a list of names of all currently open workbooks.
    """

    app = excel_conn.get_excel_app()

    return [book.name for book in app.books]

def open_workbook(path: str) -> xw.Book:
    """
    Opens an existing Excel workbook at the specified path and activates it.
    """

    app = excel_conn.get_excel_app()

    book = app.books.open(path)

    book.activate()

    return book

def create_workbook() -> xw.Book:
    """
    Creates a new empty Excel workbook and activates it.
    """

    app = excel_conn.get_excel_app()

    book = app.books.add()

    book.activate()

    return book

def save_workbook() -> None:
    """
    Saves the active workbook. Raises error if no workbook is open.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook found to save.")

    book.save()

def save_workbook_as(path: str) -> None:
    """
    Saves the active workbook with a new path. Raises error if no workbook is open.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook found to save as.")

    book.save(path)

def close_workbook() -> None:
    """
    Closes the active workbook. Raises error if no workbook is open.
    """

    book = get_active_workbook()

    if book is None:

        raise ValueError("No active workbook found to close.")

    book.close()