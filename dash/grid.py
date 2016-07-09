import logging
import queue

LOG_LINES = 50


class FixedQueueHandler(logging.Handler):
    """
    This handler sends logging records to a fixed-length queue. When the queue becomes full,
    the oldest record is removed to make room for the newest record. The maximum size of the
    queue is handled inside of the queue constructor rather than the handler.
    """
    def __init__(self, queue):
        super(FixedQueueHandler, self).__init__()
        self.queue = queue

    def emit(self, record):
        if self.queue.full():
            self.queue.get_nowait()  # delete oldest record if full
        self.queue.put_nowait(record)


class Grid:
    def __init__(self, name):
        self.name = name  # name of plugin that owns grid
        self.panels = []

        # prepare logger
        self.logger = logging.Logger(name)
        self.logger_queue = queue.Queue(maxsize=LOG_LINES)
        handler = FixedQueueHandler(self.logger_queue)
        self.logger.addHandler(handler)

    def add(self, panel):
        panel.containers.append(self)
        self.panels.append(panel)

    def remove(self, panel):
        panel.containers.remove(self)
        self.panels.remove(panel)