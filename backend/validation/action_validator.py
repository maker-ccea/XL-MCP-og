
from typing import Tuple, Optional

from schemas.actions import ExcelAction

from validation.range_validator import validate_range_format
from validation.formula_validator import validate_formula_safety

from excel.workbook import get_active_workbook
from excel.worksheet import get_sheets

import logging


logger = logging.getLogger("action_validator")

def validate_action(action: ExcelAction) -> Tuple[bool, Optional[str]]:
    """
    Validates the structure and semantic safety of an Excel action.
    Returns (True, None) if valid, or (False, "error message") if invalid.
    """
    try:


        non_workbook_actions = ["open_workbook", "create_workbook"]
        if action.action not in non_workbook_actions:

            if get_active_workbook() is None:

                return False, "No active workbook is open. Please create or open a workbook first."



        if hasattr(action, "cell"):
            cell_address = getattr(action, "cell")

            if not validate_range_format(cell_address):
                return False, f"Invalid cell format: '{cell_address}'."


        if hasattr(action, "range"):
            range_address = getattr(action, "range")

            if not validate_range_format(range_address):
                return False, f"Invalid range format: '{range_address}'."


        if hasattr(action, "formula"):
            formula_string = getattr(action, "formula")

            if not validate_formula_safety(formula_string):
                return False, f"Formula is unsafe or invalid: '{formula_string}'."


        if action.action in ["rename_sheet", "delete_sheet", "activate_sheet"]:

            available_sheets = get_sheets()


            if action.action == "rename_sheet":
                source_sheet = getattr(action, "old_name")
                if source_sheet not in available_sheets:
                    return False, f"Source sheet '{source_sheet}' does not exist in workbook."


            if action.action in ["delete_sheet", "activate_sheet"]:
                target_sheet = getattr(action, "name")
                if target_sheet not in available_sheets:
                    return False, f"Target sheet '{target_sheet}' does not exist in workbook."


        return True, None

    except Exception as e:

        logger.error(f"Error during action validation: {e}")

        return False, f"Validation system error: {str(e)}"