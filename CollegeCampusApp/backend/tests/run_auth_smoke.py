from backend.app import create_app

app = create_app()
client = app.test_client()
# Register a user
resp = client.post('/api/auth/register', json={'name':'Test User','roll_no':'123456','password':'secret'})
print('register status', resp.status_code, resp.get_json())
# Login user
resp2 = client.post('/api/auth/login', json={'erp':'123456','password':'secret'})
print('login status', resp2.status_code, resp2.get_json())
