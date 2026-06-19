
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect

from typing import List, Dict, Any

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

from ai.planner import generate_action_plan
from validation.action_validator import validate_action
from executor.action_executor import execute_action_plan
from state.excel_state import state_manager
from excel.excel_connection import excel_conn
from excel.context import get_workbook_context

import asyncio

import logging
import uuid

from state.graph_db import graph_db


logger = logging.getLogger("chat_routes")


router = APIRouter()



@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Accepts user natural language message, parses into action plan,
    validates the actions, and returns an execution preview.
    """
    try:

        plan = generate_action_plan(request.message)


        msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        graph_db.add_node(msg_id, "Message", {"message": request.message})

        curr_state = state_manager.get_current_state()
        wb_name = curr_state.get("workbook")
        if wb_name:
            graph_db.add_edge(msg_id, wb_name, "IN_WORKBOOK")


        previews = []
        all_valid = True

        for action in plan:

            if not action.id:
                action.id = str(uuid.uuid4())


            graph_db.add_node(action.id, "Action", action.model_dump())
            graph_db.add_edge(msg_id, action.id, "TRIGGERED")


            is_valid, err_msg = validate_action(action)

            if not is_valid:
                all_valid = False

            previews.append(
                ActionPreview(
                    action=action,
                    is_valid=is_valid,
                    error_message=err_msg
                )
            )


        return ChatResponse(
            message=request.message,
            plan=previews,
            all_valid=all_valid
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")

        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", response_model=ExecuteResponse)
async def execute_endpoint(request: ExecuteRequest):
    """
    Executes the list of client-approved actions in sequence.
    """
    try:

        for action in request.actions:
            is_valid, err_msg = validate_action(action)
            if not is_valid:
                raise HTTPException(
                    status_code=400,
                    detail=f"Action validation failed for execution: {err_msg}"
                )


        results = execute_action_plan(request.actions)


        successes = sum(1 for r in results if r.success)
        failures = sum(1 for r in results if not r.success)


        return ExecuteResponse(
            results=results,
            success_count=successes,
            failure_count=failures
        )
    except HTTPException as he:

        raise he
    except Exception as e:
        logger.error(f"Error in execution endpoint: {e}")

        raise HTTPException(status_code=500, detail=str(e))

@router.get("/state", response_model=WorkbookContext)
async def get_state_endpoint():
    """
    Returns the current active workbook context.
    """
    try:

        context = get_workbook_context()

        return WorkbookContext(
            workbook_name=context.get("workbook_name"),
            sheet_name=context.get("sheet_name"),
            selected_range=context.get("selected_range"),
            available_sheets=context.get("available_sheets", [])
        )
    except Exception as e:
        logger.error(f"Error in state endpoint: {e}")

        return WorkbookContext(workbook_name=None, sheet_name=None, selected_range=None, available_sheets=[])

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history_endpoint():
    """
    Returns the history of all executed actions.
    """

    return state_manager.get_history()

@router.post("/undo/{action_id}")
async def undo_endpoint(action_id: str):
    """
    Undoes a specific action by restoring the range snapshot captured prior to execution.
    """
    from executor.undo_manager import undo_manager
    success = undo_manager.trigger_undo(action_id)
    if not success:
        raise HTTPException(status_code=400, detail=f"No undo snapshot found or failed to restore for action {action_id}")
    return {"status": "success", "action_id": action_id}

@router.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """
    Checks backend service status and Excel connectivity status.
    """

    excel_running = excel_conn.is_excel_running()

    return HealthResponse(
        status="healthy",
        excel_running=excel_running
    )



class ConnectionManager:
    """
    Manages active WebSocket connections for streaming live Excel state changes.
    """
    def __init__(self):

        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):

        await websocket.accept()

        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):

        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket client disconnected.")

    async def broadcast(self, message: dict):

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:

                pass


ws_manager = ConnectionManager()

@router.websocket("/ws/state")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that streams state updates to connected clients.
    Broadcasts state whenever selection changes in Excel.
    """

    await ws_manager.connect(websocket)
    try:

        while True:

            if state_manager.track_selection_changes():

                current_state = state_manager.get_current_state()

                await ws_manager.broadcast({
                    "event": "state_changed",
                    "state": current_state
                })

            await asyncio.sleep(0.5)
    except WebSocketDisconnect:

        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket)



@router.get("/graph/summary")
async def graph_summary_endpoint():
    """
    Returns the complete local graph database summary (nodes and edges).
    """
    try:
        return graph_db.get_summary()
    except Exception as e:
        logger.error(f"Error retrieving graph summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))