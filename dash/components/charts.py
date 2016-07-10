from .panel import Panel
from flask import render_template


class BarChart(Panel):
    chart_type = 'bar'

    def __init__(self, title=None, labels=None):
        super(BarChart, self).__init__()
        self.title = title
        self.labels = labels
        self.max_points = 0

    def render_html(self):
        return render_template('chart.html', id=self.id)

    def render_js(self):
        return render_template('chart.js', id=self.id, chart_type=self.chart_type, labels=self.labels,
                               max_points=self.max_points)


class LineChart(Panel):
    chart_type = 'line'

    def __init__(self, title=None, labels=None, max_points=0):
        super(LineChart, self).__init__()
        self.title = title
        self.labels = labels
        self.max_points = max_points

    def render_html(self):
        return render_template('chart.html', id=self.id)

    def render_js(self):
        return render_template('chart.js', id=self.id, chart_type=self.chart_type, labels=self.labels,
                               max_points=self.max_points)

    def add_data(self, x, y):
        self.emit(['add', [x, y]])
