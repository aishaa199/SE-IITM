from flask_restful import Resource, Api, reqparse, marshal_with, fields, marshal
from flask_security import auth_required, roles_required, current_user, hash_password, verify_password
from datetime import datetime, timedelta, date
from flask import request, jsonify
from .sec import datastore
from .models import Service, Staff, Customer, User, Product, Appointment, Invoice, InventoryTransaction, StaffAttendance, CustomerReview, Finance, Manager, Owner, CustomerReward, SalonConfig, db, Role, UserRoles
api = Api(prefix = '/api')


################################## Owner Dashboard #####################################
################################## Create Manager ######################################
class Owner(Resource):
    @auth_required("token")
    @roles_required("owner")
    def post(self):
        data = request.get_json()
        manager_name = data.get('fullname')
        manager_email = data.get('email')
        manager_contact = data.get('phone')
        manager_skills = data.get('skills')
        manager_role1 = data.get('role')
        manager_dob_str = data.get('dob')
        manager_doj_str = data.get('doj')
        username = data.get('username')
        password = data.get('password')
        
        # Parse dates
        try:
            manager_dob = datetime.strptime(manager_dob_str, '%Y-%m-%d').date() if manager_dob_str else None
            manager_doj = datetime.strptime(manager_doj_str, '%Y-%m-%d').date() if manager_doj_str else date.today()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

        if not username:
            return {"message":"username not provided"}, 400
        
        if not password:
            return {"message":"password not provided"}, 400
        
        existing_user = datastore.find_user(username=username)
        if existing_user:
            return {"message": "User with this username already exists"}, 400
        
        manager_role = Role.query.filter_by(name='manager').first()
        if not manager_role:
            manager_role = Role(name='manager')
            db.session.add(manager_role)
            db.session.commit()
        
        new_user = User(username=username, password=hash_password(password))
        new_user.roles.append(manager_role)
        
        try:
            db.session.add(new_user)
            #db.session.flush() # Sync with DB to get new_user.id without committing yet
            db.session.commit() # Commit to get the ID generated for the new user
            # Now create the manager with the newly generated ID
            new_manager = Manager(
                manager_id=new_user.id, 
                manager_name=manager_name or "Unknown", 
                manager_email=manager_email,
                manager_contact=manager_contact or "0000000000",
                manager_skills=manager_skills or "Not Specified",
                manager_role=manager_role1 or "Manager",
                manager_dob=manager_dob or datetime.now().date(),
                manager_doj=manager_doj or datetime.now().date()
            )
            db.session.add(new_manager)
            db.session.commit() 
            
            return {"message": "Manager created successfully", "username": username}
            
        except Exception as e:
            db.session.rollback() # Undo everything if either step fails
            print(f"Error creating manager: {str(e)}")
            return {"message": "Failed to create manager. Profile creation failed."}, 500

#######################################################################################
class ChangePassword(Resource):
    @auth_required("token")
    def put(self):
        data = request.get_json()
        user_id = current_user.id
        current_password = data.get("current_password", "").strip()
        new_password = data.get("new_password", "").strip()
        confirm_password = data.get("confirm_password", "").strip()

        user = User.query.get(user_id)
        
        if verify_password(current_password, user.password):
            if (new_password)== "" or (confirm_password) == "":
                return {"message": "New password and confirm password cannot be empty"}, 400
            elif (new_password) == current_password:
                return {"message": "New password cannot be the same as the current password"}, 400
            elif new_password != confirm_password:
                return {"message": "New password and confirm password do not match"}, 400
            else:
                user.password = hash_password(new_password)
                db.session.commit()
                return {"message": "Password changed successfully"}
        else:
            return {"message": "Wrong current password"}, 400



# Add API resources to the app

api.add_resource(Owner, '/create-manager', '/create-customer', '/update-customer') #get, post, put
api.add_resource(ChangePassword, '/change-password')