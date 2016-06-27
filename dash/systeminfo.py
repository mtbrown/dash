import psutil
import threading

from dash import socketio, app
from flask import render_template


def humanize(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Y', suffix)


# Socket IO thread and listeners
@app.route('/system')
def system():
    return render_template('system.html',
                           title="System",
                           num_cpus=psutil.cpu_count(),
                           mem_total=humanize(psutil.virtual_memory().total))


class SystemInfoThread(threading.Thread):
    def __init__(self):
        super(SystemInfoThread, self).__init__()
        self._stop = threading.Event()
        self.daemon = True

    @staticmethod
    def cpu_usage():
        return psutil.cpu_percent(interval=1, percpu=True)  # blocks for |interval| seconds

    @staticmethod
    def mem_usage():
        mem_info = psutil.virtual_memory()
        mem_used = humanize(mem_info.active)
        return mem_used, mem_info.percent

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self):
        while not self._stop.is_set():
            info = {
                'cpu': self.cpu_usage(),
                'mem': self.mem_usage()
            }

            socketio.emit('info', info, namespace="/sysinfo")
        print("Stopping")


thread = None


@socketio.on('connect', namespace="/sysinfo")
def connect():
    global thread
    print("Client connected")

    print("Starting thread")
    thread = SystemInfoThread()
    thread.start()


@socketio.on('disconnect', namespace="/sysinfo")
def disconnect():
    global thread
    print("Client disconnected")
    thread.stop()
