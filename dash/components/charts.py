import abc
from enum import Enum
from .component import Component
import datetime
from typing import Any, Iterable, Iterator
from threading import RLock


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

    def __init__(self, label: str, color: ChartColor = ChartColor.Blue, border_color: ChartColor = None,
                 fill: bool = False):
        self.data = []
        self.label = label
        self.fill = fill
        self.color = color
        self.border_color = border_color if border_color else color

        with self.id_lock:
            self.id = self.id_counter
            self.id_counter += 1

    @property
    def state(self):
        return {
            'label': self.label,
            'fill': self.fill,
            'backgroundColor': 'rgba({0}, {1}, {2}, 0.4)'.format(*self.color.value),
            'borderColor': 'rgba({0}, {1}, {2}, 1)'.format(*self.border_color.value),
            'data': self.data
        }


class Chart(Component):
    __metaclass__ = abc.ABCMeta

    # Require that subclasses define chart_type property
    @abc.abstractproperty
    def chart_type(self):
        raise NotImplementedError

    def __init__(self, id: str, title: str = None, min_y: float = None, max_y: float = None, max_points: int = 0,
                 description: str = None, num_datasets: int = 1):
        super().__init__(id, title=title)
        self.min_y = min_y
        self.max_y = max_y
        self.max_points = 0
        self.description = description
        self.max_points = max_points
        self.x_scale = ChartScale.Category
        self.labels = []
        self.datasets = []
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
            self.datasets.append(Dataset("Dataset {i}".format(i=i), color=next(colors)))
        self.emit_state()

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


# class BarChart(Chart):
#     chart_type = 'bar'
#
#     def add_bar(self, label: str, value: float):
#         self.labels.append(label)
#         self.data.append(value)
#         self.emit_state()
#
#     def update_bar(self, label: str, value: float):
#         data_index = self.labels.index(label)
#         self.data[data_index] = value
#         self.emit_state()
#
#     def remove_bar(self, label: str):
#         data_index = self.labels.index(label)
#         self.labels.pop(data_index)
#         self.data.pop(data_index)
#         self.emit_state()


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
