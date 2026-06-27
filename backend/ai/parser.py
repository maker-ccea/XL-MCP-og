
import os
import re
import json
import urllib.request
import urllib.error

from typing import List, Dict, Any, Optional

from state.excel_state import state_manager

from ai.prompts import SYSTEM_PROMPT

import logging


logger = logging.getLogger("ai_parser")

def parse_with_rules(message: str) -> List[Dict[str, Any]]:
    """
    Local rule-based fallback parser that translates standard patterns into structured Excel action dicts.
    """

    msg = message.strip().lower()
    actions = []


    bold_match = re.search(r"\b(?:make|set|change)?\s*([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\s*bold\b", msg) or \
                 re.search(r"\bbold\s*([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\b", msg)
    if bold_match:
        actions.append({"action": "set_bold", "range": bold_match.group(1).upper(), "bold": True})


    italic_match = re.search(r"\b(?:make|set|change)?\s*([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\s*italic\b", msg) or \
                   re.search(r"\bitalic\s*([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\b", msg)
    if italic_match:
        actions.append({"action": "set_italic", "range": italic_match.group(1).upper(), "italic": True})


    color_match = re.search(r"\b(?:make|set|color|paint)\s+([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\s+(red|green|blue|yellow|white|black|gray|grey|orange|purple|pink|cyan|magenta)\b", msg) or \
                  re.search(r"\b(?:set|change)\s+(?:background|fill)\s+(?:of|color)?\s*([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\s+to\s+(red|green|blue|yellow|white|black|gray|grey|orange|purple|pink|cyan|magenta)\b", msg)
    if color_match:
        actions.append({
            "action": "set_background_color",
            "range": color_match.group(1).upper(),
            "color": color_match.group(2)
        })


    size_match = re.search(r"\b(?:set|change)?\s*(?:font\s+)?size\s+of\s+([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\s+to\s+(\d+(?:\.\d+)?)\b", msg) or \
                 re.search(r"\bmake\s+([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\s+(?:font\s+)?size\s+(\d+(?:\.\d+)?)\b", msg)
    if size_match:
        actions.append({
            "action": "set_font_size",
            "range": size_match.group(1).upper(),
            "size": float(size_match.group(2))
        })


    write_match = re.search(r"\bwrite\s+([^\s]+)\s+(?:to|in)\s+([a-z]+[0-9]+)\b", msg) or \
                  re.search(r"\bset\s+cell\s+([a-z]+[0-9]+)\s+to\s+([^\s]+)\b", msg)
    if write_match:

        if write_match.group(1)[0].isalpha() and write_match.group(1)[1:].isdigit():

            cell_address = write_match.group(1).upper()
            val_str = write_match.group(2)
        else:

            val_str = write_match.group(1)
            cell_address = write_match.group(2).upper()


        try:
            value: Any = float(val_str) if "." in val_str else int(val_str)
        except ValueError:
            value = val_str

        actions.append({"action": "write_cell", "cell": cell_address, "value": value})


    clear_match = re.search(r"\b(?:clear|empty|erase)(?:\s+cell|\s+range)?\s*([a-z]+[0-9]+(?::[a-z]+[0-9]+)?)\b", msg)
    if clear_match:
        actions.append({"action": "clear_cells", "range": clear_match.group(1).upper()})



    create_sheet_match = re.search(r"\bcreate\s+(?:sheet|worksheet)\s*(?:named|called)?\s*['\"]?([a-z0-9_\-\s]+)['\"]?\b", msg)
    if create_sheet_match:
        actions.append({"action": "create_sheet", "name": create_sheet_match.group(1).strip()})


    delete_sheet_match = re.search(r"\bdelete\s+(?:sheet|worksheet)\s*(?:named|called)?\s*['\"]?([a-z0-9_\-\s]+)['\"]?\b", msg)
    if delete_sheet_match:
        actions.append({"action": "delete_sheet", "name": delete_sheet_match.group(1).strip()})


    activate_sheet_match = re.search(r"\b(?:activate|switch\s+to|select|open)\s+(?:sheet|worksheet)\s*(?:named|called)?\s*['\"]?([a-z0-9_\-\s]+)['\"]?\b", msg)
    if activate_sheet_match:
        actions.append({"action": "activate_sheet", "name": activate_sheet_match.group(1).strip()})


    rename_sheet_match = re.search(r"\brename\s+(?:sheet|worksheet)\s*['\"]?([a-z0-9_\-\s]+)['\"]?\s+to\s+['\"]?([a-z0-9_\-\s]+)['\"]?\b", msg)
    if rename_sheet_match:
        actions.append({
            "action": "rename_sheet",
            "old_name": rename_sheet_match.group(1).strip(),
            "new_name": rename_sheet_match.group(2).strip()
        })


    if "save workbook" in msg or "save file" in msg:
        actions.append({"action": "save_workbook"})
    elif "close workbook" in msg or "close file" in msg:
        actions.append({"action": "close_workbook"})
    elif "create workbook" in msg or "new workbook" in msg:
        actions.append({"action": "create_workbook"})


    autofit_match = re.search(r"\b(?:autofit|auto\s*fit)(?:\s+columns?\s+of)?\s*([a-z]+[0-9]*(?::[a-z]+[0-9]*)?)\b", msg)
    if autofit_match:
        actions.append({"action": "auto_fit_columns", "range": autofit_match.group(1).upper()})


    formula_match = re.search(r"\bapply\s+formula\s+([^\s]+)\s+to\s+([a-z]+[0-9]+)\b", msg)
    if formula_match:
        actions.append({
            "action": "apply_formula",
            "cell": formula_match.group(2).upper(),
            "formula": formula_match.group(1)
        })

    return actions

