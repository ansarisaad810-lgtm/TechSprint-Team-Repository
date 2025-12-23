from backend.app import create_app

print('creating app...')
app = create_app()
print('app created')
client = app.test_client()

resp = client.get('/attendance/view/1')
print('status:', resp.status_code)
print('json:', resp.get_json())

resp2 = client.get('/helpdesk/list')
print('helpdesk status:', resp2.status_code)
print('helpdesk json:', resp2.get_json())
