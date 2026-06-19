
import xlwings as xw

from typing import Tuple, Union

from excel.worksheet import get_active_sheet

def _parse_color(color: Union[str, Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """
    Helper function to parse standard color names or HEX values into RGB tuples.
    """

    if isinstance(color, tuple) and len(color) == 3:
        return color


    c_str = str(color).strip().lower()


    color_map = {
        "red": (255, 0, 0),
        "green": (0, 128, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "gray": (128, 128, 128),
        "grey": (128, 128, 128),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "light_gray": (211, 211, 211),
        "light_grey": (211, 211, 211),
        "dark_gray": (169, 169, 169),
        "dark_grey": (169, 169, 169)
    }


    if c_str in color_map:
        return color_map[c_str]


    if c_str.startswith("#"):
        c_str = c_str[1:]


    try:

        return (int(c_str[0:2], 16), int(c_str[2:4], 16), int(c_str[4:6], 16))
    except Exception:

        return (200, 200, 200)

def _rgb_to_win32_color(rgb: Tuple[int, int, int]) -> int:
    """
    Converts an RGB tuple (R, G, B) into a Win32 COLORREF integer (0x00BBGGRR).
    Excel COM API expects Win32 COLORREF format for Font.Color.
    """

    r, g, b = rgb

    return r + (g * 256) + (b * 65536)

def set_bold(range_address: str, bold: bool = True) -> None:
    """
    Sets the font bold status of a cell range.
    """

    sheet = get_active_sheet()

    sheet.range(range_address).api.Font.Bold = bold

def set_italic(range_address: str, italic: bool = True) -> None:
    """
    Sets the font italic status of a cell range.
    """

    sheet = get_active_sheet()

    sheet.range(range_address).api.Font.Italic = italic

def set_font_size(range_address: str, size: float) -> None:
    """
    Sets the font size of a cell range.
    """

    sheet = get_active_sheet()

    sheet.range(range_address).api.Font.Size = size

def set_font_color(range_address: str, color: Union[str, Tuple[int, int, int]]) -> None:
    """
    Sets the font text color of a cell range.
    """

    sheet = get_active_sheet()

    rgb = _parse_color(color)

    win32_color = _rgb_to_win32_color(rgb)

    sheet.range(range_address).api.Font.Color = win32_color

def set_background_color(range_address: str, color: Union[str, Tuple[int, int, int]]) -> None:
    """
    Sets the background fill color of a cell range.
    """

    sheet = get_active_sheet()

    rgb = _parse_color(color)

    sheet.range(range_address).color = rgb

def auto_fit_columns(range_address: str) -> None:
    """
    Automatically adjusts column widths in the range to fit their contents.
    """

    sheet = get_active_sheet()

    sheet.range(range_address).columns.autofit()