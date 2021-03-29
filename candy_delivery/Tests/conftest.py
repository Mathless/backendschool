import os
import tempfile

import pytest

from candy_delivery import create_app
from candy_delivery.db import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Creates and configures a new instance of the application for each test."""
    # creates a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # creates an application with a shared test configuration
    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
