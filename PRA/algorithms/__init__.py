"""Page Replacement Algorithms."""

from .fifo import FIFOReplacer
from .base_replacer import BaseReplacer

__all__ = ['FIFOReplacer', 'BaseReplacer']
