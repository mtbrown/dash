from .panel import Panel
from flask import render_template
from .. import socketio


class Text(Panel):
    def __init__(self, title=None, text=""):
        super(Text, self).__init__()
        self.title = title
        self.text = text

    def update(self, text):
        self.text = text
        for container in self.containers:
            socketio.emit(self.id, text, namespace='/' + container.name)

    def render_html(self):
        return render_template('text.html', id=self.id, text=self.text)

    def render_js(self):
        return render_template('text.js', id=self.id)


class Table(Panel):
    def __init__(self, title=None, rows=None, headers=None, max_rows=None):
        super(Table, self).__init__()
        self.title = title
        self.headers = headers
        self.rows = list(rows) if rows is not None else []
        self.max_rows = max_rows

    def add_row(self, row):
        if self.max_rows and len(self.rows) >= self.max_rows:
            self.rows.pop()
        self.rows.insert(0, row)

        for container in self.containers:
            socketio.emit(self.id, row, namespace='/' + container.name)

    def render_html(self):
        return render_template('table.html', id=self.id, headers=self.headers, rows=self.rows)

    def render_js(self):
        return render_template('table.js', id=self.id, max_rows=self.max_rows)

