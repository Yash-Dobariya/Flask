from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine
from typing import Any, Generator
from src.database import db
import psycopg2, pytest, uuid, jwt
from src.app import create_app
from src.config import Config
from flask import Flask
from flask.testing import FlaskClient
from pytest_factoryboy import register
from tests.factories import (
    UserFactory,
    ImagePostFactory,
)
from faker import Factory as FakerFactory
from datetime import datetime, timedelta

faker = FakerFactory.create()

register(UserFactory)
register(ImagePostFactory)

from urllib.parse import urlparse

uri = urlparse(Config.SQLALCHEMY_DATABASE_URI)
USER_NAME = uri.username
PASSWORD = uri.password
HOST = uri.hostname
PORT = uri.port
DB_NAME = uri.path[1:]

@pytest.fixture(scope="session", autouse=True)
def create_db():
    conn = psycopg2.connect(
        user=USER_NAME,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    """database query"""
    create_db_query = f"CREATE DATABASE {DB_NAME}"
    drop_db_query = f"DROP DATABASE IF EXISTS {DB_NAME}"
    db_exists_query = f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'"
    
    cursor.execute(db_exists_query)
    db_exists = cursor.fetchone()
    
    if db_exists:
        cursor.execute(drop_db_query)
    
    cursor.execute(create_db_query)
    
    yield
    
    # cursor.execute(drop_db_query)
    
    # conn.close()


@pytest.fixture(scope="function")
def engine():
    return create_engine(Config.SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope="function")
def persistent_db_session(engine: Engine) -> Generator[Session, Any, None]:
    """
    Creates a fresh sqlalchemy session for each test that operates in a
    transaction. The transaction is rolled back at the end of each test ensuring
    a clean state.
    """

    # connect to the database
    connection = engine.connect()
    # bind an individual Session to the connection
    session = Session(bind=connection)

    yield session  # use the session in tests.

    session.close()
    # return connection to the Engine
    connection.close()
    engine.dispose()


@pytest.fixture(scope="function")
def app(engine: Engine) -> Generator[Flask, Any, None]:
    """
    Create a fresh database on each test case.
    """
    db.Model.metadata.create_all(bind=engine)  # Create the tables.

    _app = create_app()

    @_app.teardown_request
    def teardown_request(exception):
        db.session.rollback()
        db.session.remove()

    yield _app

    db.Model.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def client(app: Flask) -> Generator[FlaskClient, Any, None]:
    """
    Create a new Flask TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    yield app.test_client()


# Fixture for Seeding the data to database
def persist_object(db: Session, object):
    db.add(object)
    db.commit()
    return object

pytest.persist_object = persist_object


@pytest.fixture
def seed(request: pytest.FixtureRequest, persistent_db_session: Session):
    marker = request.node.get_closest_marker("seed_data")
    if not (marker and marker.args and isinstance(marker.args, tuple)):
        print("_______________________________________________________")
        print("    There is no seed data or not a valid seed data.    ")
        print("-------------------------------------------------------")
        assert False
    
    for dataset in marker.args:
        entity_name, overridden_attributes = dataset

        factory = request.getfixturevalue(entity_name + "_factory")
        
        if isinstance(overridden_attributes, dict):
            pytest.persist_object(
                persistent_db_session, factory(**overridden_attributes)
            )
        elif isinstance(overridden_attributes, list):
            for attribute_set in overridden_attributes:
                pytest.persist_object(persistent_db_session, factory(**attribute_set))

IDENTIFIERS = {}

def id_for(key):
    if key not in IDENTIFIERS:
        IDENTIFIERS[key] = str(uuid.uuid4())
    return IDENTIFIERS[key]

pytest.id_for = id_for

def token_for(user_id: dict, exp=3600):
    exp = datetime.utcnow() + timedelta(seconds=exp)
    payload =  jwt.encode({**user_id, "exp": exp}, Config.JWT_SECRET_KEY, algorithm="HS256")
    return f"Bearer {payload}"

pytest.token_for = token_for
