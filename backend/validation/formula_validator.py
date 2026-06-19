
import re


SUSPICIOUS_PATTERNS = [

    r"cmd(?:\.exe)?",
    r"powershell(?:\.exe)?",
    r"wscript(?:\.exe)?",
    r"cscript(?:\.exe)?",
    r"mshta(?:\.exe)?",

    r"rundll32(?:\.exe)?",
    r"regsvr32(?:\.exe)?",

    r"[a-z0-9_-]+\s*\|\s*['\"]?[a-z0-9_.-]+['\"]?\s*!",

    r"hyperlink\s*\(\s*['\"](?:file|http|https)://.*\.(?:exe|bat|cmd|ps1|vbs|sh)"
]

def validate_formula_safety(formula: str) -> bool:
    """
    Validates if an Excel formula starts with '=' and is free of security threats (like DDE injections).
    """

    cleaned_formula = formula.strip()


    if not cleaned_formula.startswith("="):
        return False


    lower_formula = cleaned_formula.lower()


    for pattern in SUSPICIOUS_PATTERNS:

        if re.search(pattern, lower_formula):

            return False


    return True