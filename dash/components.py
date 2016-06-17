from flask import render_template
import abc


class Grid:
    def __init__(self):
        self.panels = []

    def add(self, panel):
        panel.containers.append(self)
        self.panels.append(panel)

    def remove(self, panel):
        panel.containers.remove(self)
        self.panels.remove(panel)

    def render(self):
        return render_template('grid.html', panels=self.panels)


class Panel:
    def __init__(self):
        self.containers = []  # grids that panel is currently contained in

    @abc.abstractmethod
    def render(self):
        return


class LiveTextBox(Panel):
    def __init__(self, title=None):
        super(LiveTextBox, self).__init__()
        self.title = title
        self.text = "hello"  # TODO
        self.id = "text1"  # TODO

    def update(self, text):
        self.text = text

    def render(self):
        return render_template('textbox.html', id=self.id, text=self.text)
