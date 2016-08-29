import inspect
from bs4 import BeautifulSoup, Tag
from typing import Dict, Any, Union, List, Tuple

from . import components
from .components.component import Component


class Grid:
    def __init__(self):
        self.children = []

    @property
    def state(self):
        return {
            'type': 'Grid',
            'children': [child.state for child in self.children]
        }

    def add(self, child: Union['Row', 'Col']):
        self.children.append(child)


class Row:
    def __init__(self):
        self.children = []

    @property
    def state(self):
        return {
            'type': 'Row',
            'children': [child.state for child in self.children]
        }

    def add(self, col: 'Col'):
        if not isinstance(col, Col):
            raise ValueError("Only Col objects can be added to a row")
        self.children.append(col)


class Col:
    def __init__(self, xs: int = None, sm: int = None, md: int = None, lg: int = None):
        self.children = []
        self.xs = xs
        self.sm = sm
        self.md = md
        self.lg = lg

    @property
    def state(self):
        return {
            'type': 'Col',
            'children': [child.state for child in self.children],
            'props': {key: val for (key, val) in self.__dict__.items() if val is not None
                      and key not in ['children']}
        }

    def add(self, child: Union['Row', 'Col']):
        self.children.append(child)


class BaseComponent:
    def __init__(self, id: str, type: str, ref: Component):
        self.type = type
        self.id = id
        self.ref = ref

    @property
    def state(self):
        return {
            'type': self.type,
            'id': self.id
        }


tag_map = {
    'grid': Grid,
    'row': Row,
    'col': Col
}

# BeautifulSoup converts all tags to lowercase due to parser limitations
# Maps lowercase class names to properly capitalized names for each component
base_tag_map = {m[0].lower(): m[0] for m in inspect.getmembers(components, inspect.isclass)}
base_tag_class_map = {m[0].lower(): m[1] for m in inspect.getmembers(components, inspect.isclass)}


def parse_layout(layout_file) -> Tuple[Grid, List[Component]]:
    """
    Parses the provided layout file and generates the corresponding Grid and list of
    Components.
    :param layout_file: The file containing the layout
    :return: A tuple containing the generated grid and a list of components instantiated
    """
    layout_string = open(layout_file).read()
    layout = BeautifulSoup(layout_string, 'html.parser')
    return create_grid_and_components(layout.grid)


def create_grid_and_components(tag: Tag) -> Tuple[Grid, List[Component]]:
    """
    Recursively traverses the layout tree and generates a Grid tree containing Row, Col, and
    BaseComponent instances. When a base component is reached, the corresponding component
    class is instantiated and added to a component list which is also returned.
    :param tag: The root BeautifulSoup tag of the layout tree.
    :return: A tuple containing the generated grid and a list of components instantiated
    """
    if tag.name in base_tag_map:
        component = construct_with_attrs(base_tag_class_map[tag.name], tag.attrs)
        return BaseComponent(id=tag.attrs['id'], type=base_tag_map[tag.name], ref=component), [component]
    elif tag.name in tag_map:
        parsed = construct_with_attrs(tag_map[tag.name], tag.attrs)
        # Recursively parse child tags, merged returned component lists into master list
        component_list = []
        for child in tag.find_all(True, recursive=False):  # find all direct child tags, ignoring NavigableStrings
            result, sub_list = create_grid_and_components(child)
            parsed.add(result)
            component_list.extend(sub_list)
        return parsed, component_list
    else:
        raise ValueError("Invalid layout tag: {0}".format(tag.name))


def construct_with_attrs(cls, attrs: Dict[str, str]):
    """
    Constructs an instance of a class using an attributes dictionary to fill
    valid constructor key-word parameters.
    :param cls: A class definition
    :param attrs: A dictionary mapping parameter strings to values
    :return: The instantiated object
    """
    # All attribute values will be strings from the parser
    # This dictionary maps types to functions that convert strings to that type
    converters = {
        int: int,
        str: str,
        List: lambda s: s[1:-1].split(', '),
        Any: lambda s: s,
        inspect.Parameter.empty: lambda s: s  # if no type specified, leave string untouched
    }

    params = inspect.signature(cls.__init__).parameters
    valid_params = list(params.keys())
    valid_params.remove('self')  # don't attempt to fill 'self' parameter

    kwargs = {}
    for attr in attrs:
        if attr not in valid_params:
            continue
        param_type = params[attr].annotation
        kwargs[attr] = converters[param_type](attrs[attr])  # convert value and add to argument dictionary
    return cls(**kwargs)
