import logging
from typing import Dict, Any, List, Optional
import xlwings as xw
from excel.excel_connection import excel_conn
from excel.worksheet import get_active_sheet

logger = logging.getLogger("undo_manager")

class UndoSnapshot:
    def __init__(self, sheet_name: str, range_address: str):
        self.sheet_name = sheet_name
        self.range_address = range_address
        self.values: Any = None
        self.formulas: Any = None
        self.bold: Any = None
        self.italic: Any = None
        self.font_size: Any = None
        self.font_color: Any = None
        self.background_color: Any = None

    def capture(self) -> None:
        try:
            sheet = get_active_sheet()
            rng = sheet.range(self.range_address)
            self.values = rng.value
            self.formulas = rng.formula


            self.bold = rng.api.Font.Bold if hasattr(rng.api, "Font") else None
            self.italic = rng.api.Font.Italic if hasattr(rng.api, "Font") else None
            self.font_size = rng.api.Font.Size if hasattr(rng.api, "Font") else None
            self.font_color = rng.api.Font.Color if hasattr(rng.api, "Font") else None


            if hasattr(rng.api, "Interior"):
                self.background_color = rng.api.Interior.Color
        except Exception as e:
            logger.error(f"Failed to capture undo snapshot for range {self.range_address}: {e}")

    def restore(self) -> None:
        try:
            excel_conn.connect_excel()
            sheet = get_active_sheet()
            rng = sheet.range(self.range_address)


            if self.formulas is not None:
                rng.formula = self.formulas
            else:
                rng.value = self.values


            if hasattr(rng.api, "Font"):
                if self.bold is not None:
                    rng.api.Font.Bold = self.bold
                if self.italic is not None:
                    rng.api.Font.Italic = self.italic
                if self.font_size is not None:
                    rng.api.Font.Size = self.font_size
                if self.font_color is not None:
                    rng.api.Font.Color = self.font_color

            if hasattr(rng.api, "Interior") and self.background_color is not None:
                rng.api.Interior.Color = self.background_color

            logger.info(f"Successfully restored snapshot for {self.range_address} on sheet {self.sheet_name}")
        except Exception as e:
            logger.error(f"Failed to restore undo snapshot for range {self.range_address}: {e}")

class UndoManager:
    def __init__(self):

        self.snapshots: Dict[str, UndoSnapshot] = {}

        self.history_stack: List[str] = []

    def prepare_undo(self, action_id: str, range_address: str) -> None:
        try:
            sheet = get_active_sheet()
            snapshot = UndoSnapshot(sheet.name, range_address)
            snapshot.capture()
            self.snapshots[action_id] = snapshot
            self.history_stack.append(action_id)
            logger.info(f"Registered undo snapshot for action {action_id} on range {range_address}")
        except Exception as e:
            logger.error(f"Could not prepare undo snapshot: {e}")

    def trigger_undo(self, action_id: str) -> bool:
        snapshot = self.snapshots.get(action_id)
        if snapshot:
            snapshot.restore()

            del self.snapshots[action_id]
            if action_id in self.history_stack:
                self.history_stack.remove(action_id)
            return True
        return False

undo_manager = UndoManager()