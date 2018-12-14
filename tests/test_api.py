import pytest

from rana import app, db
from rana.models import User

participant_code = None
organizer_code = None
sysadmin_code = None

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
    global organizer_code
    organizer_code = json_data['secret_code']
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

def test_organizer_auth(client, init_db):
    global organizer_code
    response = client.get('/schedule/1/authenticate',
        headers={'Authorization': organizer_code},
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['authorized'] == True

    response = client.get('/schedule/1/authenticate',
        headers={'Authorization': 'asdfasdf'},
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['authorized'] == False

def test_delete_schedule(client, init_db):
    response = client.post('/schedule/',
        json={
            "name": "DelTest",
            "start_date": "2018-12-04T9:00:00.00Z",
            "end_date": "2018-12-25T17:00:00.00Z",
            "duration": 15,
            "username": "diggerdata",
            "email": "thing@thing.com",
            "hours": 8
        },
        follow_redirects=True)
    json_data = response.get_json()
    temp_organizer_code = json_data['secret_code']
    del_id = str(json_data['schedule_id'])

    response = client.delete('/schedule/'+del_id,
        headers={'Authorization': temp_organizer_code},
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.delete('/schedule/'+del_id,
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

def test_get_schedule(client, init_db):
    response = client.get('/schedule/1', follow_redirects=True)
    json_data = response.get_json()
    assert 'name' in json_data

    response = client.get('/schedule/1?week=2018-12-10T00:00:00.00Z', 
        follow_redirects=True)
    json_data = response.get_json()
    assert 'name' in json_data

    response = client.get('/schedule/100', follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

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

def test_extend_schedule(client, init_db):
    global organizer_code
    response = client.post('/schedule/1/end', json={
        "date": "2019-1-06T17:00:00.00Z",
	    "hours": 8
    }, headers={'Authorization': organizer_code}, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.post('/schedule/1/end', json={
        "date": "2019-1-06T17:00:00.00Z",
	    "hours": 8
    }, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

    response = client.post('/schedule/1/end', json={
        "date": "2019-1-06T17:00:00.00Z",
	    "hours": 8
    }, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

    response = client.post('/schedule/1/start', json={
        "date": "2018-12-01T9:00:00.00Z",
	    "hours": 8
    }, headers={'Authorization': organizer_code}, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

def test_query_timeslot(client, init_db):
    response = client.get('/schedule/1/timeslot?hour=9',
        follow_redirects=True)
    json_data = response.get_json()
    assert 'timeslots' in json_data

    response = client.get('/schedule/10/timeslot?hour=9',
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

def test_toggle_timeslot(client, init_db):
    global organizer_code
    response = client.post('/schedule/1/timeslot/2/open',
        headers={'Authorization': organizer_code}, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.post('/schedule/1/timeslot/2/close',
        headers={'Authorization': organizer_code}, follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

def test_toggle_multiple_timeslot(client, init_db):
    global organizer_code
    response = client.post('/schedule/1/timeslot/close?day=2018-12-20T00:00:00.00Z',
        headers={'Authorization': organizer_code}, 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.post('/schedule/1/timeslot/open?day=2018-12-20T00:00:00.00Z',
        headers={'Authorization': organizer_code}, 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.post('/schedule/1/timeslot/open?time=2018-12-20T10:00:00.00Z',
        headers={'Authorization': organizer_code}, 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'success'

    response = client.post('/schedule/1/timeslot/open?day=2018-12-20T00:00:00.00Z', 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['status'] == 'fail'

def test_sysadmin_auth(client, init_db):
    global sysadmin_code
    sysadmin = User('god', 'god@op.com', 'sysadmin')
    sysadmin_code = sysadmin.secret_code

    init_db.session.add(sysadmin)
    init_db.session.commit()

    response = client.get('/sysadmin/authenticate',
        headers={'Authorization': sysadmin_code}, 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['authorized'] == True

    response = client.get('/sysadmin/authenticate',
        headers={'Authorization': 'SDdsfdfaee'}, 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['authorized'] == False

def test_sysadmin_remove_old_schedules(client, init_db):
    global sysadmin_code
    response = client.get('/sysadmin?hours=1',
        headers={'Authorization': sysadmin_code}, 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['num_created'] == 1

    response = client.delete('/sysadmin?days=0',
        headers={'Authorization': sysadmin_code}, 
        follow_redirects=True)
    json_data = response.get_json()
    assert json_data['num_deleted'] == 1
