[![Build Status](https://travis-ci.org/mtbrown/dash.svg?branch=master)](https://travis-ci.org/mtbrown/dash)

# Dash
Dash provides a central framework for the management, scheduling, and monitoring of Python scripts. 

The goal of this project is to allow users to easily create dynamic dashboards to monitor the state of Python 
scripts without having to worry about front-end code or the API layer.

The project, although functional, is still under active development and the API is subject to change.

#### Features
* Automatically executes scripts according to configurable schedules.
* A web application provides a central location for the monitoring of all of your scripts.
* Scripts can output to UI components such as text boxes, tables, and charts.
* All UI components are updated in real-time using websockets so information is always up to date.

#### Screenshots
![](http://i.imgur.com/9vbY9B0.png)

## Installation

```
$ git clone https://github.com/mtbrown/dash.git
$ cd dash
$ pip install -r requirements.txt
```
TODO: build client

## Sample Script
To truly understand the power of Dash, let's build a simple script. The script will generate random data 
which is added to a table and plotted in real-time. In practice, this would hopefully be more 
interesting data such as readings from a sensor or the results of an API call.

All scripts reside in `dash/scripts/`. Let's create a new script file `dash/scripts/sample.py`. 

Scripts are defined in classes that extend the `dash.Script` class. The `__init__` method of the script must call 
`__init__` method of the super class and provide a unique `id`. The `__init__` method should also create all of the
components used in the script's dashboard. We will create a `Text` component to display the current value, a `Table`
component to display the 10 most recent values, and a `LineChart` component to plot the most recent values.

The execution entry points of the script are marked using decorators. We will define a single method, `update()`, 
that generates a new value and updates the text, table, and chart components on the dashboard. To mark this
method to be executed on a schedule, the `@dash.hooks.schedule()` decorator is used. This decorator accepts a 
`timedelta` object as a parameter which describes how frequently the method is executed. In this case, we will have 
it execute once every second.

Finally, the layout of the dashboard of our script must be defined in the `render()` method of the script. 
The `Grid`, `Row`, and `Col` classes are used to describe the layout of the components in terms of nested rows and 
columns. The `render()` method must 
return an instance of `Grid`. We will put the text on top in it's own row, and the table and chart side-by-side down 
below. To do this, we will nest two `Row` instances within our `Grid`. The second `Row` will contain two `Col` 
instances which contain the table and chart components.

The complete `sample.py` file can be seen below. There is no need to instantiate the class; this will be done by
the framework.

```
import dash
from dash.grid import Grid, Col, Row
from dash.components import Text, Table, LineChart

from datetime import timedelta
from random import randint


class SampleScript(dash.Script):
    def __init__(self):
        super().__init__(id='sample')

        self.count = 0

        # Create components
        self.text = Text(id='sample_text')
        self.table = Table(id='table', headers=['Count', 'Value'], max_rows=10)
        self.chart = LineChart(id='chart', max_points=10)

    @dash.hooks.schedule(run_every=timedelta(seconds=1))
    def update(self):
        val = randint(0, 100)  # generate new value

        # Add new value to table and chart
        self.text.text = 'The current value is: {0}'.format(val)
        self.table.add_row([self.count, val])
        self.chart.add_data(self.count, val)

        self.count += 1

    def render(self):
        return Grid(
            Row(
                Col(self.text, md=12),
            ),
            Row(
                Col(self.table, md=6),
                Col(self.chart, md=6)
            )
        )

```

When the main `dash.py` is executed, the script will be automatically discovered and added to the scheduler. The
`update()` function should execute every second and the dashboard will update in real-time with the new values.

This will result in the following script dashboard:
![](http://i.imgur.com/ngAaF27.png)

## Usage
Execute the program by running `dash.py`. All scripts defined in `dash/scripts/` will be automatically discovered
and executed.
```
$ python dash.py
```

## License

TODO: Write license