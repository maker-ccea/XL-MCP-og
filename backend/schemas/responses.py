# Import Pydantic BaseModel and typing helpers
from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional
from schemas.actions import ExcelAction

# Schema for the workbook/worksheet context
class WorkbookContext(BaseModel):
    # Name of the active workbook, if any is open
    workbook_name: Optional[str] = Field(None, description="The name of the currently active workbook")
    # Name of the active worksheet
    sheet_name: Optional[str] = Field(None, description="The name of the currently active sheet")
    # Address of the currently selected cell range
    selected_range: Optional[str] = Field(None, description="The range address currently selected by the user, e.g. A1:B5")
    # List of all available sheet names in the active workbook
    available_sheets: List[str] = Field(default_factory=list, description="List of all worksheet names in the workbook")

# Schema for the request structure of the /chat endpoint
class ChatRequest(BaseModel):
    # User natural language instruction/question
    message: str = Field(..., description="The natural language command to execute on Excel")

# Schema for previewing a validated action before execution
class ActionPreview(BaseModel):
    # The action that is planned to be run
    action: ExcelAction = Field(..., description="The structured Pydantic action schema")
    # Whether this action successfully passed the validation layer
    is_valid: bool = Field(..., description="Indicates if the action is valid to execute")
    # Any validation errors associated with this action
    error_message: Optional[str] = Field(None, description="Detailed validation error if is_valid is False")

# Schema for the response structure of the /chat endpoint
class ChatResponse(BaseModel):
    # Original user message
    message: str = Field(..., description="The original user query")
    # List of action previews mapping out the planned execution steps
    plan: List[ActionPreview] = Field(..., description="The generated execution plan with validation status")
    # Quick boolean to show if the entire plan is safe/valid to execute
    all_valid: bool = Field(..., description="True if all actions in the plan are valid")

# Schema for the request structure of the /execute endpoint
class ExecuteRequest(BaseModel):
    # List of actions the client approved to execute
    actions: List[ExcelAction] = Field(..., description="The list of approved Excel actions to run")

# Schema for the execution result of a single action
class ActionResult(BaseModel):
    # Action name that was run
    action_type: str = Field(..., description="The type of action executed")
    # Flag showing if the action execution was successful
    success: bool = Field(..., description="True if the action was executed successfully")
    # Error message if the action execution failed
    error: Optional[str] = Field(None, description="Error message if execution failed")
    # Return data from the action execution (e.g. read values)
    data: Optional[Any] = Field(None, description="Any returned data or cell values from the operation")

# Schema for the response structure of the /execute endpoint
class ExecuteResponse(BaseModel):
    # List of results for each action in the executed plan
    results: List[ActionResult] = Field(..., description="List of results for each executed action")
    # Total count of successful operations
    success_count: int = Field(..., description="Number of actions executed successfully")
    # Total count of failed operations
    failure_count: int = Field(..., description="Number of actions that failed execution")

# Schema for /health endpoint response
class HealthResponse(BaseModel):
    # API health status, e.g. "ok" or "healthy"
    status: str = Field(..., description="Status of the FastAPI application service")
    # Flag showing if Excel application is currently running
    excel_running: bool = Field(..., description="True if Excel is running and available on the system")
