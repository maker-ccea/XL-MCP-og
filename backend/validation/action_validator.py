# Import typing helper
from typing import Tuple, Optional
# Import action schemas Union
from schemas.actions import ExcelAction
# Import validators
from validation.range_validator import validate_range_format
from validation.formula_validator import validate_formula_safety
# Import active context helpers
from excel.workbook import get_active_workbook
from excel.worksheet import get_sheets
# Import logging
import logging

# Configure logger for the validation layer
logger = logging.getLogger("action_validator")

def validate_action(action: ExcelAction) -> Tuple[bool, Optional[str]]:
    """
    Validates the structure and semantic safety of an Excel action.
    Returns (True, None) if valid, or (False, "error message") if invalid.
    """
    try:
        # 1. Check if the action requires an open workbook.
        # Most actions except opening or creating a workbook require an active workbook.
        non_workbook_actions = ["open_workbook", "create_workbook"]
        if action.action not in non_workbook_actions:
            # Check if active workbook is available
            if get_active_workbook() is None:
                # Return validation failure if no workbook is open
                return False, "No active workbook is open. Please create or open a workbook first."

        # 2. Extract and validate ranges/cells if present in action attributes
        # Many cell, formula, and formatting actions contain a 'cell' attribute
        if hasattr(action, "cell"):
            cell_address = getattr(action, "cell")
            # Verify the cell format is correct (e.g. A1)
            if not validate_range_format(cell_address):
                return False, f"Invalid cell format: '{cell_address}'."

        # Many actions contain a 'range' attribute (ranges, styling, autofit)
        if hasattr(action, "range"):
            range_address = getattr(action, "range")
            # Verify the range format is correct (e.g. A1:C10)
            if not validate_range_format(range_address):
                return False, f"Invalid range format: '{range_address}'."

        # 3. Extract and validate formulas if present
        if hasattr(action, "formula"):
            formula_string = getattr(action, "formula")
            # Check if the formula starts with '=' and is secure/safe
            if not validate_formula_safety(formula_string):
                return False, f"Formula is unsafe or invalid: '{formula_string}'."

        # 4. Check sheet existence for sheet operations
        if action.action in ["rename_sheet", "delete_sheet", "activate_sheet"]:
            # Retrieve currently open sheets
            available_sheets = get_sheets()
            
            # For rename, verify the source sheet exists
            if action.action == "rename_sheet":
                source_sheet = getattr(action, "old_name")
                if source_sheet not in available_sheets:
                    return False, f"Source sheet '{source_sheet}' does not exist in workbook."
            
            # For delete or activate, verify the sheet exists
            if action.action in ["delete_sheet", "activate_sheet"]:
                target_sheet = getattr(action, "name")
                if target_sheet not in available_sheets:
                    return False, f"Target sheet '{target_sheet}' does not exist in workbook."

        # If all checks pass, return success
        return True, None

    except Exception as e:
        # Log the unexpected error during validation
        logger.error(f"Error during action validation: {e}")
        # Return validation failure with the exception detail
        return False, f"Validation system error: {str(e)}"
