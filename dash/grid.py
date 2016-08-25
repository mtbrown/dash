import inspect
from bs4 import BeautifulSoup, Tag

from . import components


class Grid:
    def __init__(self, layout):
        self.layout = layout
        self.children = []

        soup = BeautifulSoup(layout, 'html.parser')
        if not soup.find('grid'):
            raise ValueError("Invalid layout, missing Grid tag")
        self.children = parse_layout(soup.grid)

    @property
    def state(self):
        return [child.state for child in self.children]


class Row:
    def __init__(self):
        self.children = []

    @property
    def state(self):
        return {
            'type': 'row',
            'children': [child.state for child in self.children]
        }

    def add(self, col):
        if not isinstance(col, Col):
            raise ValueError("Only columns may be immediate children of rows")
        self.children.append(col)


class Col:
    def __init__(self, xs=None, sm=None, md=None, lg=None):
        self.children = []
        self.xs = xs
        self.sm = sm
        self.md = md
        self.lg = lg

    @property
    def state(self):
        return {
            'type': 'col',
            'xs': self.xs,
            'sm': self.sm,
            'md': self.md,
            'lg': self.lg,
            'children': [child.state for child in self.children]
        }

    def add(self, child):
        self.children.append(child)


class BaseComponent:
    def __init__(self, id, type):
        self.type = type
        self.id = id

    @property
    def state(self):
        return {
            'type': self.type,
            'id': self.id
        }


tag_map = {
    'row': Row,
    'col': Col
}

# BeautifulSoup converts all tags to lowercase due to parser limitations
# Maps lowercase class names to properly capitalized names for each component
base_tag_map = {m[0].lower(): m[0] for m in inspect.getmembers(components, inspect.isclass)}


def parse_layout(tag):
    if not isinstance(tag, Tag):
        raise ValueError("Expected a Tag instance")
    tag_children = tag.find_all(True, recursive=False)  # find all children, skipping NavigableStrings

    if tag.name == 'grid':
        return list(map(parse_layout, tag_children))
    if tag.name in base_tag_map:
        return BaseComponent(id=tag.attrs['id'], type=base_tag_map[tag.name])
    if tag.name not in tag_map:
        raise ValueError("Invalid layout tag: {0}".format(tag.name))

    # Search tag attributes for valid parameters to pass to constructor
    valid_params = list(inspect.signature(tag_map[tag.name].__init__).parameters)
    valid_params.remove('self')
    kwargs = {}
    for attr in tag.attrs:
        if attr in valid_params:
            kwargs[attr] = tag.attrs[attr]
    parsed = tag_map[tag.name](**kwargs)

    # Recursively parse child tags
    for child in tag_children:
        parsed.add(parse_layout(child))
    return parsed
