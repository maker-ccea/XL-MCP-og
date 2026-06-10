# Import xlwings for Excel API access
import xlwings as xw
# Import List and Optional types from typing
from typing import List, Optional
# Import the connection manager to make sure Excel is running
from excel.excel_connection import excel_conn

def get_active_workbook() -> Optional[xw.Book]:
    """
    Returns the currently active workbook object.
    Returns None if no workbook is currently open.
    """
    # Verify/establish connection to Excel application instance
    app = excel_conn.get_excel_app()
    try:
        # Check if there are any open books in the Excel application instance
        if len(app.books) > 0:
            # Return the active workbook
            return app.books.active
        # If no workbooks are open, return None
        return None
    except Exception:
        # Return None on any failure (e.g. no active book)
        return None

def get_workbooks() -> List[str]:
    """
    Returns a list of names of all currently open workbooks.
    """
    # Establish connection to Excel app
    app = excel_conn.get_excel_app()
    # List comprehension to extract names of all books in the app.books collection
    return [book.name for book in app.books]

def open_workbook(path: str) -> xw.Book:
    """
    Opens an existing Excel workbook at the specified path and activates it.
    """
    # Ensure Excel connection is initialized
    app = excel_conn.get_excel_app()
    # Use xlwings Books collection to open the file at the given path
    book = app.books.open(path)
    # Activate the workbook to make it the focus
    book.activate()
    # Return the opened Book object
    return book

def create_workbook() -> xw.Book:
    """
    Creates a new empty Excel workbook and activates it.
    """
    # Ensure Excel connection is initialized
    app = excel_conn.get_excel_app()
    # Use app.books.add() to create a new workbook
    book = app.books.add()
    # Activate the newly created workbook
    book.activate()
    # Return the Book object
    return book

def save_workbook() -> None:
    """
    Saves the active workbook. Raises error if no workbook is open.
    """
    # Retrieve the currently active workbook
    book = get_active_workbook()
    # Check if a workbook exists
    if book is None:
        # Raise an exception if no workbook is active to be saved
        raise ValueError("No active workbook found to save.")
    # Invoke the save method on the Book object
    book.save()

def save_workbook_as(path: str) -> None:
    """
    Saves the active workbook with a new path. Raises error if no workbook is open.
    """
    # Retrieve the currently active workbook
    book = get_active_workbook()
    # Check if a workbook exists
    if book is None:
        # Raise an exception if no workbook is active to be saved
        raise ValueError("No active workbook found to save as.")
    # Invoke the save method passing the new path parameter
    book.save(path)

def close_workbook() -> None:
    """
    Closes the active workbook. Raises error if no workbook is open.
    """
    # Retrieve the currently active workbook
    book = get_active_workbook()
    # Check if a workbook exists
    if book is None:
        # Raise an exception if no workbook is active to be closed
        raise ValueError("No active workbook found to close.")
    # Close the workbook reference
    book.close()
