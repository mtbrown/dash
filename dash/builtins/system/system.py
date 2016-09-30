import dash
from dash.components import ChartColor, ChartScale
from datetime import timedelta
import psutil


def humanize(num, suffix='B'):
    units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
    for unit in units:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Y', suffix)


def bytes_to_gigabytes(num):
    return num / (1024.0 ** 3)


@dash.hooks.setup
def setup(panel):
    panel.components['cpu_chart'].x_scale = ChartScale.Time
    panel.components['cpu_chart'].num_datasets = psutil.cpu_count()
    for i, dataset in enumerate(panel.components['cpu_chart'].datasets):
        dataset.label = "CPU {i}".format(i=i)

    panel.components['mem_chart'].x_scale = ChartScale.Time
    panel.components['mem_chart'].datasets[0].color = ChartColor.Red
    panel.components['mem_chart'].datasets[0].label = "Memory Usage (GB)"
    panel.components['mem_chart'].max_y = bytes_to_gigabytes(psutil.virtual_memory().total)


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def update_mem(panel):
    mem_info = psutil.virtual_memory()
    mem_used = mem_info.total - mem_info.available
    panel.components['mem_text'].text = "#### {0} ({1:.2f}%) of {2}".format(
        humanize(mem_used), mem_info.percent, humanize(mem_info.total))
    panel.components['mem_bar'].value = mem_info.percent
    panel.components['mem_chart'].add_data_now(bytes_to_gigabytes(mem_used))


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def update_cpu(panel):
    cpu_usage = psutil.cpu_percent(interval=0.1, percpu=True)
    cpu_percent = sum(cpu_usage) / len(cpu_usage)
    panel.components['cpu_text'].text = "#### {0:.2f}%".format(cpu_percent)
    panel.components['cpu_bar'].value = cpu_percent
    panel.components['cpu_chart'].add_data_now(*cpu_usage)
