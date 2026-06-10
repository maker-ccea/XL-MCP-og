# Import typing List and Any
from typing import List, Any
# Import action schemas and response objects
from schemas.actions import ExcelAction
from schemas.responses import ActionResult
# Import Excel connection object
from excel.excel_connection import excel_conn
# Import Excel operation modules
import excel.workbook as wb
import excel.worksheet as ws
import excel.cells as cells
import excel.formulas as formulas
import excel.formatting as formatting
import excel.charts as charts
# Import global state manager to track executed actions and state updates
from state.excel_state import state_manager
# Import logging
import logging

# Configure logger for tracking action execution
logger = logging.getLogger("action_executor")

def execute_action(action: ExcelAction) -> ActionResult:
    """
    Executes a single structured Excel action, registers it with the state manager,
    and returns an ActionResult indicating success or failure.
    """
    # Ensure Excel application connection is active
    excel_conn.connect_excel()
    
    # Store type name of the current action
    action_type = action.action
    # Initialize variables for execution results
    success = False
    error_msg = None
    returned_data = None

    try:
        # Match the action type to the corresponding helper functions
        if action_type == "open_workbook":
            # Call open workbook helper
            wb.open_workbook(action.path)
            success = True
            
        elif action_type == "create_workbook":
            # Call create workbook helper
            wb.create_workbook()
            success = True
            
        elif action_type == "save_workbook":
            # Call save workbook helper
            wb.save_workbook()
            success = True
            
        elif action_type == "save_workbook_as":
            # Call save workbook as helper
            wb.save_workbook_as(action.path)
            success = True
            
        elif action_type == "close_workbook":
            # Call close workbook helper
            wb.close_workbook()
            success = True
            
        elif action_type == "create_sheet":
            # Call create sheet helper
            ws.create_sheet(action.name)
            success = True
            
        elif action_type == "rename_sheet":
            # Call rename sheet helper
            ws.rename_sheet(action.old_name, action.new_name)
            success = True
            
        elif action_type == "delete_sheet":
            # Call delete sheet helper
            ws.delete_sheet(action.name)
            success = True
            
        elif action_type == "activate_sheet":
            # Call activate sheet helper
            ws.activate_sheet(action.name)
            success = True
            
        elif action_type == "write_cell":
            # Call write cell helper
            cells.write_cell(action.cell, action.value)
            success = True
            
        elif action_type == "write_range":
            # Call write range helper
            cells.write_range(action.range, action.data)
            success = True
            
        elif action_type == "clear_cells":
            # Call clear cells helper
            cells.clear_cells(action.range)
            success = True
            
        elif action_type == "apply_formula":
            # Call apply formula helper
            formulas.apply_formula(action.cell, action.formula)
            success = True
            
        elif action_type == "fill_formula":
            # Call fill formula helper
            formulas.fill_formula(action.range, action.formula)
            success = True
            
        elif action_type == "remove_formula":
            # Call remove formula helper
            formulas.remove_formula(action.cell)
            success = True
            
        elif action_type == "set_bold":
            # Call set bold helper
            formatting.set_bold(action.range, getattr(action, "bold", True))
            success = True
            
        elif action_type == "set_italic":
            # Call set italic helper
            formatting.set_italic(action.range, getattr(action, "italic", True))
            success = True
            
        elif action_type == "set_font_size":
            # Call set font size helper
            formatting.set_font_size(action.range, action.size)
            success = True
            
        elif action_type == "set_font_color":
            # Call set font color helper
            formatting.set_font_color(action.range, action.color)
            success = True
            
        elif action_type == "set_background_color":
            # Call set background color helper
            formatting.set_background_color(action.range, action.color)
            success = True
            
        elif action_type == "auto_fit_columns":
            # Call auto fit helper
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

        else:
            # Handle unknown action types
            raise ValueError(f"Unknown action type: '{action_type}'")

        # If operation succeeded, synchronize local cache state from active Excel context
        state_manager.update_state()
        
        # Log successful action execution in history
        state_manager.log_action({
            "action": action.model_dump(),
            "status": "success"
        })

    except Exception as e:
        # Log any exceptions raised during Excel execution
        logger.error(f"Failed to execute action '{action_type}': {e}")
        # Mark success flag as False
        success = False
        # Save error message string
        error_msg = str(e)
        
        # Log failed action execution in history
        state_manager.log_action({
            "action": action.model_dump(),
            "status": "failed",
            "error": error_msg
        })

    # Return the structured ActionResult response
    return ActionResult(
        action_type=action_type,
        success=success,
        error=error_msg,
        data=returned_data
    )

def execute_action_plan(actions: List[ExcelAction]) -> List[ActionResult]:
    """
    Executes a sequence of Excel actions in order. Returns list of ActionResults.
    """
    # Initialize a list to hold the execution result of each action
    results = []
    # Loop over all actions in the plan
    for action in actions:
        # Execute the action and append result
        res = execute_action(action)
        results.append(res)
        # If an action fails, we might want to stop the sequence depending on application logic.
        # But here we will continue processing the list.
    # Return list of results
    return results
