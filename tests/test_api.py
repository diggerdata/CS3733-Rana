import pytest

from rana import app, db

participant_code = None
organizer_code = None

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
    db.create_all()
 
    yield db
    
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

def test_extend_schedule(client, init_db):
    pass

def test_create_meeting(client, init_db):
    response = client.post('/schedule/1/timeslot/1', json={
        "email": "test@example.com"
    }, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

    response = client.post('/schedule/1/timeslot/1', json={
        "username": "diggerdata",
        "email": "test@example.com"
    }, follow_redirects=True)
    json_data = response.get_json()
    global participant_code
    participant_code = json_data['secret_code']
    assert json_data['status'] == 'success'

    response = client.get('/schedule/1', follow_redirects=True)
    json_data = response.get_json()
    assert json_data['timeslots'][0]['meeting'] is not None

def test_get_meeting(client, init_db):
    global participant_code
    response = client.get('/schedule/1/meeting/' + participant_code, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['username'] == 'diggerdata'

def test_close_meeting(client, init_db):
    response = client.delete('/schedule/1/timeslot/1', 
        headers={'Authorization': participant_code}, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    
    response = client.delete('/schedule/1/timeslot/1', follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'