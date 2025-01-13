import attr
import time
from typing import Any, BinaryIO, Dict, Optional
from pysmt.shortcuts import simplify
from kipro2.expectations.Guard import Guard
import re

@attr.s
class Timer:
    """
    A timer keeps a total time in seconds and allows starting and stopping it to
    increment the values.
    """

    _elapsed: float = attr.ib(default=0.0)
    _timer_start: Optional[float] = attr.ib(default=None)
    """The start time returned from time.perf_counter()."""
    def start_timer(self):
        assert self._timer_start is None, "cannot start timer twice without stopping in between"
        self._timer_start = time.perf_counter()

    def stop_timer(self):
        end = time.perf_counter()
        assert self._timer_start is not None, "cannot stop timer that is not running"
        self._elapsed += end - self._timer_start
        self._timer_start = None

    @property
    def value(self) -> float:
        """Return the current value of this timer, including running timer values."""
        extra = time.perf_counter(
        ) - self._timer_start if self._timer_start is not None else 0
        return self._elapsed + extra

    def __getstate__(self) -> float:
        return self.value

    def __setstate__(self, value: float):
        self._elapsed = value
        self._timer_start = None

    def __str__(self) -> str:
        return f"{round(self.value, 2)} s"


def _make_running_timer() -> Timer:
    timer = Timer()
    timer.start_timer()
    return timer


@attr.s
class Statistics:

    program: str = attr.ib()
    post: str = attr.ib()
    prop: str = attr.ib()
    engine: str = attr.ib()

    k: int = attr.ib(default=None)
    final_size: int = attr.ib(default=None)
    result: str = attr.ib(default="")

    formula_time: Timer = attr.ib(factory=Timer)
    sat_time: Timer = attr.ib(factory=Timer)
    total_time: Timer = attr.ib(factory=_make_running_timer)


    def __str__(self):
        lines = [
            "------- Statistics for %s (%s, post: %s, pre: %s) -------" % (self.engine, self.program, self.post, self.prop), f"Total time = {self.total_time}",
            f"result = {self.result}",
            f"k = {self.k}",
            f"Expectation size = {self.final_size}",
            "",
            f"Total time = {self.total_time}",
            f"Sat time = {self.sat_time}",
            f"Formula time = {self.formula_time}",
        ]

        try:
            lines.append(f"Inductive Invariant = {self.inductive_invariant}")
        except:
            pass

        return "\n".join(lines)

