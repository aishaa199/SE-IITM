import anthropic
import json
from collections import Counter

from flask import Blueprint, request, jsonify, current_app, send_file
from flask_restful import Api, Resource
from flask_security import auth_required, roles_accepted, current_user, verify_password, hash_password
from sqlalchemy import func
from datetime import datetime, date, timedelta
from werkzeug.security import check_password_hash
from .models import Service, Staff, Customer, User, Product, Appointment, Invoice, CustomerReview, db, Role, Manager, ManagerTask, StaffAttendance, ReportRecord, InventoryTransaction, Finance
from .sec import datastore

main = Blueprint('main', __name__)
api = Api(main) 

################################# Login ##############################################
################################# Owner Login ########################################
@main.route('/owner-login', methods=['POST'])
def owner_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify({"message":"username not provided"}), 400
    
    if not password:
        return jsonify({"message":"password not provided"}), 400
    
    user = datastore.find_user(username=username)
    if not user:
        return jsonify({"message": "User with this username does not exist"}), 404
    
    # Check if the user has the 'Owner' role
    role_names = [role.name for role in user.roles]
    if 'owner' not in role_names:
        return jsonify({"message": "Access denied: User is not an Owner"}), 403
    
    if verify_password(password, user.password):
        return jsonify({"token": user.get_auth_token(), "username": user.username, "role": user.roles[0].name})
    else:
        return jsonify({"message":"Wrong Password"}), 400
    
#######################################################################################
################################## Manager Login ######################################
@main.route('/manager-login', methods=['POST'])
def manager_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify({"message":"username not provided"}), 400
    
    if not password:
        return jsonify({"message":"password not provided"}), 400
    
    user = datastore.find_user(username=username)
    if not user:
        return jsonify({"message": "User with this username does not exist"}), 404
    
    # Check if the user has the 'Manager' role
    role_names = [role.name for role in user.roles]
    if 'manager' not in role_names:
        return jsonify({"message": "Access denied: User is not a Manager"}), 403
    
    if verify_password(password, user.password):
        return jsonify({"token": user.get_auth_token(), "username": user.username, "role": user.roles[0].name})
    else:
        return jsonify({"message":"Wrong Password"}), 400
#######################################################################################
################################## Staff Login ######################################
@main.route('/staff-login', methods=['POST'])
def staff_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify({"message":"username not provided"}), 400
    
    if not password:
        return jsonify({"message":"password not provided"}), 400
    
    user = datastore.find_user(username=username)
    if not user:
        return jsonify({"message": "User with this username does not exist"}), 404
    
    # Check if the user has the 'Staff' role
    role_names = [role.name for role in user.roles]
    if 'staff' not in role_names:
        return jsonify({"message": "Access denied: User is not a Staff member"}), 403
    
    if verify_password(password, user.password):
        return jsonify({"token": user.get_auth_token(), "username": user.username, "role": user.roles[0].name})
    else:
        return jsonify({"message":"Wrong Password"}), 400
#######################################################################################
################################## Customer Login ######################################
@main.route('/customer-login', methods=['POST'])
def customer_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify({"message":"username not provided"}), 400
    
    if not password:
        return jsonify({"message":"password not provided"}), 400
    
    user = datastore.find_user(username=username)
    if not user:
        return jsonify({"message": "User with this username does not exist"}), 404
    
    # Check if the user has the 'Customer' role
    role_names = [role.name for role in user.roles]
    if 'customer' not in role_names:
        return jsonify({"message": "Access denied: User is not a Customer"}), 403
    
    if verify_password(password, user.password):
        return jsonify({"token": user.get_auth_token(), "username": user.username, "role": user.roles[0].name})
    else:
        return jsonify({"message":"Wrong Password"}), 400

