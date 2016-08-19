from .panel import Panel
from flask import render_template


class Text(Panel):
    def __init__(self, title=None, text=""):
        super().__init__(title=title)
        self._text = ""
        self.text = text

    @property
    def state(self):
        return {
            "text": self.text
        }

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.emit_state()

    def render_html(self):
        return render_template('text.html', id=self.id, text=self.text)

    def render_js(self):
        return render_template('text.js', id=self.id)


class Table(Panel):
    def __init__(self, title=None, rows=None, headers=None, max_rows=0):
        super().__init__(title=title)
        self.headers = headers
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

    def render_html(self):
        return render_template('table.html', id=self.id, headers=self.headers, rows=self.rows)

    def render_js(self):
        return render_template('table.js', id=self.id, max_rows=self.max_rows)

