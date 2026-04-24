"""Constants used by maze terminal rendering.

Grouped by responsibility to keep renderer logic separate from static data.
"""

# ANSI styling
ANSI_RESET = "\033[0m"
ANSI_COLORS = {
    "default": "",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}
ANSI_BG_COLORS = {
    "default": "",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
}

# Render tuning
CELL_WIDTH = 3
PATH_COLOR = "yellow"

# Box-drawing lookup tables
JUNCTIONS = {
    (False, False, False, False): " ",
    (False, False, False, True): "╶",
    (False, False, True, False): "╴",
    (False, False, True, True): "─",
    (False, True, False, False): "╷",
    (False, True, False, True): "┌",
    (False, True, True, False): "┐",
    (False, True, True, True): "┬",
    (True, False, False, False): "╵",
    (True, False, False, True): "└",
    (True, False, True, False): "┘",
    (True, False, True, True): "┴",
    (True, True, False, False): "│",
    (True, True, False, True): "├",
    (True, True, True, False): "┤",
    (True, True, True, True): "┼",
}

PATH_GLYPHS = dict(JUNCTIONS)
PATH_GLYPHS[(False, False, False, False)] = "•"
