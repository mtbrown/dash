import abc

from .component import Component


class GridNode:
    __metaclass__ = abc.ABCMeta

    def __init__(self, *children):
        self.children = []
        self.components = []  # list of components that are descendants (not necessarily directly) of the node

        for child in children:
            self.children.append(child)
            if isinstance(child, GridNode):
                self.components.extend(child.components)
            elif isinstance(child, Component):
                self.components.append(child)


class Grid(GridNode):
    def __init__(self, *children):
        super().__init__(*children)

    @property
    def state(self):
        return {
            'type': 'Grid',
            'children': [child.grid_state for child in self.children]
        }


class Row(GridNode):
    def __init__(self, *children):
        super().__init__(*children)

    @property
    def grid_state(self):
        return {
            'type': 'Row',
            'children': [child.grid_state for child in self.children]
        }


class Col(GridNode):
    def __init__(self, *children, xs: int = None, sm: int = None, md: int = None, lg: int = None):
        super().__init__(*children)
        self.xs = xs
        self.sm = sm
        self.md = md
        self.lg = lg

    @property
    def grid_state(self):
        return {
            'type': 'Col',
            'children': [child.grid_state for child in self.children],
            'props': {key: val for (key, val) in self.__dict__.items() if val is not None
                      and key not in ['children', 'components']}
        }
