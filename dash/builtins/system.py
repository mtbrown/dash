import dash
from dash.grid import Grid, Col, Row
from dash.components import Text, ProgressBar, LineChart, ChartScale, ChartColor

import psutil
from datetime import timedelta


def humanize(num, suffix='B'):
    units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
    for unit in units:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Y', suffix)


def bytes_to_gigabytes(num):
    return num / (1024.0 ** 3)


class DemoGrid(dash.Script):
    def __init__(self):
        super().__init__('system')

        # CPU
        self.cpu_text = Text(id='cpu_text')
        self.cpu_bar = ProgressBar(id='cpu_bar', striped=True, animated=True)
        self.cpu_chart = LineChart(id='cpu_chart', min_y=0, max_y=100, max_points=30, x_scale=ChartScale.Time,
                                   num_datasets=psutil.cpu_count())
        for i, dataset in enumerate(self.cpu_chart.datasets):
            dataset.label = 'CPU {i}'.format(i=i)

        # Memory
        self.mem_text = Text(id='mem_text')
        self.mem_bar = ProgressBar(id='mem_bar', style='danger', striped=True, animated=True)
        self.mem_chart = LineChart(id='mem_chart', min_y=0, max_points=30, x_scale=ChartScale.Time,
                                   max_y=bytes_to_gigabytes(psutil.virtual_memory().total))
        self.mem_chart.datasets[0].color = ChartColor.Red
        self.mem_chart.datasets[0].label = "Memory Usage (GB)"

    @dash.hooks.schedule(run_every=timedelta(seconds=1))
    def update_cpu(self):
        cpu_usage = psutil.cpu_percent(interval=0.1, percpu=True)
        cpu_percent = sum(cpu_usage) / len(cpu_usage)
        self.cpu_text.text = "#### {0:.2f}%".format(cpu_percent)
        self.cpu_bar.value = cpu_percent
        self.cpu_chart.add_data_now(*cpu_usage)

    @dash.hooks.schedule(run_every=timedelta(seconds=1))
    def update_mem(self):
        mem_info = psutil.virtual_memory()
        mem_used = mem_info.total - mem_info.available
        self.mem_text.text = "#### {0} ({1:.2f}%) of {2}".format(
            humanize(mem_used), mem_info.percent, humanize(mem_info.total))
        self.mem_bar.value = mem_info.percent
        self.mem_chart.add_data_now(bytes_to_gigabytes(mem_used))

    def render(self):
        return Grid(
            Row(
                Col(
                    Text(id='cpu_title', text='### CPU'),
                    self.cpu_text,
                    self.cpu_bar,
                    self.cpu_chart,
                    md=6
                ),
                Col(
                    Text(id='mem_title', text='### Memory'),
                    self.mem_text,
                    self.mem_bar,
                    self.mem_chart,
                    md=6
                )
            )
        )
