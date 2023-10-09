import datetime

from rework import api
from rework import io as rio


@api.task
def helloworld(task):
    """This task will run in the `default` domain and, without any
    input specification, won't show up in the rework ui `launcher`
    section.

    """
    with task.capturelogs(std=True):
        # the capturelogs context manager allows to capture logs
        # emitted within its scope; the logs will be available through
        # the rewok ui task section (when you click on a task).
        print(
            f'Hello world from Babar, at time {datetime.datetime.now()}'
        )


@api.task
def failing(task):
    """This task will fail."""
    raise Exception('Oops')


@api.task
def looping(task):
    """This task will loop forever."""
    import time
    while True:
        time.sleep(1)


@api.task(domain='timeseries', inputs=())
def helloworld_2(task):
    """This task will run in the `timeseries` domain and, without an
    empty input specification, will show up in the rework ui
    `launcher` section.

    """
    with task.capturelogs(std=True):
        # with std=True, we not only capture the logs but the output
        # of the print function are also captured at log level INFO
        print(
            f'Hello world from Celeste, at time {datetime.datetime.now()}'
        )


@api.task(domain='timeseries',
      inputs=(
          rio.string('name', default='Celeste'),
          rio.moment('birthdate', default='(date "1920-5-20")')
      ))
def helloworld_with_inputs(task):
    with task.capturelogs(std=True):
        print(
            f'Hello world from Babar, at time {datetime.datetime.now()}'
        )
        print(
            f'I got the following input dictionary : '
            f'{task.input}'
        )

    # Let's save some intermediate result for our clients.
    # Without an output spec in the @task decorator,
    # the value given to .save_output will be simply pickled.
    task.save_output(42)


@api.task(domain='timeseries',
      inputs=(
          rio.string('name', default='Celeste'),
          rio.moment('birthdate', default='(date "1920-5-20")')
      ),
      outputs=(
          rio.number('computed'),
      ))
def also_with_outputs(task):
    with task.capturelogs(std=True):
        print(
            f'Hello world from Babar, at time {datetime.datetime.now()}'
        )
        print(
            f'I got the following input dictionary : '
            f'{task.input}'
        )

        # now, let's run a task by ourselves
        t = api.schedule(
            task.engine,
            'helloworld_with_inputs',
            {'name': 'John Doe'}
        )

        # The task will be queued, run and then be done (or failed).
        # To be sure it is finished, we wait for its completion.
        t.join()

        if t.state == 'failed':
            print(f'Oops. Task {t} failed.')
            return

        print(
            f'Good job {t}. We got {t.output} from you.'
        )

        # We can now finish our job.
        # Since we have an output specification, we can send
        # data there in a structured way.
        task.save_output(
            {'computed': 42}
        )
