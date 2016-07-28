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

    def __init__(self, title=None):
        super(Chart, self).__init__()
        self.title = title
        self.labels = []
        self.data = []
        self.x_scale = ChartScale.Category

    def render_html(self):
        return render_template('chart.html', id=self.id)

    def render_js(self, **kwargs):
        return render_template('chart.js', id=self.id, chart_type=self.chart_type, labels=self.labels,
                               data=self.data, x_scale=self.x_scale, **kwargs)


class BarChart(Chart):
    chart_type = 'bar'

    def add_bar(self, label, value):
        self.labels.append(label)
        self.data.append(value)
        self.emit(['add', [label, value]])

    def update_bar(self, label, value):
        data_index = self.labels.index(label)
        self.data[data_index] = value
        self.emit(['update', [data_index, value]])

    def remove_bar(self, label):
        data_index = self.labels.index(label)
        self.labels.pop(data_index)
        self.data.pop(data_index)
        self.emit(['remove', data_index])


class LineChart(Chart):
    chart_type = 'line'

    def __init__(self, title=None, max_points=0):
        super().__init__(title=title)
        self.max_points = max_points

    def add_point(self, label, value):
        if len(self.labels) > self.max_points > 0:
            self.labels.pop(0)
            self.data.pop(0)
        self.labels.append(label)
        self.data.append(value)
        self.emit(['add', [label, value]])

    def render_js(self, **kwargs):
        return super().render_js(max_points=self.max_points)
