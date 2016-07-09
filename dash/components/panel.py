import abc


class Panel:
    id_counter = 0

    def __init__(self):
        self.containers = []  # grids that panel is currently contained in
        self.id = "panel" + str(Panel.id_counter)
        Panel.id_counter += 1

    @abc.abstractmethod
    def render_html(self):
        return

    @abc.abstractmethod
    def render_js(self):
        return
