from flask import render_template
import abc
import logging

from dash import socketio


class Grid:
    def __init__(self, name):
        self.name = name  # name of plugin that owns grid
        self.panels = []

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
        self.id = "text{0}".format(LiveTextBox.id_counter)
        LiveTextBox.id_counter += 1

    def update(self, text):
        self.text = text
        for container in self.containers:
            logging.debug('Emitting "{0}" to {1} on namespace {2}'.format(text, self.id, container.name))
            socketio.emit(self.id, text, namespace='/{0}'.format(container.name))

    def render_html(self):
        return render_template('textbox.html', id=self.id, text=self.text)

    def render_js(self):
        return render_template('textbox.js', id=self.id)
