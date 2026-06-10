# Import FastAPI routing tools, WebSocket handlers, and Exception models
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
# Import typing helpers
from typing import List, Dict, Any
# Import response schemas and action schemas
from schemas.responses import (
    ChatRequest,
    ChatResponse,
    ActionPreview,
    ExecuteRequest,
    ExecuteResponse,
    WorkbookContext,
    ActionResult,
    HealthResponse
)
from schemas.actions import ExcelAction
# Import planners, validators, executors, state managers, and connections
from ai.planner import generate_action_plan
from validation.action_validator import validate_action
from executor.action_executor import execute_action_plan
from state.excel_state import state_manager
from excel.excel_connection import excel_conn
from excel.context import get_workbook_context
# Import asyncio to manage non-blocking loops for WebSockets
import asyncio
# Import logging
import logging

# Configure logger for route operations
logger = logging.getLogger("chat_routes")

# Instantiate FastAPI Router object
router = APIRouter()

# --- HTTP Endpoints ---

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Accepts user natural language message, parses into action plan,
    validates the actions, and returns an execution preview.
    """
    try:
        # Generate the structured actions sequence from natural language
        plan = generate_action_plan(request.message)
        
        # Build action preview list
        previews = []
        all_valid = True
        
        for action in plan:
            # Validate each action using validation layer functions
            is_valid, err_msg = validate_action(action)
            # If any single action fails validation, mark entire plan validity flag to False
            if not is_valid:
                all_valid = False
            # Append formatted ActionPreview
            previews.append(
                ActionPreview(
                    action=action,
                    is_valid=is_valid,
                    error_message=err_msg
                )
            )
            
        # Return the structured preview response
        return ChatResponse(
            message=request.message,
            plan=previews,
            all_valid=all_valid
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        # Raise HTTP 500 error if operation fails unexpectedly
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", response_model=ExecuteResponse)
async def execute_endpoint(request: ExecuteRequest):
    """
    Executes the list of client-approved actions in sequence.
    """
    try:
        # Validate all actions first to prevent executing partial plans with bad actions
        for action in request.actions:
            is_valid, err_msg = validate_action(action)
            if not is_valid:
                raise HTTPException(
                    status_code=400,
                    detail=f"Action validation failed for execution: {err_msg}"
                )

        # Dispatch the plan list to action execution engine
        results = execute_action_plan(request.actions)
        
        # Count success and failure events
        successes = sum(1 for r in results if r.success)
        failures = sum(1 for r in results if not r.success)
        
        # Return structured ExecuteResponse mapping execution counts and results
        return ExecuteResponse(
            results=results,
            success_count=successes,
            failure_count=failures
        )
    except HTTPException as he:
        # Re-raise explicit HTTP validation errors
        raise he
    except Exception as e:
        logger.error(f"Error in execution endpoint: {e}")
        # Return standard Internal Server Error on exceptions
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/state", response_model=WorkbookContext)
async def get_state_endpoint():
    """
    Returns the current active workbook context.
    """
    try:
        # Retrieve workbook context from active Excel session
        context = get_workbook_context()
        # Return the values wrapped in the WorkbookContext Pydantic schema
        return WorkbookContext(
            workbook_name=context.get("workbook_name"),
            sheet_name=context.get("sheet_name"),
            selected_range=context.get("selected_range"),
            available_sheets=context.get("available_sheets", [])
        )
    except Exception as e:
        logger.error(f"Error in state endpoint: {e}")
        # Return empty context if Excel isn't connected or query fails
        return WorkbookContext(workbook_name=None, sheet_name=None, selected_range=None, available_sheets=[])

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history_endpoint():
    """
    Returns the history of all executed actions.
    """
    # Retrieve execution history log list from the state manager cache
    return state_manager.get_history()

@router.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """
    Checks backend service status and Excel connectivity status.
    """
    # Check if Microsoft Excel is running
    excel_running = excel_conn.is_excel_running()
    # Return structured status response
    return HealthResponse(
        status="healthy",
        excel_running=excel_running
    )

# --- WebSocket Live State Manager ---

class ConnectionManager:
    """
    Manages active WebSocket connections for streaming live Excel state changes.
    """
    def __init__(self):
        # List storing active client WebSocket connection handlers
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Accept client WebSocket request connection
        await websocket.accept()
        # Append connection reference to list
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        # Remove connection from list
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket client disconnected.")

    async def broadcast(self, message: dict):
        # Loop through active connections and push JSON message payloads
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Handle connection write failures silently
                pass

# Global instance of WebSocket connection manager
ws_manager = ConnectionManager()

@router.websocket("/ws/state")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that streams state updates to connected clients.
    Broadcasts state whenever selection changes in Excel.
    """
    # Accept and register client connection
    await ws_manager.connect(websocket)
    try:
        # Loop endlessly checking for state updates
        while True:
            # Check if selection changed or active sheet changed in Excel
            if state_manager.track_selection_changes():
                # Fetch fresh state cache dictionary
                current_state = state_manager.get_current_state()
                # Broadcast the state payload to client
                await ws_manager.broadcast({
                    "event": "state_changed",
                    "state": current_state
                })
            # Sleep briefly (e.g. 500ms) to prevent busy waiting/CPU spikes
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        # Unregister client on socket disconnect event
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)
