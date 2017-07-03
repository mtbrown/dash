import abc
import datetime
from enum import Enum
from threading import RLock
from typing import Any, Iterable, Iterator

from dash.component import Component


class ChartScale(Enum):
    Category = "category"
    Linear = "linear"
    Logarithmic = "logarithmic"
    Time = "time"
    RadialLinear = "radialLinear"


class ChartColor(Enum):
    Blue = (54, 162, 235)
    Red = (255, 99, 132)
    Yellow = (255, 206, 86)
    Green = (75, 192, 192)
    Purple = (153, 102, 255)
    Pink = (255, 153, 204)
    Orange = (255, 159, 64)
    Grey = (128, 128, 128)


def color_generator() -> Iterator[ChartColor]:
    while True:
        for color in ChartColor:
            yield color


class Dataset:
    id_counter = 0
    id_lock = RLock()

    def __init__(self, label: str, color: ChartColor = ChartColor.Blue, line_tension: float = None,
                 point_radius: float = None, fill: bool = False):
        self.data = []
        self.label = label
        self.fill = fill
        self.color = color
        self.line_tension = line_tension
        self.point_radius = point_radius

        with self.id_lock:
            self.id = self.id_counter
            self.id_counter += 1

    @property
    def state(self):
        state = {
            'label': self.label,
            'fill': self.fill,
            'backgroundColor': 'rgba({0}, {1}, {2}, 0.4)'.format(*self.color.value),
            'borderColor': 'rgba({0}, {1}, {2}, 1)'.format(*self.color.value),
            'borderWidth': 2,  # required for border around bar chart bars
            'data': self.data
        }
        if self.line_tension is not None:
            state['lineTension'] = self.line_tension
        if self.point_radius is not None:
            state['pointRadius'] = self.point_radius

        return state


class Chart(Component):
    __metaclass__ = abc.ABCMeta

    # Require that subclasses define chart_type property
    @abc.abstractproperty
    def chart_type(self):
        raise NotImplementedError

    def __init__(self, id: str, min_y: float = None, max_y: float = None, max_points: int = 0,
                 description: str = None, num_datasets: int = 1, line_tension: float = None,
                 point_radius: float = None, fill: bool = False):
        super().__init__(id)
        self.min_y = min_y
        self.max_y = max_y
        self.max_points = 0
        self.description = description
        self.max_points = max_points
        self.x_scale = ChartScale.Category
        self.labels = []
        self.datasets = []
        self.line_tension = line_tension
        self.point_radius = point_radius
        self.fill = fill

        self.num_datasets = num_datasets

    @property
    def num_datasets(self):
        return len(self.datasets)

    @num_datasets.setter
    def num_datasets(self, value):
        # Clear all current data
        self.labels = []
        self.datasets = []

        colors = color_generator()
        for i in range(value):
            self.datasets.append(Dataset("Dataset {i}".format(i=i), color=next(colors), line_tension=self.line_tension,
                                         point_radius=self.point_radius, fill=self.fill))

    @property
    def state(self):
        cur_state = {
            "type": self.chart_type,
            "data": {
                "labels": self.labels,
                "datasets": [d.state for d in self.datasets]
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
        self.datasets[0].data.append(value)
        self.emit_state()

    def update_bar(self, label: str, value: float):
        data_index = self.labels.index(label)
        self.datasets[0].data[data_index] = value
        self.emit_state()

    def remove_bar(self, label: str):
        data_index = self.labels.index(label)
        self.labels.pop(data_index)
        self.datasets[0].data.pop(data_index)
        self.emit_state()


class LineChart(Chart):
    chart_type = 'line'

    def add_data(self, label: Any, *values: Iterable[float]):
        if len(self.labels) > self.max_points > 0:
            self.labels.pop(0)
            for dataset in self.datasets:
                dataset.data.pop(0)

        self.labels.append(label)
        for i, value in enumerate(values):
            self.datasets[i].data.append(value)

        self.emit_state()

    def add_data_time(self, time: datetime.datetime, *values: Iterable[float]):
        self.add_data(time.isoformat(), *values)

    def add_data_now(self, *values: Iterable[float]):
        self.add_data(datetime.datetime.now().isoformat(), *values)
