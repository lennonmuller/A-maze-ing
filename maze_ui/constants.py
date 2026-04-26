"""Constants used by terminal UI modules.

Sections are grouped by responsibility so each UI module can import
only what it needs.
"""

# Layout and framing
APP_TITLE = "A_MAZE_ING"
FIXED_UI_WIDTH_CELLS = 15
UI_CELL_RENDER_WIDTH = 4
UI_FRAME_EXTRA_WIDTH = 1
UI_FRAME_BORDER_DISCOUNT = 2
UI_MIN_INNER_WIDTH = 16

# Menu behavior and labels
DEFAULT_COLOR = "default"
DEFAULT_WALL_COLOR = "red"
DEFAULT_PATTERN_COLOR = "green"
MENU_OPTION_NEW = "1"
MENU_OPTION_PATH = "2"
MENU_OPTION_WALLS = "3"
MENU_OPTION_PATTERN = "4"
MENU_OPTION_ALGORITHM = "5"
MENU_OPTION_QUIT = "6"
MENU_FOOTER_TEMPLATE = (
    "[1] New  [2] Path  [3] Walls  [4] 42  [5] {next_algo}  [6] Quit"
)

COLOR_OPTIONS = [
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]

PROMPT_OPTION = "Option > "
PROMPT_COLOR = "Select color (name or number): "
LABEL_WALL_COLOR = "Choose wall color"
LABEL_PATTERN_COLOR = "Choose 42 pattern color"

# Status and feedback messages
STATUS_ALGO_CHANGED = "Algorithm changed to "
STATUS_READY = "Maze ready."
STATUS_NEW_MAZE = "New maze generated."
STATUS_PATH_ON = "Shortest path: ON."
STATUS_PATH_OFF = "Shortest path: OFF."
STATUS_NO_PATH = "No valid path between entry and exit."
STATUS_DRAWING_PATH = "Drawing shortest path..."
STATUS_INVALID_OPTION = "Invalid option. Choose 1 to 6."
STATUS_INVALID_COLOR = "Invalid color. Keeping current color."
STATUS_GENERATING_PREFIX = "Generating maze"
STATUS_QUIT = "Exiting program. See you next time."

# Terminal control sequences
ALT_SCREEN_ON = "\033[?1049h"
ALT_SCREEN_OFF = "\033[?1049l"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_HOME = "\033[3J\033[1;1H"

# Animation tuning
ANIM_MIN_FRAME_INTERVAL = 0.03
ANIM_DRAW_EVERY_STEPS = 1
ANIM_STEP_SLEEP_SECONDS = 0.0012
PATH_REVEAL_MAX_STEPS = 50
PATH_REVEAL_SLEEP_SECONDS = 0.016
