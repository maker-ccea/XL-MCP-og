# Import pytest framework for writing unit tests
import pytest
# Import the validators we want to test
from validation.range_validator import validate_range_format
from validation.formula_validator import validate_formula_safety

def test_range_validator_single_cell():
    """
    Tests that the range validator correctly validates single cell formats (e.g. A1, Z99).
    """
    # Assert standard uppercase cell coordinates return True
    assert validate_range_format("A1") is True
    assert validate_range_format("Z99") is True
    # Assert case-insensitivity works
    assert validate_range_format("b10") is True
    # Assert multi-letter columns work
    assert validate_range_format("ABC500") is True

def test_range_validator_cell_ranges():
    """
    Tests that the range validator correctly validates range formats (e.g. A1:B10).
    """
    # Assert standard uppercase cell ranges return True
    assert validate_range_format("A1:B10") is True
    # Assert case-insensitivity in cell range works
    assert validate_range_format("a1:b10") is True

def test_range_validator_row_column_ranges():
    """
    Tests that the range validator correctly validates row-only or column-only ranges (e.g. A:B, 1:10).
    """
    # Assert column ranges return True
    assert validate_range_format("A:B") is True
    assert validate_range_format("c:z") is True
    # Assert row ranges return True
    assert validate_range_format("1:10") is True
    assert validate_range_format("5:5") is True

def test_range_validator_invalid_formats():
    """
    Tests that invalid range expressions correctly return False.
    """
    # Assert completely malformed strings return False
    assert validate_range_format("invalid") is False
    # Assert missing row number returns False
    assert validate_range_format("A") is False
    # Assert number first returns False
    assert validate_range_format("1A") is False
    # Assert spaces or extra symbols return False
    assert validate_range_format("A1 : B10") is False

def test_formula_validator_valid():
    """
    Tests that safe, valid formula patterns pass the validator.
    """
    # Assert basic math formulas return True
    assert validate_formula_safety("=SUM(A1:A10)") is True
    assert validate_formula_safety("=AVERAGE(B1, B2)") is True
    assert validate_formula_safety("=A1+B1") is True
    # Assert case variation works
    assert validate_formula_safety("=sum(a1:a10)") is True

def test_formula_validator_invalid_syntax():
    """
    Tests that formulas must start with '='.
    """
    # Assert missing '=' returns False
    assert validate_formula_safety("SUM(A1:A10)") is False

def test_formula_validator_security_threats():
    """
    Tests that formulas containing suspicious patterns/DDE threats return False.
    """
    # Assert DDE injection pattern using cmd.exe returns False
    assert validate_formula_safety("=cmd|' /C calc'!A0") is False
    # Assert powershell commands return False
    assert validate_formula_safety("=powershell|' -bypass '!A0") is False
    # Assert malicious hyperlink formulas return False
    assert validate_formula_safety("=HYPERLINK(\"file:///C:/Windows/System32/cmd.exe\", \"Click Me\")") is False
