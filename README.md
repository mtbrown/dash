[![Build Status](https://travis-ci.org/mtbrown/dash.svg?branch=master)](https://travis-ci.org/mtbrown/dash)

# Dash

Dash provides a central framework for the management, scheduling, and monitoring of Python scripts. The project, although functional, is still under active development and the API is subject to change.

#### Features
* Automatically executes scripts according to configurable schedules.
* A web application provides a central location for the monitoring of all your scripts.
* Scripts can output to UI components such as tables, statistics, and charts.
* All UI components are updated dynamically using websockets so information is always up to date.

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
To truly understandy the power of Dash, let's build a simple script. In this case, the script will use random data. In practice, this would hopefully be more interesting data such as readings from a sensor or the results of an API call.

All scripts reside in `/dash/scripts/`. Let's create a new directory `/dash/scripts/sample`.

To begin, let's define the UI grid of the script in `/sample/layout.html`. This declares the layout of the UI components that will make up the dashboard of the script. Let's add a text element that displays the current value, a table for previous values, and a line chart that plots the values.
```
<Grid>
    <Row>
        <Col md=12>
            <Text id="text" />
        </Col>
    </Row>
    <Row>
        <Col md=6>
            <Table id="table" />
        </Col>
        <Col md=6>
            <LineChart id="chart" />
        </Col>
    </Row>
</Grid>
```

Next, let's add the Python code that generate the values and update the UI components. This will be in `/sample/sample.py`, but the name is arbitrary and the main function of the script can be in any Python module or package within the `/sample` directory.

Script entry points are marked with a `dash.hooks.*` decorator. A `panel` object is passed as an argument to these functions when they are run which provides access to all of the UI components and a store dictionary.
```
import dash
from datetime import timedelta
from random import randint


@dash.hooks.setup
def setup(panel):
    # store is used for state storage across multiple executions
    panel.store['count'] = 0

    # perform one-time configuration UI components
    panel.components['table'].headers = ['Count', 'Value']
    panel.components['table'].max_rows = 10  # only show last 10 values
    panel.components['chart'].max_points = 10  # only plot last 10 values


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def update(panel):
    val = randint(0, 100)
    count = panel.store['count']  # retrieve current count

    panel.components['text'].text = 'The current value is: {0}'.format(val)
    panel.components['table'].add_row([count, val])
    panel.components['chart'].add_data(count, val)

    panel.store['count'] += 1
```

This will result in the following script dashboard:
![](http://i.imgur.com/ngAaF27.png)

## Usage
Execute the script by running `dash.py`.
```
$ python dash.py
```

## License

TODO: Write license