from .panel import Panel
from flask import render_template


class BarChart(Panel):
    def __init__(self, title=None, labels=None):
        super(BarChart, self).__init__()
        self.title = title
        self.labels = labels

    def render_html(self):
        return render_template('chart.html', id=self.id)

    def render_js(self):
        return render_template('chart.js', id=self.id, labels=self.labels)
