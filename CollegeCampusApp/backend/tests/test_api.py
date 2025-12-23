import pytest
from backend.app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_helpdesk_list_empty(client):
    resp = client.get('/helpdesk/list')
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

def test_attendance_missing(client):
    resp = client.get('/attendance/view/1')
    assert resp.status_code == 404
    assert resp.get_json().get('error') == 'Attendance record not found'
