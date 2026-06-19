
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional
from schemas.actions import ExcelAction


class WorkbookContext(BaseModel):

    workbook_name: Optional[str] = Field(None, description="The name of the currently active workbook")

    sheet_name: Optional[str] = Field(None, description="The name of the currently active sheet")

    selected_range: Optional[str] = Field(None, description="The range address currently selected by the user, e.g. A1:B5")

    available_sheets: List[str] = Field(default_factory=list, description="List of all worksheet names in the workbook")

    selection_data: Optional[Dict[str, Any]] = Field(None, description="Data within the selected range for grid preview")


class ChatRequest(BaseModel):

    message: str = Field(..., description="The natural language command to execute on Excel")


class ActionPreview(BaseModel):

    action: ExcelAction = Field(..., description="The structured Pydantic action schema")

    is_valid: bool = Field(..., description="Indicates if the action is valid to execute")

    error_message: Optional[str] = Field(None, description="Detailed validation error if is_valid is False")


class ChatResponse(BaseModel):

    message: str = Field(..., description="The original user query")

    plan: List[ActionPreview] = Field(..., description="The generated execution plan with validation status")

    all_valid: bool = Field(..., description="True if all actions in the plan are valid")


class ExecuteRequest(BaseModel):

    actions: List[ExcelAction] = Field(..., description="The list of approved Excel actions to run")


class ActionResult(BaseModel):

    action_type: str = Field(..., description="The type of action executed")

    success: bool = Field(..., description="True if the action was executed successfully")

    error: Optional[str] = Field(None, description="Error message if execution failed")

    data: Optional[Any] = Field(None, description="Any returned data or cell values from the operation")

    action_id: Optional[str] = Field(None, description="The unique ID of the action instance")


class ExecuteResponse(BaseModel):

    results: List[ActionResult] = Field(..., description="List of results for each executed action")

    success_count: int = Field(..., description="Number of actions executed successfully")

    failure_count: int = Field(..., description="Number of actions that failed execution")


class HealthResponse(BaseModel):

    status: str = Field(..., description="Status of the FastAPI application service")

    excel_running: bool = Field(..., description="True if Excel is running and available on the system")