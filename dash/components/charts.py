import abc
from enum import Enum
from .panel import Panel
from flask import render_template
import datetime


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

    def __init__(self, title=None, min_y=None, max_y=None, description=None):
        super().__init__(title=title)
        self.labels = []
        self.data = []
        self.x_scale = ChartScale.Category
        self.min_y = min_y
        self.max_y = max_y
        self.description = description

    def render_html(self):
        return render_template('chart.html', id=self.id)

    def render_js(self, **kwargs):
        return render_template('chart.js', id=self.id, chart_type=self.chart_type, labels=self.labels,
                               data=self.data, x_scale=self.x_scale, min_y=self.min_y, max_y=self.max_y,
                               description=self.description, **kwargs)


class BarChart(Chart):
    chart_type = 'bar'

    def add_bar(self, label, value):
        self.labels.append(label)
        self.data.append(value)

    def update_bar(self, label, value):
        data_index = self.labels.index(label)
        self.data[data_index] = value

    def remove_bar(self, label):
        data_index = self.labels.index(label)
        self.labels.pop(data_index)
        self.data.pop(data_index)


class LineChart(Chart):
    chart_type = 'line'

    def __init__(self, title=None, min_y=None, max_y=None, description=None, max_points=0):
        super().__init__(title, min_y, max_y, description)
        self.max_points = max_points

    def add_point(self, label, value):
        if len(self.labels) > self.max_points > 0:
            self.labels.pop(0)
            self.data.pop(0)
        self.labels.append(label)
        self.data.append(value)

    def add_point_time(self, time, value):
        self.add_point(time.isoformat(), value)

    def add_point_now(self, value):
        self.add_point(datetime.datetime.now().isoformat(), value)

    def render_js(self, **kwargs):
        return super().render_js(max_points=self.max_points)
