from flask import render_template
import abc
import logging
import logging.handlers
import queue
import jinja2

from dash import app, socketio

LOG_LINES = 50


class FixedQueueHandler(logging.Handler):
    """
    This handler sends logging records to a fixed-length queue. When the queue becomes full,
    the oldest record is removed to make room for the newest record. The maximum size of the
    queue is handled inside of the queue constructor rather than the handler.
    """
    def __init__(self, queue):
        super(FixedQueueHandler, self).__init__()
        self.queue = queue

    def emit(self, record):
        if self.queue.full():
            self.queue.get_nowait()  # delete oldest record if full
        self.queue.put_nowait(record)


class Grid:
    def __init__(self, name):
        self.name = name  # name of plugin that owns grid
        self.panels = []

        # prepare logger
        self.logger = logging.Logger(name)
        self.logger_queue = queue.Queue(maxsize=LOG_LINES)
        handler = FixedQueueHandler(self.logger_queue)
        self.logger.addHandler(handler)

    def add(self, panel):
        panel.containers.append(self)
        self.panels.append(panel)

    def remove(self, panel):
        panel.containers.remove(self)
        self.panels.remove(panel)


class Panel:
    id_counter = 0

    def __init__(self):
        self.containers = []  # grids that panel is currently contained in
        self.id = "panel" + str(Panel.id_counter)
        Panel.id_counter += 1

    @abc.abstractmethod
    def render_html(self):
        return

    @abc.abstractmethod
    def render_js(self):
        return


class LiveTextBox(Panel):
    def __init__(self, title=None, text=""):
        super(LiveTextBox, self).__init__()
        self.title = title
        self.text = text

    def update(self, text):
        self.text = text
        for container in self.containers:
            socketio.emit(self.id, text, namespace='/' + container.name)

    def render_html(self):
        return render_template('textbox.html', id=self.id, text=self.text)

    def render_js(self):
        return render_template('textbox.js', id=self.id)


class Table(Panel):
    def __init__(self, title=None, rows=None, headers=None, max_rows=None):
        super(Table, self).__init__()
        self.title = title
        self.headers = headers
        self.rows = list(rows) if rows is not None else []
        self.max_rows = max_rows

    def add_row(self, row):
        # self.rows.append(row)
        for container in self.containers:
            with app.app_context():
                row_html = render_template('table_row.html', row=row)
                socketio.emit(self.id, row_html, namespace='/' + container.name)

    def render_html(self):
        return render_template('table.html', id=self.id, headers=self.headers, rows=self.rows)

    def render_js(self):
        return render_template('table.js', id=self.id)