#######################################################################################
################################## Customer Registration API ##############################
@main.route('/register-customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    dob_str = data.get('dob')
    phone = data.get('phone')
    address = data.get('address')
    # preferences is expected to be a list of strings from checkboxes
    preferences_list = data.get('preferences', []) 

    if not all([email, password, name, dob_str, phone]):
        return jsonify({"message": "Missing required fields: email, password, name, dob, phone"}), 400

    existing_user = User.query.filter_by(username=email).first()
    if existing_user:
        return jsonify({"message": "User with this email already exists"}), 400

    # Validate dob format
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Invalid date format for dob. Use YYYY-MM-DD"}), 400

    # Ensure 'customer' role exists
    customer_role = Role.query.filter_by(name='customer').first()
    if not customer_role:
        customer_role = Role(name='customer')
        db.session.add(customer_role)
        db.session.commit()

    try:
        # Create User
        new_user = User(username=email, password=hash_password(password), active=True)
        new_user.roles.append(customer_role)
        db.session.add(new_user)
        db.session.flush() # Get user ID before commit

        # Format preferences as a comma-separated string
        if isinstance(preferences_list, list):
            preferences_str = ",".join(preferences_list)
        else:
            preferences_str = str(preferences_list)

        # Create Customer Profile
        new_customer = Customer(
            customer_id=new_user.id,
            customer_name=name,
            customer_contact=phone,
            customer_dob=dob,
            customer_reg_date=date.today(),
            customer_email=email,
            customer_address=address,
            customer_type="Regular",
            customer_preferences=preferences_str,
            customer_available_rewards=0
        )
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"message": "Registration successful", "customer_id": new_customer.customer_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500

#######################################################################################
#######################################################################################

def get_dashboard_data():
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    # Today's appointments
    today_appointments = Appointment.query.filter(
        Appointment.appointment_datetime >= today_start,
        Appointment.appointment_datetime <= today_end
    ).all()

    appointment_count = len(today_appointments)

    # Peak hours — find the hour block with the most bookings today
    hour_counts = Counter(
        appt.appointment_datetime.hour for appt in today_appointments
    )
    if hour_counts:
        peak_hour = max(hour_counts, key=hour_counts.get)
        def fmt_hour(h):
            if h == 0:   return "12 AM"
            elif h < 12: return f"{h} AM"
            elif h == 12: return "12 PM"
            else:        return f"{h - 12} PM"
        peak_hours = f"{fmt_hour(peak_hour)} – {fmt_hour(peak_hour + 1)}"
    else:
        peak_hours = "N/A"

    # Most booked service today
    service_counts = Counter()
    for appt in today_appointments:
        for svc in appt.services:
            service_counts[svc.service_desc] += 1
    top_service = service_counts.most_common(1)[0][0] if service_counts else "N/A"

    # Top stylist today (most appointments assigned)
    staff_counts = Counter(
        appt.staff.staff_name
        for appt in today_appointments
        if appt.staff is not None
    )
    top_stylist = staff_counts.most_common(1)[0][0] if staff_counts else "N/A"

    # Low stock inventory items
    low_stock_products = Product.query.filter_by(product_low_stock_alert=True).all()
    inventory_alerts = [p.product_desc for p in low_stock_products]

    # Pending tasks: completed appointments awaiting feedback
    feedback_pending = Appointment.query.filter(
        Appointment.status == 1,
        Appointment.feedback_given == False
    ).count()
    pending_tasks = []
    if feedback_pending > 0:
        pending_tasks.append(f"Review {feedback_pending} pending customer feedback(s)")

    # Feedback alerts: low-rated reviews (≤ 3 stars)
    feedback_alerts = CustomerReview.query.filter(CustomerReview.rating <= 3).count()

    return {
        'appointments_today': appointment_count,
        'peak_hours': peak_hours,
        'top_service': top_service,
        'top_stylist': top_stylist,
        'inventory_alerts': inventory_alerts,
        'pending_tasks': pending_tasks,
        'feedback_alerts': feedback_alerts,
    }


def call_claude_api(data, manager_name, time_of_day):
    api_key = current_app.config.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured")

    client = anthropic.Anthropic(api_key=api_key)

    inventory_text = ", ".join(data['inventory_alerts']) if data['inventory_alerts'] else "None"
    tasks_text = ", ".join(data['pending_tasks']) if data['pending_tasks'] else "None"

    prompt = f"""You are an AI assistant for a salon management system. Generate a concise daily briefing for the salon manager.

Current time context: It is {time_of_day} in India (IST).

Today's operational data:
- Manager Name: {manager_name}
- Appointments Today: {data['appointments_today']}
- Peak Hours: {data['peak_hours']}
- Most Booked Service: {data['top_service']}
- Top Stylist (most bookings): {data['top_stylist']}
- Low Stock Inventory Items: {inventory_text}
- Pending Tasks: {tasks_text}
- Low-Rated Customer Feedback (≤3 stars): {data['feedback_alerts']}

Return ONLY a valid JSON object with exactly these keys:
- "greeting": Greet by first name using the correct time ("Good {time_of_day}, <name>! 👋") — match the IST time context exactly
- "summary": One sentence summarising today's key highlight, using actual numbers from the data
- "insights": Array of 3-5 concise insights, each mentioning specific values/names from the data (each under 15 words)
- "recommendations": Array of 3-4 specific, actionable recommendations tied to the data above (each under 15 words)

Rules: be data-driven, use real numbers, no generic filler. No markdown, no extra text — pure JSON only."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()
    # Strip markdown code fences if model adds them
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    return json.loads(response_text.strip())


@main.route('/ai/daily-briefing', methods=['GET'])
@auth_required()
@roles_accepted('owner', 'manager')
def daily_briefing():
    import pytz
    ist = pytz.timezone('Asia/Kolkata')
    ist_now = datetime.now(ist)
    hour = ist_now.hour
    if 5 <= hour < 12:
        time_of_day = "morning"
    elif 12 <= hour < 17:
        time_of_day = "afternoon"
    elif 17 <= hour < 21:
        time_of_day = "evening"
    else:
        time_of_day = "night"

    # Resolve the caller's display name
    manager_name = "Manager"
    if current_user.manager_profile:
        manager_name = current_user.manager_profile.manager_name.split()[0]
    elif current_user.owner_profile:
        manager_name = current_user.owner_profile.owner_name.split()[0]

    data = get_dashboard_data()

    try:
        response = call_claude_api(data, manager_name, time_of_day)
        return jsonify(response)
    except Exception as e:
        # Graceful fallback so the dashboard never breaks
        inv_count = len(data['inventory_alerts'])
        inv_note = (
            f"{inv_count} item(s) low on stock: {', '.join(data['inventory_alerts'][:2])}"
            if inv_count else "Inventory levels are adequate"
        )
        fallback = {
            "greeting": f"Good {time_of_day}, {manager_name}! 👋",
            "summary": (
                f"You have {data['appointments_today']} appointments today"
                + (f", with peak demand at {data['peak_hours']}." if data['peak_hours'] != 'N/A' else ".")
            ),
            "insights": [
                f"{data['appointments_today']} appointments scheduled today",
                f"Peak demand expected: {data['peak_hours']}",
                f"Most booked service: {data['top_service']}",
                f"Top stylist today: {data['top_stylist']}",
                inv_note,
            ],
            "recommendations": [
                f"Ensure adequate staffing during {data['peak_hours']}",
                "Replenish low-stock inventory items" if inv_count else "Inventory is healthy — no restocking needed",
                f"Follow up on {data['feedback_alerts']} low-rated review(s)" if data['feedback_alerts'] else "No critical feedback to address today",
            ],
            "ai_error": str(e),
        }
        return jsonify(fallback)


##############################################################################
# AI Manager Task Checklist
##############################################################################

def get_task_dashboard_data():
    """Gather salon operational data for AI task generation."""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    tomorrow = today + timedelta(days=1)
    tomorrow_start = datetime.combine(tomorrow, datetime.min.time())
    tomorrow_end = datetime.combine(tomorrow, datetime.max.time())

    # Today's appointments
    today_appts = Appointment.query.filter(
        Appointment.appointment_datetime >= today_start,
        Appointment.appointment_datetime <= today_end
    ).all()
    appointment_count = len(today_appts)

    # Peak hour
    hour_counts = Counter(a.appointment_datetime.hour for a in today_appts)
    if hour_counts:
        peak_hour = max(hour_counts, key=hour_counts.get)
        def fmt_hour(h):
            if h == 0:    return "12 AM"
            elif h < 12:  return f"{h} AM"
            elif h == 12: return "12 PM"
            else:         return f"{h - 12} PM"
        peak_hours = f"{fmt_hour(peak_hour)} – {fmt_hour(peak_hour + 1)}"
    else:
        peak_hours = "N/A"

    # Low-stock items
    low_stock = Product.query.filter_by(product_low_stock_alert=True).all()
    inventory_alerts = [p.product_desc for p in low_stock]

    # Pending feedback (completed appointments, no review yet)
    pending_feedback = Appointment.query.filter(
        Appointment.status == 1,
        Appointment.feedback_given == False
    ).count()

    # Tomorrow's unconfirmed (status=0 Booked) appointments
    tomorrow_unconfirmed = Appointment.query.filter(
        Appointment.appointment_datetime >= tomorrow_start,
        Appointment.appointment_datetime <= tomorrow_end,
        Appointment.status == 0
    ).count()

    # Staff absent today
    present_ids = {row[0] for row in db.session.query(StaffAttendance.staff_id).filter(
        StaffAttendance.register_datetime >= today_start,
        StaffAttendance.register_datetime <= today_end
    ).distinct().all()}
    total_staff = Staff.query.count()
    absent_count = max(0, total_staff - len(present_ids))

    return {
        'appointments_today': appointment_count,
        'peak_hours': peak_hours,
        'inventory_alerts': inventory_alerts,
        'pending_feedback': pending_feedback,
        'tomorrow_unconfirmed': tomorrow_unconfirmed,
        'staff_absent_count': absent_count,
    }


def call_claude_for_tasks(data, manager_name):
    """Call Claude API and return a list of task dicts."""
    api_key = current_app.config.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured")

    client = anthropic.Anthropic(api_key=api_key)
    inventory_text = ", ".join(data['inventory_alerts']) if data['inventory_alerts'] else "None"

    prompt = f"""You are an AI assistant helping a salon manager organize daily tasks.

Manager Name: {manager_name}

Salon Data:
- Appointments Today: {data['appointments_today']}
- Peak Hours: {data['peak_hours']}
- Low-Stock Inventory Items: {inventory_text}
- Pending Customer Feedback: {data['pending_feedback']}
- Unconfirmed Appointments Tomorrow: {data['tomorrow_unconfirmed']}
- Staff Absent Today: {data['staff_absent_count']}

Generate a checklist of the most important tasks the manager should complete today.

Rules:
- Maximum 6 tasks
- Each task must be short and actionable (under 12 words)
- Focus only on items where the data indicates an actual issue
- Tasks must relate to salon operations

Return ONLY valid JSON, no markdown, no extra text:
{{
  "tasks": [
    {{"task": "Prepare staff for peak hours", "section": "appointments"}},
    {{"task": "Restock Hair Serum inventory", "section": "inventory"}}
  ]
}}

Valid section values: appointments, inventory, feedback, staff, general"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
    parsed = json.loads(response_text.strip())
    return parsed.get('tasks', [])


@main.route('/ai/generate-manager-tasks', methods=['POST'])
@auth_required()
@roles_accepted('manager')
def generate_manager_tasks():
    manager = current_user.manager_profile
    if not manager:
        return jsonify({"message": "Manager profile not found"}), 404

    manager_name = manager.manager_name.split()[0]
    manager_id = manager.manager_id

    data = get_task_dashboard_data()

    try:
        tasks = call_claude_for_tasks(data, manager_name)
    except Exception as e:
        return jsonify({"message": f"AI generation failed: {str(e)}"}), 500

    # Replace today's tasks for this manager
    today_start = datetime.combine(date.today(), datetime.min.time())
    ManagerTask.query.filter(
        ManagerTask.manager_id == manager_id,
        ManagerTask.created_at >= today_start
    ).delete(synchronize_session=False)

    new_tasks = []
    for t in tasks:
        task = ManagerTask(
            manager_id=manager_id,
            task_description=t.get('task', ''),
            task_section=t.get('section', 'general'),
            status='pending'
        )
        db.session.add(task)
        new_tasks.append(task)

    db.session.commit()

    return jsonify({
        "tasks": [
            {
                "task_id": task.task_id,
                "task_description": task.task_description,
                "task_section": task.task_section,
                "status": task.status,
                "created_at": task.created_at.isoformat()
            }
            for task in new_tasks
        ]
    })


@main.route('/ai/manager-tasks', methods=['GET'])
@auth_required()
@roles_accepted('manager')
def get_manager_tasks():
    manager = current_user.manager_profile
    if not manager:
        return jsonify({"tasks": []})

    today_start = datetime.combine(date.today(), datetime.min.time())
    tasks = ManagerTask.query.filter(
        ManagerTask.manager_id == manager.manager_id,
        ManagerTask.created_at >= today_start
    ).order_by(ManagerTask.task_id).all()

    return jsonify({
        "tasks": [
            {
                "task_id": t.task_id,
                "task_description": t.task_description,
                "task_section": t.task_section,
                "status": t.status,
                "created_at": t.created_at.isoformat()
            }
            for t in tasks
        ]
    })


@main.route('/tasks/<int:task_id>', methods=['PATCH'])
@auth_required()
@roles_accepted('manager')
def update_task_status(task_id):
    task = ManagerTask.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    # Verify ownership
    manager = current_user.manager_profile
    if not manager or task.manager_id != manager.manager_id:
        return jsonify({"message": "Forbidden"}), 403

    data = request.get_json()
    new_status = data.get('status')
    if new_status not in ('pending', 'completed'):
        return jsonify({"message": "Invalid status. Use 'pending' or 'completed'"}), 400

    task.status = new_status
    db.session.commit()

    return jsonify({
        "task_id": task.task_id,
        "status": task.status
    })



##############################################################################
# AI Report Generation
##############################################################################

VALID_REPORT_TYPES  = {'sales', 'appointments', 'staff', 'inventory', 'financial', 'feedback'}
VALID_TIME_PERIODS  = {'daily', 'yesterday', 'weekly', 'monthly', 'custom'}


def _call_claude_report_intent(message):
    """Ask Claude to classify the report type and time period from a free-text request."""
    api_key = current_app.config.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not configured")

    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""You are an assistant helping a salon manager generate operational reports.

Manager request: "{message}"

Identify the report type and time period.

Supported report types: sales, appointments, staff, inventory, financial, feedback
Supported time periods: daily, yesterday, weekly, monthly, custom

If time_period is custom, extract start_date and end_date from the message (format YYYY-MM-DD).
If you cannot determine the report type, set report_type to null.

Return ONLY valid JSON, no markdown:
{{
  "report_type": "staff",
  "time_period": "weekly",
  "custom_start": null,
  "custom_end": null
}}"""

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    text = msg.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


@main.route('/ai/report-intent', methods=['POST'])
@auth_required()
@roles_accepted('manager', 'owner')
def report_intent():
    data = request.get_json()
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({"message": "No message provided"}), 400

    try:
        result = _call_claude_report_intent(message)
    except Exception as e:
        return jsonify({"message": f"AI classification failed: {str(e)}"}), 500

    report_type  = result.get('report_type')
    time_period  = result.get('time_period', 'monthly')
    custom_start = result.get('custom_start')
    custom_end   = result.get('custom_end')

    if report_type not in VALID_REPORT_TYPES:
        return jsonify({
            "report_type": None,
            "message": (
                "Please specify the type of report you need: "
                "sales, staff, appointments, inventory, financial, or feedback."
            )
        }), 422

    if time_period not in VALID_TIME_PERIODS:
        time_period = 'monthly'

    return jsonify({
        "report_type":  report_type,
        "time_period":  time_period,
        "custom_start": custom_start,
        "custom_end":   custom_end,
    })


# ─────────────────────────────────────────────────────────────────────────────
# Customer AI endpoints
# ─────────────────────────────────────────────────────────────────────────────

def _parse_json_response(raw_text):
    """Safely extract first JSON object from Claude response text."""
    import re
    raw_text = raw_text.strip()
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        m = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except json.JSONDecodeError:
                pass
    return {}


@main.route('/ai/generate-feedback', methods=['POST'])
@auth_required()
@roles_accepted('customer')
def generate_customer_feedback():
    """Generate structured salon feedback from keyword selections + optional note."""
    data        = request.get_json(silent=True) or {}
    keywords    = data.get('keywords', [])
    note        = (data.get('customer_note') or '').strip()
    service_name = (data.get('service_name') or 'salon service').strip()
    staff_name   = (data.get('staff_name') or 'the staff').strip()

    if not keywords and not note:
        return jsonify({"message": "Provide at least one keyword or a note"}), 400

    kw_str = ', '.join(keywords) if keywords else 'Overall Experience'
    prompt = f"""You are helping a customer write short feedback for a salon visit.

Service: {service_name}
Attended by: {staff_name}
Customer selected topics: {kw_str}
Customer's own note: {note if note else 'None'}

Write a polite, natural 2–3 sentence feedback message in first person.
Rules:
- Keep it under 80 words
- If the note mentions negatives, include them constructively
- Sound like a real customer, not a template
- Do not use placeholders like [service] or [staff]

Return ONLY valid JSON: {{"feedback_message": "..."}}"""

    try:
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=256,
            messages=[{'role': 'user', 'content': prompt}],
        )
        result = _parse_json_response(resp.content[0].text)
        if 'feedback_message' not in result:
            result = {'feedback_message': resp.content[0].text.strip()}
    except Exception as e:
        return jsonify({"message": f"AI generation failed: {str(e)}"}), 500

    return jsonify(result)


@main.route('/ai/customer-chat', methods=['POST'])
@auth_required()
@roles_accepted('customer')
def customer_chat():
    """
    AI-powered customer assistant.
    Handles: service recommendations, pricing queries, booking guidance,
    general Q&A, and reward point information.
    """
    data    = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()
    if not message:
        return jsonify({"message": "Empty message"}), 400

    # ── Fetch customer context ────────────────────────────────────────────────
    customer = Customer.query.filter_by(customer_id=current_user.id).first()
    reward_points = customer.customer_available_rewards if customer else 0
    reward_discount = (reward_points // 500) * 25   # ₹25 per 500 pts

    # ── All active services from DB ───────────────────────────────────────────
    services = Service.query.filter_by(active_flg=True).all()
    staff_list = Staff.query.all()

    services_catalog = '\n'.join([
        f"- {s.service_desc} | Category: {s.service_category} | ₹{int(s.service_price)} | {s.service_duration} min | Rating: {s.service_rating:.1f}★"
        for s in services
    ])

    staff_catalog = '\n'.join([
        f"- {s.staff_name} ({s.staff_role}) | Skills: {s.staff_skills} | Rating: {s.staff_cumulative_rating:.1f}★"
        for s in staff_list[:10]
    ])

    # ── Single-pass Claude call ───────────────────────────────────────────────
    prompt = f"""You are a warm, knowledgeable assistant for Glow Suite Beauty Salon.

Customer message: "{message}"

=== SALON SERVICES ===
{services_catalog}

=== AVAILABLE STAFF ===
{staff_catalog}

=== CUSTOMER ACCOUNT ===
Reward Points: {reward_points} pts (= ₹{reward_discount} discount available)

Instructions:
1. If the customer asks about a service, give its exact price and duration from the list above.
2. If the customer asks for a recommendation based on a concern (dry hair, tanning, etc.), suggest 2–3 relevant services with prices.
3. If the customer asks about booking, tell them to use the "Book Appointment" tab on the left sidebar.
4. If the customer asks about reward points or discounts, explain their balance.
5. If the customer asks about stylists/staff, mention relevant staff by name and their speciality.
6. Keep the response friendly, concise (under 120 words), and written in plain text (no markdown).
7. Always use ₹ for prices.

Return ONLY valid JSON: {{"response": "..."}}"""

    try:
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=350,
            messages=[{'role': 'user', 'content': prompt}],
        )
        result = _parse_json_response(resp.content[0].text)
        if 'response' not in result:
            result = {'response': resp.content[0].text.strip()}
    except Exception as e:
        # Graceful fallback
        result = {
            'response': (
                "I'm having trouble connecting right now. "
                "You can browse services in the 'Browse Services' tab "
                "or book an appointment from 'Book Appointment'. "
                "Feel free to try again shortly!"
            )
        }

    return jsonify(result)


def _reports_dir():
    """Absolute path to the /reports/ folder next to main.py."""
    import os
    return os.path.join(current_app.root_path, '..', 'reports')


def _save_report_file(file_obj, filename):
    """Write BytesIO to disk, return the saved absolute path."""
    import os
    folder = _reports_dir()
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, 'wb') as f:
        f.write(file_obj.read())
    file_obj.seek(0)   # rewind for send_file
    return path


def _upsert_report_record(report_type, time_period, user_id, pdf_path=None, csv_path=None):
    """
    Find or create today's ReportRecord for this (type, period, user).
    Returns the record after commit.
    """
    today_start = datetime.combine(date.today(), datetime.min.time())
    rec = ReportRecord.query.filter(
        ReportRecord.report_type  == report_type,
        ReportRecord.time_period  == time_period,
        ReportRecord.generated_by == user_id,
        ReportRecord.created_at   >= today_start,
    ).first()

    if rec is None:
        rec = ReportRecord(
            report_type=report_type,
            time_period=time_period,
            generated_by=user_id,
        )
        db.session.add(rec)

    if pdf_path:
        rec.pdf_path = pdf_path
    if csv_path:
        rec.csv_path = csv_path

    db.session.commit()
    return rec


@main.route('/generate-report', methods=['POST'])
@auth_required()
@roles_accepted('manager', 'owner')
def generate_report_endpoint():
    from .report_generators import generate_report

    data         = request.get_json()
    report_type  = (data.get('report_type') or '').strip().lower()
    time_period  = (data.get('time_period') or 'monthly').strip().lower()
    file_format  = (data.get('format') or 'csv').strip().lower()
    custom_start = data.get('custom_start')
    custom_end   = data.get('custom_end')

    if report_type not in VALID_REPORT_TYPES:
        return jsonify({"message": f"Invalid report type: {report_type}"}), 400
    if file_format not in ('csv', 'pdf'):
        return jsonify({"message": "Format must be 'csv' or 'pdf'"}), 400

    try:
        file_obj, filename, mimetype = generate_report(
            report_type, time_period, file_format, custom_start, custom_end
        )
        saved_path = _save_report_file(file_obj, filename)
    except Exception as e:
        return jsonify({"message": f"Report generation failed: {str(e)}"}), 500

    try:
        kwargs = {'pdf_path': saved_path} if file_format == 'pdf' else {'csv_path': saved_path}
        _upsert_report_record(report_type, time_period, current_user.id, **kwargs)
    except Exception:
        pass   # non-fatal — file still downloads even if DB write fails

    return send_file(
        file_obj,
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename,
    )


@main.route('/reports', methods=['GET'])
@auth_required()
@roles_accepted('manager', 'owner')
def list_reports():
    role_names = [r.name for r in current_user.roles]
    if 'owner' in role_names:
        records = ReportRecord.query.filter_by(shared_with_owner=True).order_by(ReportRecord.created_at.desc()).all()
    else:
        records = ReportRecord.query.filter_by(generated_by=current_user.id).order_by(ReportRecord.created_at.desc()).all()

    return jsonify([{
        'id':          r.id,
        'report_type': r.report_type,
        'time_period': r.time_period,
        'created_at':  r.created_at.isoformat(),
        'has_pdf':     bool(r.pdf_path),
        'has_csv':     bool(r.csv_path),
        'shared':      r.shared_with_owner,
    } for r in records])


@main.route('/reports/<int:report_id>/download', methods=['GET'])
@auth_required()
@roles_accepted('manager', 'owner')
def download_saved_report(report_id):
    import os
    fmt = request.args.get('format', 'csv').lower()
    rec = ReportRecord.query.get(report_id)
    if not rec:
        return jsonify({"message": "Report not found"}), 404

    role_names = [r.name for r in current_user.roles]
    if 'owner' not in role_names and rec.generated_by != current_user.id:
        return jsonify({"message": "Forbidden"}), 403

    path = rec.pdf_path if fmt == 'pdf' else rec.csv_path
    if not path or not os.path.isfile(path):
        return jsonify({"message": "File not found on disk"}), 404

    mimetype = 'application/pdf' if fmt == 'pdf' else 'text/csv'
    return send_file(path, mimetype=mimetype, as_attachment=True,
                     download_name=os.path.basename(path))


@main.route('/reports/<int:report_id>/share', methods=['POST'])
@auth_required()
@roles_accepted('manager')
def share_report_with_owner(report_id):
    rec = ReportRecord.query.get(report_id)
    if not rec:
        return jsonify({"message": "Report not found"}), 404
    if rec.generated_by != current_user.id:
        return jsonify({"message": "Forbidden"}), 403

    rec.shared_with_owner = True
    db.session.commit()
    return jsonify({"message": "Report shared with owner", "id": rec.id})


@main.route('/reports/generate-and-share', methods=['POST'])
@auth_required()
@roles_accepted('manager')
def generate_and_share_report():
    """Silently generate both PDF + CSV, save to disk, upsert DB record, share with owner."""
    from .report_generators import generate_report
    data        = request.get_json(silent=True) or {}
    report_type = data.get('report_type', 'appointments').lower()
    time_period = data.get('time_period', 'monthly').lower()
    custom_start = data.get('custom_start')
    custom_end   = data.get('custom_end')

    try:
        csv_obj, csv_filename, _ = generate_report(report_type, time_period, 'csv', custom_start, custom_end)
        pdf_obj, pdf_filename, _ = generate_report(report_type, time_period, 'pdf', custom_start, custom_end)
    except Exception as e:
        return jsonify({"message": f"Report generation failed: {e}"}), 500

    csv_path = _save_report_file(csv_obj, csv_filename)
    pdf_path = _save_report_file(pdf_obj, pdf_filename)

    rec = _upsert_report_record(report_type, time_period, current_user.id, csv_path=csv_path, pdf_path=pdf_path)
    rec.shared_with_owner = True
    db.session.commit()

    return jsonify({"message": "Report generated and shared with owner", "id": rec.id})


@main.route('/reports/analytics', methods=['GET'])
@auth_required()
@roles_accepted('manager', 'owner')
def report_analytics():
    """Return chart-ready JSON for a given report type and time period."""
    from collections import Counter as _Counter
    report_type = request.args.get('type', 'appointments').lower()
    time_period = request.args.get('period', 'monthly').lower()
    custom_start = request.args.get('custom_start')
    custom_end   = request.args.get('custom_end')

    from .report_generators import get_date_range
    start, end, label = get_date_range(time_period, custom_start, custom_end)

    STATUS_MAP = {0: 'Booked', 1: 'Completed', 2: 'No-show', 3: 'Cancelled', 4: 'Rescheduled', 5: 'Invoiced'}

    if report_type == 'appointments':
        appts = Appointment.query.filter(
            Appointment.appointment_datetime >= start,
            Appointment.appointment_datetime <= end,
        ).all()

        by_status = _Counter(STATUS_MAP.get(a.status, 'Unknown') for a in appts)
        by_day = _Counter(a.appointment_datetime.strftime('%Y-%m-%d') for a in appts)
        service_counts = _Counter()
        for a in appts:
            for s in a.services:
                service_counts[s.service_desc] += 1

        return jsonify({
            'label':        label,
            'total':        len(appts),
            'by_status':    [{'name': k, 'value': v} for k, v in sorted(by_status.items())],
            'by_day':       [{'date': d, 'count': c} for d, c in sorted(by_day.items())],
            'top_services': [{'name': k, 'count': v} for k, v in service_counts.most_common(8)],
        })

    elif report_type == 'sales':
        invoices = Invoice.query.filter(
            Invoice.invoice_date >= start.date(),
            Invoice.invoice_date <= end.date(),
        ).all()

        by_day = {}
        svc_revenue = _Counter()
        for inv in invoices:
            d = inv.invoice_date.strftime('%Y-%m-%d')
            by_day[d] = by_day.get(d, 0) + float(inv.payable_invoice_amount)
            svc_ids = [s.strip() for s in (inv.service_ids or '').split(',') if s.strip().isdigit()]
            svc_objs = Service.query.filter(Service.service_id.in_(svc_ids)).all() if svc_ids else []
            for svc in svc_objs:
                svc_revenue[svc.service_desc] += float(inv.payable_invoice_amount) / max(len(svc_objs), 1)

        total = sum(float(i.payable_invoice_amount) for i in invoices)

        return jsonify({
            'label':         label,
            'total_revenue': round(total, 2),
            'invoice_count': len(invoices),
            'by_day':        [{'date': d, 'revenue': round(v, 2)} for d, v in sorted(by_day.items())],
            'by_service':    [{'name': k, 'revenue': round(v, 2)} for k, v in svc_revenue.most_common(8)],
        })

    elif report_type == 'staff':
        all_staff = Staff.query.all()
        staff_data = []
        for s in all_staff:
            total = Appointment.query.filter(
                Appointment.staff_id == s.staff_id,
                Appointment.appointment_datetime >= start,
                Appointment.appointment_datetime <= end,
            ).count()
            completed = Appointment.query.filter(
                Appointment.staff_id == s.staff_id,
                Appointment.appointment_datetime >= start,
                Appointment.appointment_datetime <= end,
                Appointment.status == 1,
            ).count()
            att_days = db.session.query(
                func.count(func.distinct(func.date(StaffAttendance.register_datetime)))
            ).filter(
                StaffAttendance.staff_id == s.staff_id,
                StaffAttendance.register_datetime >= start,
                StaffAttendance.register_datetime <= end,
            ).scalar() or 0

            staff_data.append({
                'name':            s.staff_name,
                'total':           total,
                'completed':       completed,
                'attendance_days': att_days,
                'rating':          round(s.staff_cumulative_rating, 1) if s.staff_cumulative_rating else 0,
            })

        return jsonify({'label': label, 'staff': staff_data})

    elif report_type == 'inventory':
        products = Product.query.all()
        items = []
        for p in products:
            used = db.session.query(func.sum(InventoryTransaction.quantity)).filter(
                InventoryTransaction.product_id == p.product_id,
                InventoryTransaction.txn_type == 0,
                InventoryTransaction.date_of_txn >= start,
                InventoryTransaction.date_of_txn <= end,
            ).scalar() or 0
            items.append({
                'name':      p.product_desc,
                'current':   p.product_curr_qoh,
                'minimum':   p.product_min_qoh,
                'low_stock': p.product_low_stock_alert,
                'used':      used,
            })
        low_count = sum(1 for i in items if i['low_stock'])
        return jsonify({'label': label, 'items': items, 'low_stock_count': low_count})

    elif report_type == 'feedback':
        reviews = (
            db.session.query(CustomerReview)
            .join(Appointment, CustomerReview.apppointment_id == Appointment.appointment_id)
            .filter(
                Appointment.appointment_datetime >= start,
                Appointment.appointment_datetime <= end,
            ).all()
        )
        by_rating = _Counter(r.rating for r in reviews)
        avg = round(sum(r.rating for r in reviews) / len(reviews), 2) if reviews else 0
        positive = sum(1 for r in reviews if r.rating >= 4)
        neutral  = sum(1 for r in reviews if r.rating == 3)
        negative = sum(1 for r in reviews if r.rating <= 2)

        return jsonify({
            'label':    label,
            'total':    len(reviews),
            'average':  avg,
            'by_rating': [{'rating': k, 'count': v} for k, v in sorted(by_rating.items())],
            'sentiment': [
                {'name': 'Positive', 'value': positive},
                {'name': 'Neutral',  'value': neutral},
                {'name': 'Negative', 'value': negative},
            ],
        })

    elif report_type == 'financial':
        records = Finance.query.filter(
            Finance.reporting_month >= start,
            Finance.reporting_month <= end,
        ).order_by(Finance.reporting_month).all()
        return jsonify({
            'label': label,
            'months': [{
                'month':   r.reporting_month.strftime('%b %Y'),
                'revenue': float(r.total_revenue),
                'cost':    float(r.product_cost),
                'salary':  float(r.staff_salary),
                'profit':  float(r.net_profit) if r.net_profit else 0,
            } for r in records],
        })

    return jsonify({"message": f"Unknown report type: {report_type}"}), 400
