# Import typing helpers
from typing import List, Dict, Any
# Import Pydantic parser schemas
from schemas.actions import (
    ExcelAction,
    OpenWorkbookAction,
    CreateWorkbookAction,
    SaveWorkbookAction,
    SaveWorkbookAsAction,
    CloseWorkbookAction,
    CreateSheetAction,
    RenameSheetAction,
    DeleteSheetAction,
    ActivateSheetAction,
    WriteCellAction,
    WriteRangeAction,
    ClearCellsAction,
    ApplyFormulaAction,
    FillFormulaAction,
    RemoveFormulaAction,
    SetBoldAction,
    SetItalicAction,
    SetFontSizeAction,
    SetFontColorAction,
    SetBackgroundColorAction,
    AutoFitColumnsAction,
    CreateChartAction,
    DeleteChartAction,
    UpdateChartTitleAction,
)
# Import natural language parser function
from ai.parser import parse_natural_language
# Import logger
import logging

# Configure local logger for planning module
logger = logging.getLogger("ai_planner")

# Dictionary mapping action action names to their corresponding Pydantic model classes
ACTION_MODEL_MAP = {
    "open_workbook": OpenWorkbookAction,
    "create_workbook": CreateWorkbookAction,
    "save_workbook": SaveWorkbookAction,
    "save_workbook_as": SaveWorkbookAsAction,
    "close_workbook": CloseWorkbookAction,
    "create_sheet": CreateSheetAction,
    "rename_sheet": RenameSheetAction,
    "delete_sheet": DeleteSheetAction,
    "activate_sheet": ActivateSheetAction,
    "write_cell": WriteCellAction,
    "write_range": WriteRangeAction,
    "clear_cells": ClearCellsAction,
    "apply_formula": ApplyFormulaAction,
    "fill_formula": FillFormulaAction,
    "remove_formula": RemoveFormulaAction,
    "set_bold": SetBoldAction,
    "set_italic": SetItalicAction,
    "set_font_size": SetFontSizeAction,
    "set_font_color": SetFontColorAction,
    "set_background_color": SetBackgroundColorAction,
    "auto_fit_columns": AutoFitColumnsAction,
    "create_chart": CreateChartAction,
    "delete_chart": DeleteChartAction,
    "update_chart_title": UpdateChartTitleAction,
}

def generate_action_plan(message: str) -> List[ExcelAction]:
    """
    Parses a natural language instruction and generates a sequence of validated Pydantic Action models.
    """
    # 1. Parse natural language message to list of dictionaries
    raw_actions = parse_natural_language(message)
    
    # Initialize a list to hold the validated ExcelAction Pydantic objects
    action_plan: List[ExcelAction] = []
    
    # 2. Map and validate each action dictionary using Pydantic models
    for act_dict in raw_actions:
        # Extract the action name/type
        action_name = act_dict.get("action")
        
        # Check if the action name is recognized and has a Pydantic model mapped
        if action_name in ACTION_MODEL_MAP:
            try:
                # Instantiate the Pydantic model class passing the dictionary items as kwargs
                model_class = ACTION_MODEL_MAP[action_name]
                action_obj = model_class(**act_dict)
                # Append the validated object to the plan list
                action_plan.append(action_obj)
            except Exception as e:
                # Log any validation exceptions raised when parsing the dict to Pydantic model
                logger.error(f"Action validation failed for dictionary data '{act_dict}': {e}")
        else:
            # Log any unsupported/unknown action key found
            logger.warning(f"Skipping unsupported action dictionary key: '{action_name}'")
            
    # Return the generated plan of strongly-typed Pydantic objects
    return action_plan
