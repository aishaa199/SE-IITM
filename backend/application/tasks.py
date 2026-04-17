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
            # Check if a notification for this staff member already exists for the manager today
            from sqlalchemy import func
            existing_note = Notification.query.filter(
                Notification.user_id == manager.manager_id,
                Notification.subject == subject,
                func.date(Notification.created_at) == datetime.date.today()
            ).first()

            if not existing_note:
                new_note = Notification(
                    user_id=manager.manager_id,
                    subject=subject,
                    message=body,
                    phone_number=staff.staff_contact, # Using staff contact as reference
                    is_read=False
                )
                db.session.add(new_note)
                print(f"Follow-up: Generated 'Staff Absent' notification for {staff.staff_name}")
            else:
                print(f"Follow-up: Notification already exists today for absent staff {staff.staff_name}")
    
    db.session.commit()


def send_birthday_bonus_notification(customer_ids):
    """Notify customer(s) about their birthday bonus reward points. Supports single ID or list of IDs."""
    from application.models import Customer, Notification
    from main import scheduler
    
    if not isinstance(customer_ids, list):
        customer_ids = [customer_ids]

    with scheduler.app.app_context():
        for c_id in customer_ids:
            customer = Customer.query.get(c_id)
            if not customer:
                print(f"Follow-up: Customer ID {c_id} not found for birthday notification.")
                continue

            subject = "Happy Birthday! Your Bonus is Here"
            body = (f"Happy Birthday, {customer.customer_name}! As a special gift, we have credited "
                    f"bonus reward points to your account. Your current balance is now "
                    f"{customer.customer_available_rewards} points.")
            
            # Create internal App Notification for the customer
            # Check if a notification already exists for this customer today with the same subject
            from sqlalchemy import func
            existing_note = Notification.query.filter(
                Notification.user_id == customer.customer_id,
                Notification.subject == subject,
                func.date(Notification.created_at) == datetime.date.today()
            ).first()

            if not existing_note:
                new_note = Notification(
                    user_id=customer.customer_id, 
                    subject=subject,
                    message=body,
                    phone_number=customer.customer_contact,
                    is_read=False
                )
                db.session.add(new_note)
                print(f"Follow-up: Generated 'Birthday Bonus' notification for {customer.customer_name}")
            else:
                print(f"Follow-up: Birthday notification already exists today for {customer.customer_name}")
        
        db.session.commit()


def log_task_completion(task_name):
    """Generic logging method."""
    print(f"Follow-up: {task_name} finished successfully at {datetime.datetime.now()}.")


def daily_notification_cleanup():
    """Delete notifications older than 30 days."""
    from main import scheduler
    with scheduler.app.app_context():
        limit = datetime.datetime.now() - datetime.timedelta(days=30)
        # Filter notifications older than the limit and delete them
        num_deleted = Notification.query.filter(Notification.created_at < limit).delete()
        
        db.session.commit()
        print(f"Scheduled Task Run: Cleaned up and deleted {num_deleted} notifications.")

def send_daily_reminder():
    """Example: Send a generic reminder every day at a specific time."""
    from main import scheduler
    with scheduler.app.app_context():
        print("Scheduled Task Run: Sending daily reminders...")
        # Add logic here to send emails or create notification records


def check_daily_birthdays():
    """Daily job to check for birthdays in the 15-day window and trigger bonus rewards."""
    from main import scheduler
    from application.models import Customer
    from application.resources import birthday_bonus_rewards
    from datetime import date, timedelta
    
    with scheduler.app.app_context():
        today = date.today()
        all_customers = Customer.query.all()
        birthday_ids = []
        
        for customer in all_customers:
            if customer.customer_dob:
                # Calculate this year's birthday
                try:
                    this_year_bday = date(today.year, customer.customer_dob.month, customer.customer_dob.day)
                except ValueError: # Handle Feb 29
                    this_year_bday = date(today.year, 3, 1)
                
                # Eligibility window: [Birthday - 15 days, Birthday]
                reward_trigger_date = this_year_bday - timedelta(days=15)
                
                # Check if today falls within that window
                if reward_trigger_date <= today <= this_year_bday:
                    # Allocate points only if not already awarded
                    birthday_bonus_rewards(customer.customer_id)
                    
                    # Check if the customer has an unread birthday notification
                    from application.models import Notification
                    unread_birthday_note = Notification.query.filter_by(
                        user_id=customer.customer_id,
                        subject="Happy Birthday! Your Bonus is Here",
                        is_read=False
                    ).first()
                    
                    # If no unread notification exists, add to list to send a new one/reminder
                    if not unread_birthday_note:
                        birthday_ids.append(customer.customer_id)
        
        # Call the updated batch-compatible notification method
        if birthday_ids:
            send_birthday_bonus_notification(birthday_ids)
        
        print(f"Scheduled Task Run: Processed {len(birthday_ids)} birthdays in window for {today}.")

