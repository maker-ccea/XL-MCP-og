
from typing import Dict, Any, List

from excel.context import get_workbook_context

import logging

from state.graph_db import graph_db


logger = logging.getLogger("excel_state")

class ExcelStateManager:
    """
    Tracks and updates the current state of Excel (active workbook, sheet, selection).
    """
    def __init__(self) -> None:

        self._current_state: Dict[str, Any] = {
            "workbook": "",
            "sheet": "",
            "selection": "",
            "used_range": ""
        }

        self._history: List[Dict[str, Any]] = []

    def get_current_state(self) -> Dict[str, Any]:
        """
        Returns the cached state. Calls update_state first to ensure values are fresh.
        """

        self.update_state()

        return self._current_state

    def update_state(self) -> Dict[str, Any]:
        """
        Queries Excel and synchronizes the local cache with the active environment state.
        """
        try:

            context = get_workbook_context()


            wb_name = context["workbook_name"] or ""
            sheet_name = context["sheet_name"] or ""
            selection = context["selected_range"] or ""
            used_range = context["used_range"] or ""

            self._current_state["workbook"] = wb_name
            self._current_state["sheet"] = sheet_name
            self._current_state["selection"] = selection
            self._current_state["used_range"] = used_range


            if wb_name:
                graph_db.add_node(wb_name, "Workbook", {"name": wb_name})
                if sheet_name:
                    sheet_id = f"{wb_name}::{sheet_name}"
                    graph_db.add_node(sheet_id, "Sheet", {"name": sheet_name, "workbook": wb_name})
                    graph_db.add_edge(wb_name, sheet_id, "HAS_SHEET")
                    if selection:
                        range_id = f"{sheet_id}::{selection}"
                        graph_db.add_node(range_id, "Range", {"address": selection, "sheet": sheet_name})
                        graph_db.add_edge(sheet_id, range_id, "HAS_RANGE")

        except Exception as e:

            logger.error(f"Error updating excel state: {e}")


        return self._current_state

    def track_selection_changes(self) -> bool:
        """
        Checks if the selection has changed relative to the cache.
        Returns True if a change is detected.
        """

        old_selection = self._current_state.get("selection", "")

        self.update_state()

        return old_selection != self._current_state.get("selection", "")

    def log_action(self, action_dict: Dict[str, Any]) -> None:
        """
        Logs a successfully executed action to the execution history array.
        """
        import datetime
        if "timestamp" not in action_dict:
            action_dict["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
        self._history.append(action_dict)


        try:
            action = action_dict.get("action", {})
            action_id = action.get("id")
            action_type = action.get("action")
            if action_id and action_type:

                graph_db.add_node(action_id, "Action", action)


                wb_name = self._current_state.get("workbook")
                sheet_name = self._current_state.get("sheet")
                if wb_name and sheet_name:
                    sheet_id = f"{wb_name}::{sheet_name}"
                    graph_db.add_edge(action_id, sheet_id, "IN_SHEET")


                    target_range = action.get("range") or action.get("cell")
                    if target_range:
                        range_id = f"{sheet_id}::{target_range}"

                        graph_db.add_node(range_id, "Range", {"address": target_range, "sheet": sheet_name})
                        graph_db.add_edge(action_id, range_id, "MODIFIED_RANGE")
        except Exception as e:
            logger.error(f"Error logging action to graph: {e}")

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Returns the list of actions that have been executed so far.
        """

        return self._history


state_manager = ExcelStateManager()