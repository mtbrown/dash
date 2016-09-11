from typing import List

from .component import Component


class Text(Component):
    def __init__(self, id: str, title: str = None, text: str = ""):
        super().__init__(id, title=title)
        self.text = self.register_property('text', text)

    @property
    def state(self):
        return {
            "text": self.text
        }


class Table(Component):
    def __init__(self, id: str, title: str = None, rows: List[str] = None,
                 headers: List[str] = None, max_rows: int = 0):
        super().__init__(id, title=title)
        self.headers = self.register_property('headers', headers)
        self.rows = list(rows) if rows is not None else []
        self.max_rows = max_rows

    @property
    def state(self):
        return {
            "headers": self.headers,
            "rows": self.rows
        }

    def add_row(self, row):
        if self.max_rows and len(self.rows) >= self.max_rows:
            self.rows.pop()
        self.rows.insert(0, row)
        self.emit_state()


class Statistic(Component):
    def __init__(self, id: str, title: str = None, unit: str = None,
                 description: str = None, icon: str = None):
        super().__init__(id, title=title)
        self.value = self.register_property('value', 0)
        self.unit = self.register_property('unit', unit)
        self.description = self.register_property('description', description)
        self.icon = self.register_property('icon', icon)

    @property
    def state(self):
        return {
            "value": self.value,
            "unit": self.unit,
            "description": self.description,
            "icon": self.icon
        }


class ProgressBar(Component):
    def __init__(self, id: str, title: str = None, style: str = 'info', label: bool = False,
                 striped: bool = False, animated: bool = False):
        super().__init__(id, title=title)
        self.value = self.register_property('value', 0)
        self.style = self.register_property('style', style)
        self.label = self.register_property('label', label)
        self.striped = self.register_property('striped', striped)
        self.animated = self.register_property('animated', animated)

    @property
    def state(self):
        return {
            'value': self.value,
            'style': self.style,
            'label': self.label,
            'striped': self.striped,
            'animated': self.animated
        }
