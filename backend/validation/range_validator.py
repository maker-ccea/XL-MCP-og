
import re



CELL_PATTERN = re.compile(r"^[A-Z]+[0-9]+$", re.IGNORECASE)


RANGE_PATTERN = re.compile(r"^[A-Z]+[0-9]+:[A-Z]+[0-9]+$", re.IGNORECASE)


COLUMN_PATTERN = re.compile(r"^[A-Z]+:[A-Z]+$", re.IGNORECASE)


ROW_PATTERN = re.compile(r"^[0-9]+:[0-9]+$", re.IGNORECASE)

def validate_range_format(range_address: str) -> bool:
    """
    Validates if a given range string conforms to standard Excel range patterns (A1, A1:B10, A:B, 1:10).
    """

    address = range_address.strip()


    if CELL_PATTERN.match(address):
        return True
    if RANGE_PATTERN.match(address):
        return True
    if COLUMN_PATTERN.match(address):
        return True
    if ROW_PATTERN.match(address):
        return True


    return False