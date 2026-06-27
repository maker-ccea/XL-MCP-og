
from typing import List, Dict, Any

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
    SortRangeAction,
)

from ai.parser import parse_natural_language

import logging


logger = logging.getLogger("ai_planner")


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
    "sort_range": SortRangeAction,
}

def generate_action_plan(message: str) -> List[ExcelAction]:
    """
    Parses a natural language instruction and generates a sequence of validated Pydantic Action models.
    """

    raw_actions = parse_natural_language(message)


    action_plan: List[ExcelAction] = []


    for act_dict in raw_actions:

        action_name = act_dict.get("action")


        if action_name in ACTION_MODEL_MAP:
            try:

                model_class = ACTION_MODEL_MAP[action_name]
                action_obj = model_class(**act_dict)

                action_plan.append(action_obj)
            except Exception as e:

                logger.error(f"Action validation failed for dictionary data '{act_dict}': {e}")
        else:

            logger.warning(f"Skipping unsupported action dictionary key: '{action_name}'")


    return action_plan