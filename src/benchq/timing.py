"""Simplify timing code occurring in multiple places."""
import contextlib
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimingInfo:
    start_counter: float
    stop_counter: Optional[float] = None

    @property
    def total(self) -> float:
        assert self.stop_counter is not None
        return self.stop_counter - self.start_counter


@contextlib.contextmanager
def measure_time():
    info = TimingInfo(time.perf_counter())
    yield info
    info.stop_counter = time.perf_counter()
