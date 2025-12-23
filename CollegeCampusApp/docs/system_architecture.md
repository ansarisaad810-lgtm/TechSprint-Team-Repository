# System Architecture

## Overview
The app is a hybrid mobile application using **Cordova** for Android.  
It consists of:

### Frontend
- HTML, CSS, JavaScript
- Modular JS files for each feature
- Pages for helpdesk, attendance, lost & found, timetable, study materials

### Backend
- Python Flask REST API
- SQLite database
- Google Gemini API integration for duplicate image detection
- Uploads folder structure:
  - `/uploads/issues`
  - `/uploads/lostfound`
  - `/uploads/materials`

### Data Flow
1. Student reports issue → Image uploaded → Gemini detects duplicates → Admin notified
2. Attendance marked by faculty → Analytics updated in real-time
3. Lost & found → Items tracked with ERP verification
4. Study materials → Organized by branch/year/semester
