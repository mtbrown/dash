import logging
import queue

LOG_LINES = 50
BOOTSTRAP_COLUMNS = 12  # Bootstrap grid system based on 12 columns


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
        self._num_columns = 1  # number of columns the grid contains
        self.columns = [[]]  # list containing a list of panels for each column
        self.panel_columns = {}  # maps panel ids to the column they're contained in

        # prepare logger
        self.logger = logging.Logger(name)
        self.logger_queue = queue.Queue(maxsize=LOG_LINES)
        handler = FixedQueueHandler(self.logger_queue)
        self.logger.addHandler(handler)

    @property
    def num_columns(self):
        return self._num_columns

    @num_columns.setter
    def num_columns(self, num_columns):
        """
        Sets the number of columns for the grid layout. The number of columns must divide evenly
        into 12 (1, 2, 3, 4, 6, 12). If the number of columns becomes smaller than the old
        value, the panels contained in the last columns will be removed.
        """
        if BOOTSTRAP_COLUMNS % num_columns != 0:
            logging.error("Invalid columns value (%d) for grid %s. Value must divide evenly into %d.",
                          num_columns, self.name, BOOTSTRAP_COLUMNS)
            return

        while len(self.columns) < num_columns:
            self.columns.append([])  # add an empty list for each new column
        while len(self.columns) > num_columns:
            for panel in self.columns[-1]:
                panel.containers.remove(self)
            self.columns.pop(-1)
        self._num_columns = num_columns

    def add(self, panel, column=0):
        if column < 0 or column >= self._num_columns:
            logging.error("Unable to add panel %d to grid %s, invalid column index %d.",
                          panel.id, self.name, column)
            return
        if panel.id in self.panel_columns:
            logging.info("Attempted to add duplicate panel %d to grid %s, ignoring.",
                         panel.id, self.name)
            return

        panel.containers.append(self)  # add self to panel's container list
        self.panel_columns[panel.id] = column
        self.columns[column].append(panel)

    def remove(self, panel):
        if panel.id not in self.panel_columns:
            logging.info("Attempted to remove non-existent panel %d from grid %s, ignoring.",
                         panel.id, self.name)
            return

        panel.containers.remove(self)
        self.columns[self.panel_columns[panel.id]].remove(panel)
        self.panel_columns.pop(panel.id)
