# API Endpoints

## Authentication
- `POST /auth/login` → Login with ERP ID and password
- `POST /auth/register` → Register new user (admin only)

## Help Desk
- `POST /helpdesk/report` → Upload issue
- `GET /helpdesk/list?role=<student|faculty|admin>` → List all issues

## Attendance
- `POST /attendance/mark` → Mark attendance for a student
- `GET /attendance/view/<student_id>` → View attendance analytics

## Lost & Found
- `POST /lostfound/report` → Report found item
- `POST /lostfound/claim` → Claim lost item
- `GET /lostfound/list` → List all lost/found items

## Timetable
- `GET /timetable/section/<section>` → Get section timetable

## Study Materials
- `GET /materials/list` → List study materials
