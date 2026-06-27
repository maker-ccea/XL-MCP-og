
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

def test_chat_sort_command():
    """
    Tests that a sort instruction is correctly parsed into a sort_range action.
    """
    with patch("ai.parser.parse_with_llm", return_value=[
        {"action": "sort_range", "range": "A1:C50", "key_column": 2, "ascending": True, "has_headers": True}
    ]):
        response = client.post("/chat", json={"message": "sort the second column Department in ascending order"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["plan"]) > 0
        action = data["plan"][0]["action"]
        assert action["action"] == "sort_range"
        assert action["range"] == "A1:C50"
        assert action["key_column"] == 2
        assert action["ascending"] is True
        assert action["has_headers"] is True

def test_sort_range_logic():
    """
    Tests the in-memory Python sort_range logic.
    """
    import excel.cells as cells
    
    mock_range = MagicMock()
    mock_range.value = [
        ["Name", "Department", "Salary"],
        ["Alice", "HR", 50000],
        ["Bob", "Engineering", 60000],
        ["Charlie", "Sales", 55000],
    ]
    
    mock_sheet = MagicMock()
    mock_sheet.range.return_value = mock_range
    
    with patch("excel.cells.get_active_sheet", return_value=mock_sheet):
        cells.sort_range("A1:C4", key_column=2, ascending=True, has_headers=True)
        
        # Expected sorted order: Engineering (Bob), HR (Alice), Sales (Charlie)
        expected = [
            ["Name", "Department", "Salary"],
            ["Bob", "Engineering", 60000],
            ["Alice", "HR", 50000],
            ["Charlie", "Sales", 55000],
        ]
        assert mock_range.value == expected


