

class Panel:
    def __init__(self, name):
        self.name = name
        self.grid = []

    def add(self, element):
        pass


class LiveTextBox:
    def __init__(self):
        self.text = ""

    def update(self, text):
        self.text = text
