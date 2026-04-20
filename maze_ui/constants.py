"""Simple constants for terminal UI text and options."""

APP_TITLE = "A_MAZE_IN"

COLOR_OPTIONS = [
    "default",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]

MENU_FOOTER_TEXT = (
    "[1] New  [2] Path  [3] Walls  [4] 42  [5] Quit"
)

PROMPT_OPTION = "Option > "
PROMPT_COLOR = "Select color (name or number): "

STATUS_READY = "Maze ready."
STATUS_NEW_MAZE = "New maze generated."
STATUS_PATH_ON = "Shortest path: ON."
STATUS_PATH_OFF = "Shortest path: OFF."
STATUS_NO_PATH = "No valid path between entry and exit."
STATUS_DRAWING_PATH = "Drawing shortest path..."
STATUS_INVALID_OPTION = "Invalid option. Choose 1 to 5."
STATUS_INVALID_COLOR = "Invalid color. Keeping 'default'."
STATUS_GENERATING_PREFIX = "Generating maze"

LABEL_WALL_COLOR = "Choose wall color"
LABEL_PATTERN_COLOR = "Choose 42 pattern color"
