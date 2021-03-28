import os
import tempfile

import pytest

from candy_delivery import create_app
from candy_delivery.db import init_db, get_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Создает и настроивает новый экземпляр приложения для каждого теста."""
    # создает временный файл, чтобы изолировать базу данных для каждого теста
    db_fd, db_path = tempfile.mkstemp()
    # создает приложение с общей тестовой конфигурацией
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
