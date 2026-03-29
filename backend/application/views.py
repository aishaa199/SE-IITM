from pyclbr import Class

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_security import auth_required, roles_required, current_user, verify_password, hash_password
from datetime import datetime, date
from werkzeug.security import check_password_hash
from .models import Service, Staff, Customer, User, Product, Appointment, Invoice, InventoryTransaction, StaffAttendance, CustomerReview, Finance, Manager, Owner, CustomerReward, SalonConfig, db, Role, UserRoles
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

