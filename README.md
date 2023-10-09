# A number of examples of rework

## Introduction

Rework is a small task manager using only python and postgres.
Rework tasks can be scheduled on the spot or according to a cron rule.
They can take inputs and yield outputs.
In our examples (tasks module), we show a number of features.

To run the examples:
* install this package (`pip install -e rework-example`)
* install pytest (`pip install pytest`) and just launch it.

Also have a look at the tests in `test/test_rework.py`.


## Simplest possible operation

```python
from rework import api

@api.task
def helloworld(task):
    with task.capturelogs(std=True):
        # the capturelogs context manager allows to caputure logs
        # emitted within its scope; the logs will be available through
        # the rewok ui task section (when you click on a task).
        print(
            f'Hello world from Babar, at time {datetime.datetime.now()}'
        )
```

This shows the basic signature of a task function.
It needs to be decorated with the `@api.task` decorator.
It must be a single-parameter function with a task parameter.

The task object provides a number of convenience features.

The first shown in this example is the `capturelogs` context manager,
which allows to capture logs emitted within its scope; the logs will
be available through the rewok ui task section (when you click on a
task).


# Domains

Domains are nothing more than labels associated with a task.  A domain
is mapped to one (or many) `monitors` (the part of rework that is
responsible to actually run the tasks).

By default, tasks are set into a `default` domain. The `task`
decorator permits to specify the domain in which a task will be put
(hence the monitor that will effectively run it).


```python
@api.task(domain='timeseries')
def helloworld_2(task):
...
```

This is useful for:
* segregating tasks into logical groups
* running python codes that have conflicting dependency requirements
* scaling up the workers pool beyond what a single machine can provide


## Inputs (and Outputs) management

The `task` decorator allows to specify in a structured way the input
(and output) types accepted by a given operation.

```python
from rework import io as rio

@api.task(
      domain='timeseries',
      inputs=(
          rio.string('name', default='Celeste'),
          rio.moment('birthdate', default='(date "1920-5-20")')
      ),
      outputs=(
          rio.number('computed'),
      ))
def also_with_outputs(task):
...
```

In this example, we declare two inputs (with default values), one of
type `string`, the other of type `moment` (a dynamic time expression).

We also declare a one-field output made of a number.

