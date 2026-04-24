"""Animation helpers for maze generation and path reveal."""

from collections.abc import Callable
import time
from typing import TypeVar

from maze_display.ascii_render import render_maze
from maze_gen.models import MazeData
from maze_ui.actions import (
    compute_shortest_path,
    render_current_maze,
    toggle_path,
)
from maze_ui.constants import (
    ALT_SCREEN_OFF,
    ALT_SCREEN_ON,
    ANIM_DRAW_EVERY_STEPS,
    ANIM_MIN_FRAME_INTERVAL,
    ANIM_STEP_SLEEP_SECONDS,
    CLEAR_HOME,
    HIDE_CURSOR,
    PATH_REVEAL_MAX_STEPS,
    PATH_REVEAL_SLEEP_SECONDS,
    SHOW_CURSOR,
    STATUS_DRAWING_PATH,
    STATUS_GENERATING_PREFIX,
    STATUS_NO_PATH,
)
from maze_ui.state import UIState

T = TypeVar("T")


def run_with_generation_animation(
    operation: Callable[[Callable[[MazeData], None]], T],
    wall_color: str,
    pattern_color: str,
) -> T:
    """Run one generation operation with temporary screen animation.

    Args:
        operation: Function that performs generation with a callback.
        wall_color: Wall color for animation frame.
        pattern_color: Pattern color for animation frame.

    Returns:
        T: Result returned by operation.
    """
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
    """Build throttled callback for generation animation.

    Args:
        wall_color: Wall color for animation frame.
        pattern_color: Pattern color for animation frame.

    Returns:
        Callable[[MazeData], None]: Callback used during generation.
    """
    last_draw = 0.0
    step_count = 0

    def _on_step(data: MazeData) -> None:
        nonlocal last_draw, step_count

        step_count += 1

        now = time.perf_counter()
        is_regular_frame = (step_count % ANIM_DRAW_EVERY_STEPS) == 0
        if not is_regular_frame and (
            now - last_draw
        ) < ANIM_MIN_FRAME_INTERVAL:
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
        time.sleep(ANIM_STEP_SLEEP_SECONDS)

    return _on_step


def animate_path_reveal(state: UIState) -> None:
    """Animate shortest path reveal on screen.

    Args:
        state: Mutable UI state.
    """
    path_coords = compute_shortest_path(state)
    if not path_coords:
        state.status_message = STATUS_NO_PATH
        return

    total = len(path_coords)
    steps = min(total, PATH_REVEAL_MAX_STEPS)
    stride = max(1, total // steps)

    _enter_animation_screen()
    try:
        for end in range(1, total + 1, stride):
            state.status_message = STATUS_DRAWING_PATH
            partial = path_coords[:end]
            print(CLEAR_HOME, end="", flush=True)
            render_current_maze(state, path_override=partial)
            time.sleep(PATH_REVEAL_SLEEP_SECONDS)
    finally:
        _leave_animation_screen()

    if not state.show_path:
        toggle_path(state)


def _enter_animation_screen() -> None:
    """Enter temporary terminal buffer for animation."""
    print(ALT_SCREEN_ON + HIDE_CURSOR, end="", flush=True)


def _leave_animation_screen() -> None:
    """Return to normal terminal buffer after animation."""
    print(SHOW_CURSOR + ALT_SCREEN_OFF, end="", flush=True)
