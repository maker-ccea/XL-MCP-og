
from fastapi.testclient import TestClient

from unittest.mock import patch, MagicMock

from main import app


client = TestClient(app)

def test_health_endpoint():
    """
    Tests that the GET /health endpoint correctly returns status.
    Mocks Excel running status to True.
    """

    with patch("excel.excel_connection.excel_conn.is_excel_running", return_value=True):

        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "healthy"
        assert data["excel_running"] is True

def test_state_endpoint_empty():
    """
    Tests GET /state endpoint returns empty defaults when no workbook is open.
    """

    mock_context = {
        "workbook_name": None,
        "sheet_name": None,
        "selected_range": None,
        "available_sheets": []
    }
    with patch("routes.chat.get_workbook_context", return_value=mock_context):

        response = client.get("/state")
        assert response.status_code == 200
        data = response.json()

        assert data["workbook_name"] is None
        assert data["sheet_name"] is None
        assert data["selected_range"] is None
        assert data["available_sheets"] == []

def test_chat_endpoint_valid_command():
    """
    Tests that POST /chat correctly plans and validates standard user messages.
    """

    response = client.post("/chat", json={"message": "make A1 bold"})
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "make A1 bold"

    assert len(data["plan"]) > 0
    assert data["plan"][0]["action"]["action"] == "set_bold"
    assert data["plan"][0]["action"]["range"] == "A1"

