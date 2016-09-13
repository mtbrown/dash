"""
A Panel object is used for all interactions between a script and the library. It provides
access to a dictionary containing all of the UI components and the grid.
"""
from typing import Dict

from .components.component import Component
from .grid import Grid


class Panel:
    def __init__(self, script_id: str, grid: Grid, components: Dict[str, Component]):
        self.script_id = script_id
        self.grid = grid
        self.components = components
        self.store = {}
