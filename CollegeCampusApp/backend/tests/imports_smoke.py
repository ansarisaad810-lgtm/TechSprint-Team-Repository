# quick import smoke test
modules = [
    'backend.app',
    'backend.routes.attendance_routes',
    'backend.routes.helpdesk_routes',
    'backend.routes.lostfound_routes',
    'backend.routes.materials_routes',
    'backend.routes.timetable_routes',
    'backend.routes.student_routes',
    'backend.routes.auth_routes',
    'backend.services.gemini_service',
    'backend.services.issue_classifier',
    'backend.services.attendance_logic',
    'backend.utils.file_utils',
    'backend.utils.validators',
    'backend.utils.auth_utils',
    'backend.models.user',
    'backend.models.request',
    'backend.models.attendance',
    'backend.models.issue',
    'backend.models.lostfound',
    'backend.models.timetable'
]

for m in modules:
    try:
        __import__(m)
        print('OK:', m)
    except Exception as e:
        print('ERROR importing', m, e)
