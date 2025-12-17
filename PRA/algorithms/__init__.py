"""Page Replacement Algorithms."""

from .base_replacer import BaseReplacer, PageReplacementResult, PageAccessResult
from .fifo import FIFOReplacer
from .lru import LRUReplacer
from .optimal import OptimalReplacer
from .second_chance import SecondChanceReplacer
from .clock import ClockReplacer

__all__ = [
    'BaseReplacer', 'PageReplacementResult', 'PageAccessResult',
    'FIFOReplacer', 'LRUReplacer', 'OptimalReplacer', 
    'SecondChanceReplacer', 'ClockReplacer'
]
