class Grid:
    def __init__(self):
        pass

    def add(self, panel):
        pass


class Panel:
    def __init__(self):
        pass

    def render(self):
        pass


class LiveTextBox(Panel):
    def __init__(self, title=None):
        super(LiveTextBox, self).__init__()
        self.title = title
        self.text = ""

    def update(self, text):
        self.text = text
