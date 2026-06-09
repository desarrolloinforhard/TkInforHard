"""Small animation helper for Tk widgets."""

from __future__ import annotations

from collections.abc import Callable


class IHAnimator:
    """Drive short UI transitions with Tk's ``after`` loop."""

    def __init__(self, widget, duration: int = 140, fps: int = 60, easing: str = "ease_out"):
        self.widget = widget
        self.duration = max(1, duration)
        self.frame_ms = max(8, int(1000 / max(1, fps)))
        self.easing = easing
        self._after_id = None
        self._start = 0.0
        self._end = 0.0
        self._current = 0.0
        self._elapsed = 0
        self._on_frame: Callable[[float], None] | None = None
        self._on_done: Callable[[], None] | None = None

    @property
    def value(self) -> float:
        """Return the last animated value."""

        return self._current

    def animate_to(
        self,
        target: float,
        on_frame: Callable[[float], None],
        on_done: Callable[[], None] | None = None,
    ) -> None:
        """Animate from the current value to ``target``."""

        self.cancel()
        self._start = self._current
        self._end = target
        self._elapsed = 0
        self._on_frame = on_frame
        self._on_done = on_done
        self._tick()

    def set(self, value: float) -> None:
        """Set the current value without animation."""

        self.cancel()
        self._current = value

    def cancel(self) -> None:
        """Cancel any pending animation frame."""

        if self._after_id is not None:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _tick(self) -> None:
        progress = min(1.0, self._elapsed / self.duration)
        eased = self._ease(progress)
        self._current = self._start + (self._end - self._start) * eased
        if self._on_frame is not None:
            self._on_frame(self._current)
        if progress >= 1.0:
            self._after_id = None
            if self._on_done is not None:
                self._on_done()
            return
        self._elapsed += self.frame_ms
        self._after_id = self.widget.after(self.frame_ms, self._tick)

    def _ease(self, progress: float) -> float:
        if self.easing == "linear":
            return progress
        if self.easing == "ease_in":
            return progress * progress
        if self.easing == "ease_in_out":
            return 3 * progress * progress - 2 * progress * progress * progress
        return 1 - (1 - progress) * (1 - progress)
