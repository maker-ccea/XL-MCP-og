
from typing import List, Any

from schemas.actions import ExcelAction
from schemas.responses import ActionResult

from excel.excel_connection import excel_conn

import excel.workbook as wb
import excel.worksheet as ws
import excel.cells as cells
import excel.formulas as formulas
import excel.formatting as formatting
import excel.charts as charts

from state.excel_state import state_manager

import logging
import uuid

from executor.undo_manager import undo_manager


logger = logging.getLogger("action_executor")

def execute_action(action: ExcelAction) -> ActionResult:
    """
    Executes a single structured Excel action, registers it with the state manager,
    and returns an ActionResult indicating success or failure.
    """

    excel_conn.connect_excel()


    if not action.id:
        action.id = str(uuid.uuid4())


    action_type = action.action

    success = False
    error_msg = None
    returned_data = None


    target_range = None
    if action_type in ["write_cell", "apply_formula", "remove_formula"]:
        target_range = getattr(action, "cell", None)
    elif action_type in ["write_range", "clear_cells", "fill_formula", "set_bold", "set_italic", "set_font_size", "set_font_color", "set_background_color", "sort_range"]:
        target_range = getattr(action, "range", None)

    if target_range:
        undo_manager.prepare_undo(action.id, target_range)

    try:

        if action_type == "open_workbook":

            wb.open_workbook(action.path)
            success = True

        elif action_type == "create_workbook":

            wb.create_workbook()
            success = True

        elif action_type == "save_workbook":

            wb.save_workbook()
            success = True

        elif action_type == "save_workbook_as":

            wb.save_workbook_as(action.path)
            success = True

        elif action_type == "close_workbook":

            wb.close_workbook()
            success = True

        elif action_type == "create_sheet":

            ws.create_sheet(action.name)
            success = True

        elif action_type == "rename_sheet":

            ws.rename_sheet(action.old_name, action.new_name)
            success = True

        elif action_type == "delete_sheet":

            ws.delete_sheet(action.name)
            success = True

        elif action_type == "activate_sheet":

            ws.activate_sheet(action.name)
            success = True

        elif action_type == "write_cell":

            cells.write_cell(action.cell, action.value)
            success = True

        elif action_type == "write_range":

            cells.write_range(action.range, action.data)
            success = True

        elif action_type == "clear_cells":

            cells.clear_cells(action.range)
            success = True

        elif action_type == "apply_formula":

            formulas.apply_formula(action.cell, action.formula)
            success = True

        elif action_type == "fill_formula":

            formulas.fill_formula(action.range, action.formula)
            success = True

        elif action_type == "remove_formula":

            formulas.remove_formula(action.cell)
            success = True

        elif action_type == "set_bold":

            formatting.set_bold(action.range, getattr(action, "bold", True))
            success = True

        elif action_type == "set_italic":

            formatting.set_italic(action.range, getattr(action, "italic", True))
            success = True

        elif action_type == "set_font_size":

            formatting.set_font_size(action.range, action.size)
            success = True

        elif action_type == "set_font_color":

            formatting.set_font_color(action.range, action.color)
            success = True

        elif action_type == "set_background_color":

            formatting.set_background_color(action.range, action.color)
            success = True

        elif action_type == "auto_fit_columns":

            formatting.auto_fit_columns(action.range)
            success = True

        elif action_type == "create_chart":
            chart_name = charts.create_chart(
                data_range=action.data_range,
                chart_type=getattr(action, "chart_type", "column"),
                title=getattr(action, "title", None),
                sheet_name=getattr(action, "sheet", None),
                left=getattr(action, "left", None),
                top=getattr(action, "top", None),
                width=getattr(action, "width", 375),
                height=getattr(action, "height", 225),
            )
            returned_data = {"chart_name": chart_name}
            success = True

        elif action_type == "delete_chart":
            charts.delete_chart(
                name=action.name,
                sheet_name=getattr(action, "sheet", None),
            )
            success = True

        elif action_type == "update_chart_title":
            charts.update_chart_title(
                name=action.name,
                title=action.title,
                sheet_name=getattr(action, "sheet", None),
            )
            success = True

        elif action_type == "sort_range":
            cells.sort_range(
                range_address=action.range,
                key_column=action.key_column,
                ascending=getattr(action, "ascending", True),
                has_headers=getattr(action, "has_headers", True),
            )
            success = True

        else:

            raise ValueError(f"Unknown action type: '{action_type}'")


        state_manager.update_state()


        state_manager.log_action({
            "action": action.model_dump(),
            "status": "success"
        })

    except Exception as e:

        logger.error(f"Failed to execute action '{action_type}': {e}")

        success = False

        error_msg = str(e)


        state_manager.log_action({
            "action": action.model_dump(),
            "status": "failed",
            "error": error_msg
        })


    return ActionResult(
        action_type=action_type,
        success=success,
        error=error_msg,
        data=returned_data,
        action_id=action.id
    )

def execute_action_plan(actions: List[ExcelAction]) -> List[ActionResult]:
    """
    Executes a sequence of Excel actions in order. Returns list of ActionResults.
    """

    results = []

    for action in actions:

        res = execute_action(action)
        results.append(res)



    return results