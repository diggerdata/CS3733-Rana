import os
import tempfile

import pytest

from rana import app, db


@pytest.fixture(scope='module')
def client():
    app.config.from_object('config.TestingConfig')
    client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

@pytest.fixture(scope='module')
def init_db():
    # Create the database and the database table
    db.create_all()
    # db.session.no_autoflush()
 
    yield db  # this is where the testing happens!
    
    db.session.remove()
    db.drop_all()

def test_create_schedule(client, init_db):
    response = client.post('/schedule/',
        json={
            "name": "Test2",
            "start_date": "2018-12-04T9:00:00.00Z",
            "end_date": "2018-12-25T17:00:00.00Z",
            "duration": 15,
            "username": "diggerdata",
            "email": "thing@thing.com",
            "hours": 8
        },
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    response = client.post('/schedule/',
        json={
            "name": "Test2",
            "start_date": "2018-12-04T9:00:00.00Z",
            "end_date": "2018-12-25T17:00:00.00Z",
            "duration": 15,
            "username": "diggerdata",
            "email": "thing@thing.com",
            "hours": 8
        },
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

def test_get_schedule(client, init_db):
    response = client.get('/schedule/1', follow_redirects=True)
    json_data = response.get_json()
    assert 'name' in json_data
    response = client.get('/schedule/100', follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

# def test_extend_schedule(client, init_db):
