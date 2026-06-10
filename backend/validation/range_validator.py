# Import regular expression module for string pattern matching
import re

# Compiled regex pattern to match a single cell address (e.g., A1, AB12)
# [A-Z]+ matches one or more column letters, [0-9]+ matches one or more row numbers
CELL_PATTERN = re.compile(r"^[A-Z]+[0-9]+$", re.IGNORECASE)

# Compiled regex pattern to match a standard cell range (e.g., A1:C10)
RANGE_PATTERN = re.compile(r"^[A-Z]+[0-9]+:[A-Z]+[0-9]+$", re.IGNORECASE)

# Compiled regex pattern to match a column range (e.g., A:B, G:G)
COLUMN_PATTERN = re.compile(r"^[A-Z]+:[A-Z]+$", re.IGNORECASE)

# Compiled regex pattern to match a row range (e.g., 1:10, 5:5)
ROW_PATTERN = re.compile(r"^[0-9]+:[0-9]+$", re.IGNORECASE)

def validate_range_format(range_address: str) -> bool:
    """
    Validates if a given range string conforms to standard Excel range patterns (A1, A1:B10, A:B, 1:10).
    """
    # Remove leading and trailing whitespaces
    address = range_address.strip()
    
    # Check if the string matches any of our valid range patterns
    if CELL_PATTERN.match(address):
        return True
    if RANGE_PATTERN.match(address):
        return True
    if COLUMN_PATTERN.match(address):
        return True
    if ROW_PATTERN.match(address):
        return True
        
    # Return False if none of the regex patterns matched the address format
    return False
