from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_security import auth_required, roles_required, current_user, verify_password
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

