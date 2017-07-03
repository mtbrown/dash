import abc


class BaseComponent:
    def __init__(self, id: str, type: str):
        self.type = type
        self.id = id

    @property
    def state(self):
        return {
            'type': self.type,
            'id': self.id
        }


class GridNode:
    __metaclass__ = abc.ABCMeta

    _context = []

    @classmethod
    def add_component(cls, component):
        if len(cls._context) < 1:
            return

        parent = cls._context[-1]
        parent.add_child(BaseComponent(component.id, component.__class__.__name__))

    def __init__(self):
        self.children = []

    def add_child(self, child: 'GridNode'):
        self.children.append(child)

    def __enter__(self):
        self._context.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._context.pop()

        if len(self._context) > 0:
            parent = self._context[-1]
            parent.add_child(self)


class Grid(GridNode):
    def __init__(self):
        super().__init__()

    @property
    def state(self):
        return {
            'type': 'Grid',
            'children': [child.state for child in self.children]
        }


class Row(GridNode):
    def __init__(self):
        super().__init__()

    @property
    def state(self):
        return {
            'type': 'Row',
            'children': [child.state for child in self.children]
        }

    def add_child(self, child: GridNode):
        if not isinstance(child, Col):
            raise ValueError("Only Col objects can be added to a row")
        super().add_child(child)


class Col(GridNode):
    def __init__(self, xs: int = None, sm: int = None, md: int = None, lg: int = None):
        super().__init__()
        self.xs = xs
        self.sm = sm
        self.md = md
        self.lg = lg

    @property
    def state(self):
        return {
            'type': 'Col',
            'children': [child.state for child in self.children],
            'props': {key: val for (key, val) in self.__dict__.items() if val is not None
                      and key not in ['children']}
        }
