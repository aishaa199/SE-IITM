import anthropic
import json
from collections import Counter

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
from flask_security import auth_required, roles_accepted, current_user, verify_password, hash_password
from datetime import datetime, date
from werkzeug.security import check_password_hash
from .models import Service, Staff, Customer, User, Product, Appointment, Invoice, CustomerReview, db, Role
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

