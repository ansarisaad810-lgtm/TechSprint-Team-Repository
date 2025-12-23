from backend.models.attendance import Attendance
from backend.config.settings import ATTENDANCE_CRITERIA

def calculate_attendance(attendance: Attendance):
    percentage = attendance.attendance_percentage()
    classes_needed = attendance.classes_needed_for_criteria(ATTENDANCE_CRITERIA)

    status = "Safe"
    if percentage < ATTENDANCE_CRITERIA:
        status = "Warning"

    return {
        "total_classes": attendance.total_classes,
        "attended_classes": attendance.attended_classes,
        "percentage": percentage,
        "classes_needed": classes_needed,
        "status": status
    }
