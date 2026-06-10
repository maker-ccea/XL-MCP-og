# Import Dict, Any and List from typing
from typing import Dict, Any, List
# Import context helpers to fetch the latest values from Excel
from excel.context import get_workbook_context
# Import logging to log state transitions
import logging

# Configure local logger for tracking state updates
logger = logging.getLogger("excel_state")

class ExcelStateManager:
    """
    Tracks and updates the current state of Excel (active workbook, sheet, selection).
    """
    def __init__(self) -> None:
        # Cache dictionary storing the current Excel state attributes
        self._current_state: Dict[str, Any] = {
            "workbook": "",
            "sheet": "",
            "selection": ""
        }
        # List to track the historical log of executed actions
        self._history: List[Dict[str, Any]] = []

    def get_current_state(self) -> Dict[str, Any]:
        """
        Returns the cached state. Calls update_state first to ensure values are fresh.
        """
        # Refresh the cache before returning
        self.update_state()
        # Return the state dictionary
        return self._current_state

    def update_state(self) -> Dict[str, Any]:
        """
        Queries Excel and synchronizes the local cache with the active environment state.
        """
        try:
            # Query Excel connection context metadata
            context = get_workbook_context()
            
            # Map context fields to the state cache structure
            self._current_state["workbook"] = context["workbook_name"] or ""
            self._current_state["sheet"] = context["sheet_name"] or ""
            self._current_state["selection"] = context["selected_range"] or ""
        except Exception as e:
            # Log any errors when synchronizing state
            logger.error(f"Error updating excel state: {e}")
            
        # Return the updated state cache
        return self._current_state

    def track_selection_changes(self) -> bool:
        """
        Checks if the selection has changed relative to the cache.
        Returns True if a change is detected.
        """
        # Save reference to previous cached selection
        old_selection = self._current_state.get("selection", "")
        # Refresh state from active Excel session
        self.update_state()
        # Compare and return True if current selection differs from old selection
        return old_selection != self._current_state.get("selection", "")

    def log_action(self, action_dict: Dict[str, Any]) -> None:
        """
        Logs a successfully executed action to the execution history array.
        """
        # Append the action payload to the history log
        self._history.append(action_dict)

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Returns the list of actions that have been executed so far.
        """
        # Return the action history list
        return self._history

# Global state manager instance
state_manager = ExcelStateManager()