def parse_with_llm(message: str) -> Optional[List[Dict[str, Any]]]:
    """
    Sends the user message and current Excel workbook state to an LLM provider if configured.
    Supports Gemini and OpenAI API endpoints.
    """

    state = state_manager.get_current_state()


    formatted_prompt = (
        SYSTEM_PROMPT
        .replace("{workbook_name}", str(state.get("workbook") or "None"))
        .replace("{sheet_name}", str(state.get("sheet") or "None"))
        .replace("{selected_range}", str(state.get("selection") or "None"))
        .replace("{used_range}", str(state.get("used_range") or "None"))
        .replace("{available_sheets}", str([]))
    )


    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"

            payload = {
                "contents": [
                    {"role": "user", "parts": [{"text": f"{formatted_prompt}\n\nUser request: {message}"}]}
                ]
            }

            data_bytes = json.dumps(payload).encode("utf-8")

            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)

                text = res_json["candidates"][0]["content"]["parts"][0]["text"]

                clean_text = re.sub(r"^```(?:json)?\s*|```\s*$", "", text.strip(), flags=re.MULTILINE)

                return json.loads(clean_text)
        except Exception as e:
            logger.error(f"Gemini LLM parsing failed: {e}")


    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": "gpt-4-turbo",
                "messages": [
                    {"role": "system", "content": formatted_prompt},
                    {"role": "user", "content": message}
                ],
                "temperature": 0.0
            }
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                text = res_json["choices"][0]["message"]["content"]
                clean_text = re.sub(r"^```(?:json)?\s*|```\s*$", "", text.strip(), flags=re.MULTILINE)
                return json.loads(clean_text)
        except Exception as e:
            logger.error(f"OpenAI LLM parsing failed: {e}")


    return None

def parse_natural_language(message: str) -> List[Dict[str, Any]]:
    """
    Entrypoint parser. Tries to parse using LLM, and falls back to rules if it fails or keys are missing.
    """

    llm_actions = parse_with_llm(message)
    if llm_actions is not None:
        logger.info("Successfully parsed natural language using LLM API.")
        return llm_actions


    logger.info("Falling back to local rule-based parsing engine.")
    return parse_with_rules(message)