# Import regular expressions to scan for potential security risks
import re

# List of keywords/patterns that could represent a Dynamic Data Exchange (DDE) exploit or command execution
SUSPICIOUS_PATTERNS = [
    # Match Windows executable names or shells commonly used in exploits
    r"cmd(?:\.exe)?",
    r"powershell(?:\.exe)?",
    r"wscript(?:\.exe)?",
    r"cscript(?:\.exe)?",
    r"mshta(?:\.exe)?",
    # Match COM / DLL execution or system calls
    r"rundll32(?:\.exe)?",
    r"regsvr32(?:\.exe)?",
    # Match standard DDE execution format (e.g. APPLICATION|TOPIC!ITEM or APPLICATION|'TOPIC'!ITEM)
    r"[a-z0-9_-]+\s*\|\s*['\"]?[a-z0-9_.-]+['\"]?\s*!",
    # Match hyperlink formulas pointing to local executable files/scripts
    r"hyperlink\s*\(\s*['\"](?:file|http|https)://.*\.(?:exe|bat|cmd|ps1|vbs|sh)"
]

def validate_formula_safety(formula: str) -> bool:
    """
    Validates if an Excel formula starts with '=' and is free of security threats (like DDE injections).
    """
    # Clean the input formula string by removing surrounding whitespace
    cleaned_formula = formula.strip()

    # An Excel formula must begin with an equals sign
    if not cleaned_formula.startswith("="):
        return False

    # Convert the formula to lowercase to ensure case-insensitive pattern matching
    lower_formula = cleaned_formula.lower()

    # Loop through each dangerous pattern and verify it does not exist in the formula
    for pattern in SUSPICIOUS_PATTERNS:
        # Perform regex search for the suspicious pattern
        if re.search(pattern, lower_formula):
            # If a match is found, flag the formula as unsafe
            return False

    # If the formula passed all checks, return True
    return True
