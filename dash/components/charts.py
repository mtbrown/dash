import abc
from enum import Enum
from .component import Component
from flask import render_template
import datetime
from typing import Any


class ChartScale(Enum):
    Category = "category"
    Linear = "linear"
    Logarithmic = "logarithmic"
    Time = "time"
    RadialLinear = "radialLinear"


class Chart(Component):
    __metaclass__ = abc.ABCMeta

    # Require that subclasses define chart_type property
    @abc.abstractproperty
    def chart_type(self):
        print("Chart class should never be instantiated, only extended")
        raise NotImplementedError

    def __init__(self, id: str, title: str = None, min_y: float = None,
                 max_y: float = None, description: str = None):
        super().__init__(id, title=title)
        self.labels = []
        self.data = []
        self.x_scale = ChartScale.Category
        self.min_y = min_y
        self.max_y = max_y
        self.description = description

    @property
    def state(self):
        cur_state = {
            "type": self.chart_type,
            "data": {
                "labels": self.labels,
                "datasets": [{
                    "label": self.description,
                    "data": self.data,
                    "borderWidth": 1
                }]
            },
            "options": {
                "animation": {
                    "duration": 0
                },
                "scales": {
                    "xAxes": [{
                        "type": self.x_scale.value,
                        "time": {
                            "tooltipFormat": "YYYY-MM-DD hh:mm:ss a"
                        }
                    }],
                    "yAxes": [{
                        "ticks": {}
                    }]
                }
            }
        }
        if self.min_y is not None:
            cur_state["options"]["scales"]["yAxes"][0]["ticks"]["min"] = self.min_y
        if self.max_y is not None:
            cur_state["options"]["scales"]["yAxes"][0]["ticks"]["max"] = self.max_y
        return cur_state


class BarChart(Chart):
    chart_type = 'bar'

    def add_bar(self, label: str, value: float):
        self.labels.append(label)
        self.data.append(value)
        self.emit_state()

    def update_bar(self, label: str, value: float):
        data_index = self.labels.index(label)
        self.data[data_index] = value
        self.emit_state()

    def remove_bar(self, label: str):
        data_index = self.labels.index(label)
        self.labels.pop(data_index)
        self.data.pop(data_index)
        self.emit_state()


class LineChart(Chart):
    chart_type = 'line'

    def __init__(self, id: str, title: str = None, min_y: float = None, max_y: float = None,
                 description: str = None, max_points: int = 0):
        super().__init__(id, title, min_y, max_y, description)
        self.max_points = max_points

    def add_point(self, label: Any, value: float):
        if len(self.labels) > self.max_points > 0:
            self.labels.pop(0)
            self.data.pop(0)
        self.labels.append(label)
        self.data.append(value)
        self.emit_state()

    def add_point_time(self, time: datetime.datetime, value: float):
        self.add_point(time.isoformat(), value)

    def add_point_now(self, value: float):
        self.add_point(datetime.datetime.now().isoformat(), value)
