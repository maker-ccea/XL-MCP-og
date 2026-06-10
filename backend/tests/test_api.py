# Import FastAPI TestClient tool
from fastapi.testclient import TestClient
# Import unittest mock tools to prevent unit tests from spawning real Excel processes
from unittest.mock import patch, MagicMock
# Import the main FastAPI app instance to bind with TestClient
from main import app

# Create a TestClient wrapper around the FastAPI app
client = TestClient(app)

def test_health_endpoint():
    """
    Tests that the GET /health endpoint correctly returns status.
    Mocks Excel running status to True.
    """
    # Mock the is_excel_running method of ExcelConnectionManager
    with patch("excel.excel_connection.excel_conn.is_excel_running", return_value=True):
        # Query GET /health endpoint
        response = client.get("/health")
        # Assert status code is 200 OK
        assert response.status_code == 200
        # Parse the JSON response
        data = response.json()
        # Assert the response values match mock parameters
        assert data["status"] == "healthy"
        assert data["excel_running"] is True

def test_state_endpoint_empty():
    """
    Tests GET /state endpoint returns empty defaults when no workbook is open.
    """
    # Mock get_workbook_context to return empty values
    mock_context = {
        "workbook_name": None,
        "sheet_name": None,
        "selected_range": None,
        "available_sheets": []
    }
    with patch("routes.chat.get_workbook_context", return_value=mock_context):
        # Query GET /state endpoint
        response = client.get("/state")
        assert response.status_code == 200
        data = response.json()
        # Assert returned context parameters are None or empty list
        assert data["workbook_name"] is None
        assert data["sheet_name"] is None
        assert data["selected_range"] is None
        assert data["available_sheets"] == []

def test_chat_endpoint_valid_command():
    """
    Tests that POST /chat correctly plans and validates standard user messages.
    """
    # Query POST /chat with a formatting command
    response = client.post("/chat", json={"message": "make A1 bold"})
    assert response.status_code == 200
    data = response.json()
    # Assert plan response fields
    assert data["message"] == "make A1 bold"
    # Rule parser should return set_bold action for A1
    assert len(data["plan"]) > 0
    assert data["plan"][0]["action"]["action"] == "set_bold"
    assert data["plan"][0]["action"]["range"] == "A1"
    # If no workbook is active, all_valid could be False, which is correct behavior for validation layer
    # Since we didn't mock get_active_workbook, it runs on the real context (or returns False if closed)
