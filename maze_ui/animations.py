"""Animation helpers for maze generation and path reveal."""

from collections.abc import Callable
import time
from typing import TypeVar

from maze_display.ascii_render import render_maze
from maze_gen.models import MazeData
from maze_ui.actions import compute_shortest_path, render_current_maze, toggle_path
from maze_ui.constants import (
    STATUS_DRAWING_PATH,
    STATUS_GENERATING_PREFIX,
    STATUS_NO_PATH,
)
from maze_ui.state import UIState

ALT_SCREEN_ON = "\033[?1049h"
ALT_SCREEN_OFF = "\033[?1049l"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_HOME = "\033[2J\033[H"

T = TypeVar("T")


def run_with_generation_animation(
    operation: Callable[[Callable[[MazeData], None]], T],
    wall_color: str,
    pattern_color: str,
) -> T:
    """Run one generation operation with temporary screen animation."""
    _enter_animation_screen()
    try:
        callback = build_generation_callback(
            wall_color=wall_color,
            pattern_color=pattern_color,
        )
        return operation(callback)
    finally:
        _leave_animation_screen()


def build_generation_callback(
    wall_color: str,
    pattern_color: str,
) -> Callable[[MazeData], None]:
    """Build throttled callback to animate maze generation steps."""
    last_draw = 0.0
    step_count = 0
    min_frame_interval = 0.02
    draw_every_steps = 4

    def _on_step(data: MazeData) -> None:
        nonlocal last_draw, step_count

        step_count += 1

        now = time.perf_counter()
        is_regular_frame = (step_count % draw_every_steps) == 0
        if not is_regular_frame and (now - last_draw) < min_frame_interval:
            return
        last_draw = now

        frame = render_maze(
            data.grid,
            entry=data.entry,
            exit=data.exit,
            path=None,
            wall_color=wall_color,
            pattern_color=pattern_color,
        )
        print(CLEAR_HOME, end="", flush=True)
        print(f"{STATUS_GENERATING_PREFIX}...", flush=True)
        print(frame, flush=True)
        time.sleep(0.008)

    return _on_step


def animate_path_reveal(state: UIState) -> None:
    """Animate shortest path reveal."""
    path_coords = compute_shortest_path(state)
    if not path_coords:
        state.status_message = STATUS_NO_PATH
        return

    total = len(path_coords)
    steps = min(total, 30)
    stride = max(1, total // steps)

    for end in range(1, total + 1, stride):
        state.status_message = STATUS_DRAWING_PATH
        partial = path_coords[:end]
        print()
        render_current_maze(state, path_override=partial)
        time.sleep(0.02)

    if not state.show_path:
        toggle_path(state)


def _enter_animation_screen() -> None:
    """Enter temporary buffer used only for generation animation."""
    print(ALT_SCREEN_ON + HIDE_CURSOR, end="", flush=True)


def _leave_animation_screen() -> None:
    """Return to normal terminal buffer after generation animation."""
    print(SHOW_CURSOR + ALT_SCREEN_OFF, end="", flush=True)
