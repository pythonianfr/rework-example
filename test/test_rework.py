from pathlib import Path

import pytest
from sqlalchemy import create_engine
from pytest_sa_pg import db

from rework import (
    api,
    schema,
    task
)
from rework.testutils import workers

# our test tasks
from example import tasks as _tasks  # noqa


DATADIR = Path(__file__).parent / 'data'
PORT = 2346


@pytest.fixture(scope='session')
def engine(request):
    db.setup_local_pg_cluster(request, DATADIR, PORT, {
        'timezone': 'UTC',
        'log_timezone': 'UTC'
    })
    e = create_engine('postgresql://localhost:{}/postgres'.format(PORT))
    schema.init(e, drop=True)
    api.freeze_operations(e)
    return e



def test_hello(engine):
    with workers(engine):
        t = api.schedule(engine, 'helloworld')
        t.join()

        assert t.state == 'done'
        assert 'Hello world from Babar' in t.logs()[0][1]


def test_fail(engine):
    with workers(engine):
        t = api.schedule(engine, 'failing')
        t.join()

        assert t.state == 'failed'
        assert 'Oops' in t.traceback


def test_abort(engine):
    with workers(engine):
        t = api.schedule(engine, 'looping')

        try:
            t.join(timeout=1)
        except task.TimeOut:
            # this will loop forever
            pass

        # only one option: forcefully abort it
        t.abort()

        assert t.state in ('aborting', 'aborted')


def test_hello_2(engine):
    with workers(engine, domain='timeseries'):
        t = api.schedule(engine, 'helloworld_2')
        t.join()
        assert 'Hello world from Celeste' in t.logs()[0][1]


def test_hello_with_inputs(engine):
    with workers(engine, domain='timeseries'):
        t = api.schedule(
            engine,
            'helloworld_with_inputs',
            inputdata={}
        )
        t.join()

        log2 = t.logs()[1][1]
        assert "I got the following input dictionary : {'name': 'Celeste'" in log2

        t = api.schedule(
            engine,
            'helloworld_with_inputs',
            inputdata={'name': 'Aurélien', 'birthdate': '(date "1973-5-20")'}
        )
        t.join()

        log2 = t.logs()[1][1]
        assert (
            "I got the following input dictionary : {"
            "'name': 'Aurélien', "
            "'birthdate': datetime.datetime(1973, 5, 20, 0, 0)}"
        ) in log2

        assert t.output == 42



def test_also_with_outputs(engine):
    with workers(engine, numworkers=2, domain='timeseries'):
        t = api.schedule(
            engine,
            'also_with_outputs',
            inputdata={}
        )
        t.join()

        assert t.output == {'computed': 42}

