from application.models import db, Notification, SalonConfig, Staff, StaffAttendance
import datetime

def mark_absent_staff():
    """
    Fetch ATTENDANCE_THRESHOLD_TIME from SalonConfig.
    Mark staff as absent (present_flag=False) if they haven't marked attendance by then.
    """
    from main import scheduler
    with scheduler.app.app_context():
        # 1. Get the threshold time from config
        config = SalonConfig.query.filter_by(param_name='ATTENDANCE_THRESHOLD_TIME').first()
        if not config:
            print("Scheduled Task: ATTENDANCE_THRESHOLD_TIME not found in SalonConfig.")
            return
        
        today = datetime.date.today()
        
        # 2. Get all staff IDs
        all_staff_ids = [s.staff_id for s in Staff.query.all()]
        
        # 3. Get staff who already marked attendance today
        attended_staff_ids = [
            a.staff_id for a in StaffAttendance.query.filter(
                db.func.date(StaffAttendance.register_datetime) == today
            ).all()
        ]
        
        # 4. Identify missing staff
        missing_staff_ids = set(all_staff_ids) - set(attended_staff_ids)
        
        # 5. Mark them as absent
        for s_id in missing_staff_ids:
            absent_record = StaffAttendance(
                staff_id=s_id,
                register_datetime=datetime.datetime.now(),
                present_flag=False
            )
            db.session.add(absent_record)
        
        db.session.commit()
        print(f"Scheduled Task Run: Marked {len(missing_staff_ids)} staff members as absent for {today}.")
        
        # Calling follow-up methods
        send_absence_notifications(missing_staff_ids)
        log_task_completion("Attendance Cleanup")


def send_absence_notifications(staff_ids):
    """Notify the manager about absent staff members using the Notification system."""
    if not staff_ids:
        return
    
    from application.models import Staff, Manager, Notification
    
    # 1. Fetch manager to notify (assuming there is at least one manager to receive the system alert)
    manager = Manager.query.first()
    if not manager:
        print("Follow-up: No manager found to notify.")
        return

    # 2. Iterate through absent staff and create a notification for each
    for s_id in staff_ids:
        staff = Staff.query.get(s_id)
        if staff:
            subject = f"Staff Absent: {staff.staff_name}"
            body = (f"Staff member {staff.staff_name} (ID: {staff.staff_id}) was marked absent today. "
                    f"Contact: {staff.staff_contact}, Email: {staff.staff_email}")
            
            # Create internal App Notification for the manager
            new_note = Notification(
                user_id=manager.manager_id,
                subject=subject,
                message=body,
                phone_number=staff.staff_contact, # Using staff contact as reference
                is_read=False
            )
            db.session.add(new_note)
            print(f"Follow-up: Generated 'Staff Absent' notification for {staff.staff_name}")
    
    db.session.commit()


def log_task_completion(task_name):
    """Generic logging method."""
    print(f"Follow-up: {task_name} finished successfully at {datetime.datetime.now()}.")


def daily_notification_cleanup():
    """Example: Mark notifications older than 30 days as read or delete them."""
    from main import scheduler
    with scheduler.app.app_context():
        limit = datetime.datetime.now() - datetime.timedelta(days=30)
        old_notifications = Notification.query.filter(Notification.created_at < limit, Notification.is_read == False).all()
        for note in old_notifications:
            note.is_read = True
        db.session.commit()
        print(f"Scheduled Task Run: Cleaned up {len(old_notifications)} notifications.")

def send_daily_reminder():
    """Example: Send a generic reminder every day at a specific time."""
    from main import scheduler
    with scheduler.app.app_context():
        print("Scheduled Task Run: Sending daily reminders...")
        # Add logic here to send emails or create notification records
