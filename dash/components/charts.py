import abc
from enum import Enum
from .panel import Panel
from flask import render_template


class ChartScale(Enum):
    Category = "category"
    Linear = "linear"
    Logarithmic = "logarithmic"
    Time = "time"
    RadialLinear = "radialLinear"


class Chart(Panel):
    __metaclass__ = abc.ABCMeta

    # Require that subclasses define chart_type property
    @abc.abstractproperty
    def chart_type(self):
        print("Chart class should never be instantiated, only extended")
        raise NotImplementedError

    def __init__(self, title=None, labels=None, max_points=0, x_scale=ChartScale.Category):
        super(Chart, self).__init__()
        self.title = title
        self.labels = labels
        self.max_points = max_points
        self.x_scale = x_scale

    def render_html(self):
        return render_template('chart.html', id=self.id)

    def render_js(self):
        return render_template('chart.js', id=self.id, chart_type=self.chart_type, labels=self.labels,
                               max_points=self.max_points, x_scale=self.x_scale)


class BarChart(Chart):
    chart_type = 'bar'

    def add_data(self, label, value):
        self.emit(['add', [label, value]])


class LineChart(Chart):
    chart_type = 'line'

    def add_data(self, label, value):
        self.emit(['add', [label, value]])
