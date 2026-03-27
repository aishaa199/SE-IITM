from flask_restful import Resource, Api, reqparse, marshal_with, fields, marshal
from flask_security import auth_required, roles_required, roles_accepted, current_user, hash_password, verify_password
from datetime import datetime, timedelta, date
from flask import request, jsonify
from .sec import datastore
from .models import Service, Staff, Customer, User, Product, Appointment, Invoice, InventoryTransaction, StaffAttendance, CustomerReview, Finance, Manager, Owner, CustomerReward, SalonConfig, db, Role, UserRoles, appointment_services
api = Api(prefix = '/api')

################################# HELPER FUNCTIONS ########################################
################################# To update low stock alerts based on quantity and minimum stock threshold. #########################
def update_low_stock_alerts(product_id=None):
    """Helper procedure to update product_low_stock_alert based on quantity.
    If product_id is provided, update only that product, else update all.
    """
    try:
        if product_id:
            product = Product.query.get(product_id)
            if product:
                product.product_low_stock_alert = product.product_curr_qoh < product.product_min_qoh
        else:
            products = Product.query.all()
            for product in products:
                product.product_low_stock_alert = product.product_curr_qoh < product.product_min_qoh
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating low stock alerts: {str(e)}")
        return False

################################# To cleanup old appointment data based on retention policy. #########################
def cleanup_appointment_history():
    """Helper procedure to delete appointments older than retention period defined in SalonConfig."""
    config = SalonConfig.query.filter_by(param_name='APPT_HISTORY_RETENTION_DAYS').first()
    
    if not config:
        return False, "Retention policy (APPT_HISTORY_RETENTION_DAYS) not found."
    
    try:
        retention_days = int(config.param_value)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Find old appointment IDs
        old_appt_ids = db.session.query(Appointment.appointment_id).filter(
            Appointment.appointment_datetime < cutoff_date
        ).all()

        if not old_appt_ids:
            return True, 0

        ids = [a.appointment_id for a in old_appt_ids]

        # Delete associations first
        db.session.execute(
            appointment_services.delete().where(appointment_services.c.appointment_id.in_(ids))
        )

        # Delete main records
        deleted_count = Appointment.query.filter(Appointment.appointment_id.in_(ids)).delete(synchronize_session=False)
        
        db.session.commit()
        return True, deleted_count
    except Exception as e:
        db.session.rollback()
        return False, str(e)

################################# To update service active flags based on to_date comparison. #########################
def update_service_curr_flag(service_id=None):
    """Helper procedure to update active_flg in service_master table.
    Updates based on to_date comparison with today's date.
    """
    try:
        today = date.today()
        if service_id:
            service = Service.query.get(service_id)
            if service:
                if service.to_date and service.to_date < today:
                    service.active_flg = False
                else:
                    service.active_flg = True
        else:
            services = Service.query.all()
            for service in services:
                if service.to_date and service.to_date < today:
                    service.active_flg = False
                else:
                    service.active_flg = True
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error updating service active flag: {str(e)}")
        return False

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
        branch_name = data.get('branch_name')
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
                manager_doj=manager_doj or datetime.now().date(),
                branch_name=branch_name
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

################################## Manager Dashboard ##################################
################################## Product API ########################################

product_fields = {
    'product_id': fields.Integer,
    'product_desc': fields.String,
    'product_category_name': fields.String,
    'product_price': fields.Float,
    'product_min_qoh': fields.Integer,
    'product_curr_qoh': fields.Integer,
    'product_supplier_name': fields.String,
    'product_supplier_contact': fields.String,
    'product_supplier_email': fields.String,
    'product_low_stock_alert': fields.Boolean
}

class ProductResource(Resource):

################################## Create Product #####################################
    @auth_required("token")
    @roles_required("manager")
    def post(self):
        data = request.get_json()
        try:
            new_product = Product(
                product_desc=data.get('product_name'),
                product_category_name=data.get('product_category'),
                product_price=data.get('price'),
                product_min_qoh=data.get('minimum_stock'),
                product_curr_qoh=data.get('stock_quantity'),
                product_supplier_name=data.get('supplier_name'),
                product_supplier_contact=data.get('supplier_contact'),
                product_supplier_email=data.get('supplier_email')
            )
            db.session.add(new_product)
            db.session.commit()
            # Update low stock alert for the newly added product
            update_low_stock_alerts(new_product.product_id)
            return {"message": "Product added successfully", "product_id": new_product.product_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to add product: {str(e)}"}, 500

################################## Edit Product #######################################
    @auth_required("token")
    @roles_required("manager")
    def put(self, product_id):
        data = request.get_json()
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}, 404
        
        try:
            product.product_desc = data.get('product_name', product.product_desc)
            product.product_category_name = data.get('product_category', product.product_category_name)
            product.product_price = data.get('price', product.product_price)
            product.product_min_qoh = data.get('minimum_stock', product.product_min_qoh)
            product.product_curr_qoh = data.get('stock_quantity', product.product_curr_qoh)
            product.product_supplier_name = data.get('supplier_name', product.product_supplier_name)
            product.product_supplier_contact = data.get('product_supplier_contact', product.product_supplier_contact)
            product.product_supplier_email = data.get('product_supplier_email', product.product_supplier_email)
            
            db.session.commit()
            # Update low stock alert for the modified product
            update_low_stock_alerts(product_id)
            return {"message": "Product updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update product: {str(e)}"}, 500

################################## Delete Product #####################################
    @auth_required("token")
    @roles_required("manager")
    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}, 404
        
        # Check if product is referenced in InventoryTransaction
        transaction_exists = InventoryTransaction.query.filter_by(product_id=product_id).first()
        if transaction_exists:
            return {"message": "Cannot delete product as it has associated inventory transactions"}, 400
        
        try:
            db.session.delete(product)
            db.session.commit()
            return {"message": "Product deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete product: {str(e)}"}, 500

################################## Get Products #####################################
    @auth_required("token")
    def get(self, product_id=None):
        # Update low stock alerts before fetching
        update_low_stock_alerts()

        if product_id:
            product = Product.query.get(product_id)
            if not product:
                return {"message": "Product not found"}, 404
            return marshal(product, product_fields)
        
        products = Product.query.all()
        return marshal(products, product_fields)

################################## Inventory Transaction Fields ###########################
def get_recorded_by_name(txn):
    """Helper to get name of person who recorded the transaction (Staff or Manager)"""
    if txn.txn_type == 0 and txn.staff:
        return txn.staff.staff_name
    elif txn.txn_type == 1 and txn.manager:
        return txn.manager.manager_name
    return "Unknown"

inventory_transaction_fields = {
    'txn_id': fields.Integer,
    'product_id': fields.Integer,
    'product_name': fields.String(attribute='product.product_desc'),
    'staff_id': fields.Integer,
    'recorded_by': fields.String(attribute=get_recorded_by_name),
    'service_id': fields.Integer,
    'service_name': fields.String(attribute='service.service_desc'),
    'txn_type': fields.Integer,
    'quantity': fields.Integer,
    'date_of_txn': fields.DateTime
}

################################## Inventory Transaction API ###########################
class InventoryTransactionResource(Resource):
################################## Get Inventory Transaction ###########################
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def get(self, txn_id=None):
        if txn_id:
            txn = InventoryTransaction.query.get(txn_id)
            if not txn:
                return {"message": "Transaction not found"}, 404
            return marshal(txn, inventory_transaction_fields)
        
        # Date filtering logic
        from_date_str = request.args.get('from_date')
        to_date_str = request.args.get('to_date')
        
        try:
            if from_date_str and to_date_str:
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
                # Make to_date inclusive of the entire day
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            else:
                # Default to this month
                today = date.today()
                from_date = datetime(today.year, today.month, 1)
                to_date = datetime.now()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD"}, 400

        query = InventoryTransaction.query.filter(
            InventoryTransaction.date_of_txn >= from_date,
            InventoryTransaction.date_of_txn <= to_date
        )
        
        # Managers see all, staff see theirs
        if not any(role.name == 'manager' for role in current_user.roles):
            query = query.filter_by(staff_id=current_user.id)
            
        transactions = query.order_by(InventoryTransaction.date_of_txn.desc()).all()
        return marshal(transactions, inventory_transaction_fields)

################################## Create Inventory Transaction ###########################
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def post(self):
        data = request.get_json()
        product_id = data.get('product_id')
        service_id = data.get('service_id')
        quantity = data.get('quantity')
        
        if not product_id or not quantity or quantity <= 0:
            return {"message": "Invalid product_id or quantity"}, 400
            
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}, 404
            
        # Optional: Validate service_id if provided
        if service_id:
            service = Service.query.get(service_id)
            if not service:
                return {"message": "Service not found"}, 404
            
        is_manager = any(role.name == 'manager' for role in current_user.roles)
        is_staff = any(role.name == 'staff' for role in current_user.roles)
        
        # Logic: 
        # Staff: txn_type = 0 (ordering/taking), reduces qoh
        # Manager: txn_type = 1 (replenishing), increases qoh
        
        if is_manager:
            txn_type = 1
            product.product_curr_qoh += quantity
        elif is_staff:
            txn_type = 0
            if product.product_curr_qoh < quantity:
                return {"message": "Insufficient stock"}, 400
            product.product_curr_qoh -= quantity
        else:
            return {"message": "Unauthorized"}, 403
            
        try:
            new_txn = InventoryTransaction(
                product_id=product_id,
                staff_id=current_user.id,
                service_id=service_id,
                txn_type=txn_type,
                quantity=quantity,
                date_of_txn=datetime.now()
            )
            db.session.add(new_txn)
            db.session.commit()
            
            # Check for low stock alerts after update
            update_low_stock_alerts(product_id)
            
            return {"message": "Transaction recorded successfully", "txn_id": new_txn.txn_id}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error recording transaction: {str(e)}"}, 500


################################## Customer Fields ########################################
customer_fields = {
    'customer_id': fields.Integer,
    'customer_name': fields.String,
    'customer_contact': fields.String,
    'customer_dob': fields.String,
    'customer_reg_date': fields.String,
    'customer_email': fields.String,
    'customer_address': fields.String,
    'number_of_visits': fields.Integer,
    'customer_type': fields.String,
    'customer_preferences': fields.String,
    'customer_available_rewards': fields.Integer
}

################################## Customer API ########################################
class CustomerResource(Resource):

################################## Fetch Customer #####################################
    @auth_required("token")
    def get(self, customer_id=None):
        if customer_id:
            customer = Customer.query.get(customer_id)
            if not customer:
                return {"message": "Customer not found"}, 404
            return marshal(customer, customer_fields)
        
        customers = Customer.query.all()
        return marshal(customers, customer_fields)

################################## Create Customer #####################################
    @auth_required("token")
    @roles_required("manager")
    def post(self):
        data = request.get_json()
        
        # Use email as username
        username = data.get('customer_email')
        # Set default password
        password = "pass1234"
        
        if not username:
            return {"message": "Customer email is required to create an account"}, 400
            
        existing_user = datastore.find_user(username=username)
        if existing_user:
            return {"message": "User with this email already exists"}, 400
            
        customer_role = Role.query.filter_by(name='customer').first()
        if not customer_role:
            customer_role = Role(name='customer')
            db.session.add(customer_role)
            db.session.commit()
            
        new_user = User(username=username, password=hash_password(password))
        new_user.roles.append(customer_role)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            dob_str = data.get('customer_dob')
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else datetime.now().date()
            
            new_customer = Customer(
                customer_id=new_user.id,
                customer_name=data.get('customer_name'),
                customer_contact=data.get('customer_contact'),
                customer_dob=dob,
                customer_reg_date=datetime.now().date(),
                customer_email=username, # Same as username
                customer_address=data.get('customer_address'),
                customer_type=data.get('customer_type', 'Regular'),
                customer_preferences=data.get('customer_preferences')
            )
            db.session.add(new_customer)
            db.session.commit()
            return {"message": "Customer created successfully", "customer_id": new_customer.customer_id, "username": username}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to create customer: {str(e)}"}, 500

################################## Edit Customer #####################################
    @auth_required("token")
    @roles_required("manager")
    def put(self, customer_id):
        data = request.get_json()
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"message": "Customer not found"}, 404
            
        try:
            customer.customer_name = data.get('customer_name', customer.customer_name)
            customer.customer_contact = data.get('customer_contact', customer.customer_contact)
            customer.customer_email = data.get('customer_email', customer.customer_email)
            customer.customer_address = data.get('customer_address', customer.customer_address)
            customer.customer_type = data.get('customer_type', customer.customer_type)
            customer.customer_preferences = data.get('customer_preferences', customer.customer_preferences)
            
            if 'customer_dob' in data:
                customer.customer_dob = datetime.strptime(data['customer_dob'], '%Y-%m-%d').date()
                
            db.session.commit()
            return {"message": "Customer updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update customer: {str(e)}"}, 500

################################## Delete Customer #####################################
    @auth_required("token")
    @roles_required("manager")
    def delete(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"message": "Customer not found"}, 404
            
        # Check for associations before deleting
        has_appointments = Appointment.query.filter_by(customer_id=customer_id).first()
        if has_appointments:
            return {"message": "Cannot delete customer with existing appointments"}, 400
        
        has_invoices = Invoice.query.filter_by(customer_id=customer_id).first()
        if has_invoices:
            return {"message": "Cannot delete customer with existing invoices"}, 400
            
        try:
            user = User.query.get(customer.customer_id)
            db.session.delete(customer)
            if user:
                db.session.delete(user)
            db.session.commit()
            return {"message": "Customer deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete customer: {str(e)}"}, 500

################################## Manager Serialization Fields #########################
manager_fields = {
    'manager_id': fields.Integer,
    'manager_name': fields.String,
    'manager_email': fields.String,
    'manager_contact': fields.String,
    'manager_skills': fields.String,
    'manager_role': fields.String,
    'manager_dob': fields.String,
    'manager_doj': fields.String,
    'branch_name': fields.String
}

################################## Manager API ############################################
class ManagerResource(Resource):
################################## Fetch Manager ############################################
    @auth_required("token")
    @roles_accepted("owner", "manager")
    def get(self, manager_id=None):
        if manager_id:
            manager = Manager.query.get(manager_id)
            if not manager:
                return {"message": "Manager not found"}, 404
            return marshal(manager, manager_fields)
        
        managers = Manager.query.all()
        return marshal(managers, manager_fields)

################################## Edit Manager ############################################
    @auth_required("token")
    @roles_accepted("owner", "manager")
    def put(self, manager_id):
        # Managers can only edit their own profile, Owners can edit any
        is_owner = any(role.name == 'owner' for role in current_user.roles)
        if not is_owner and current_user.id != manager_id:
            return {"message": "Unauthorized to edit this manager profile"}, 403

        data = request.get_json()
        manager = Manager.query.get(manager_id)
        if not manager:
            return {"message": "Manager not found"}, 404
            
        try:
            manager.manager_name = data.get('manager_name', manager.manager_name)
            manager.manager_email = data.get('manager_email', manager.manager_email)
            manager.manager_contact = data.get('manager_contact', manager.manager_contact)
            manager.manager_skills = data.get('manager_skills', manager.manager_skills)
            manager.manager_role = data.get('manager_role', manager.manager_role)
            manager.branch_name = data.get('branch_name', manager.branch_name)
            
            if 'manager_dob' in data:
                manager.manager_dob = datetime.strptime(data['manager_dob'], '%Y-%m-%d')
            if 'manager_doj' in data:
                manager.manager_doj = datetime.strptime(data['manager_doj'], '%Y-%m-%d')
            
            db.session.commit()
            return {"message": "Manager updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update manager: {str(e)}"}, 500

################################## Delete Manager ############################################
    @auth_required("token")
    @roles_required("owner")
    def delete(self, manager_id):
        manager = Manager.query.get(manager_id)
        if not manager:
            return {"message": "Manager not found"}, 404
            
        try:
            user = User.query.get(manager.manager_id)
            db.session.delete(manager)
            if user:
                db.session.delete(user)
            db.session.commit()
            return {"message": "Manager and associated user deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete manager: {str(e)}"}, 500

################################## Staff Serialization Fields #########################
staff_fields = {
    'staff_id': fields.Integer,
    'staff_name': fields.String,
    'staff_contact': fields.String,
    'staff_email': fields.String,
    'staff_skills': fields.String,
    'staff_role': fields.String,
    'staff_dob': fields.String,
    'staff_doj': fields.String,
    'staff_salary': fields.Float,
    'staff_cumulative_rating': fields.Float,
    'no_of_reviews': fields.Integer
}

################################## Staff API ############################################
class StaffResource(Resource):

################################## Fetch Staff ############################################
    @auth_required("token")
    def get(self, staff_id=None):
        if staff_id:
            staff = Staff.query.get(staff_id)
            if not staff:
                return {"message": "Staff member not found"}, 404
            return marshal(staff, staff_fields)
        
        staff_members = Staff.query.all()
        return marshal(staff_members, staff_fields)

################################## Create Staff ############################################
    @auth_required("token")
    @roles_required("manager")
    def post(self):
        data = request.get_json()
        
        
        username = data.get('username')
        password = "pass1234" # Default password for new members
        
        existing_user = datastore.find_user(username=username)
        if existing_user:
            return {"message": f"User with username '{username}' already exists"}, 400
            
        staff_role_obj = Role.query.filter_by(name='staff').first()
        if not staff_role_obj:
            staff_role_obj = Role(name='staff')
            db.session.add(staff_role_obj)
            db.session.commit()
            
        new_user = User(username=username, password=hash_password(password))
        new_user.roles.append(staff_role_obj)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            dob_str = data.get('staff_dob')
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else datetime.now().date()
            
            doj_str = data.get('staff_doj')
            doj = datetime.strptime(doj_str, '%Y-%m-%d').date() if doj_str else datetime.now().date()
            
            new_staff = Staff(
                staff_id=new_user.id,
                staff_name=data.get('staff_name'),
                staff_contact=data.get('staff_contact'),
                staff_email=data.get('staff_email'),
                staff_skills=data.get('staff_skills', 'Not Specified'),
                staff_role=data.get('staff_role', 'Staff'),
                staff_dob=dob,
                staff_doj=doj,
                staff_salary=data.get('staff_salary', 0.0)
            )
            db.session.add(new_staff)
            db.session.commit()
            return {"message": "Staff member created successfully", "staff_id": new_staff.staff_id, "username": username}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to create staff: {str(e)}"}, 500
        
################################## Edit Staff ############################################
    @auth_required("token")
    @roles_required("manager")
    def put(self, staff_id):
        data = request.get_json()
        staff = Staff.query.get(staff_id)
        if not staff:
            return {"message": "Staff member not found"}, 404
            
        try:
            staff.staff_name = data.get('staff_name', staff.staff_name)
            staff.staff_contact = data.get('staff_contact', staff.staff_contact)
            staff.staff_email = data.get('staff_email', staff.staff_email)
            staff.staff_skills = data.get('staff_skills', staff.staff_skills)
            staff.staff_role = data.get('staff_role', staff.staff_role)
            staff.staff_salary = data.get('staff_salary', staff.staff_salary)
            
            if 'staff_dob' in data:
                staff.staff_dob = datetime.strptime(data['staff_dob'], '%Y-%m-%d').date()
            if 'staff_doj' in data:
                staff.staff_doj = datetime.strptime(data['staff_doj'], '%Y-%m-%d').date()
                
            db.session.commit()
            return {"message": "Staff member updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update staff: {str(e)}"}, 500

################################## Delete Staff ############################################
    @auth_required("token")
    @roles_required("manager")
    def delete(self, staff_id):
        staff = Staff.query.get(staff_id)
        if not staff:
            return {"message": "Staff member not found"}, 404
            
        #Check if staff has assigned appointments or transactions
        has_appointments = Appointment.query.filter_by(staff_id=staff_id).first()
        if has_appointments:
            return {"message": "Cannot delete staff with existing appointments"}, 400

        has_invoices = Invoice.query.filter_by(staff_id=staff_id).first()
        if has_invoices:
            return {"message": "Cannot delete staff with existing invoices"}, 400
        
        has_transactions = InventoryTransaction.query.filter_by(staff_id=staff_id).first()
        if has_transactions:
            return {"message": "Cannot delete staff with existing inventory transactions"}, 400

        try:
            user = User.query.get(staff.staff_id)
            db.session.delete(staff)
            if user:
                db.session.delete(user)
            db.session.commit()
            return {"message": "Staff member deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete staff: {str(e)}"}, 500

################################## Service Serialization Fields #########################
service_fields = {
    'service_id': fields.Integer,
    'service_desc': fields.String,
    'service_category': fields.String,
    'from_date': fields.String,
    'to_date': fields.String,
    'active_flg': fields.Boolean,
    'service_price': fields.Float,
    'service_duration': fields.Integer,
    'service_products': fields.String,
    'service_rating': fields.Float,
    'no_of_reviews': fields.Integer
}

################################## Salon Config Serialization Fields ###################
salon_config_fields = {
    'setting_id': fields.Integer,
    'param_name': fields.String,
    'param_value': fields.String,
    'from_date': fields.String,
    'to_date': fields.String
}

################################## Service API ##########################################
class ServiceResource(Resource):
################################## Get Service ###########################################
    @auth_required("token")
    def get(self, service_id=None):
        # Update service active flags before fetching
        update_service_curr_flag()

        if service_id:
            service = Service.query.get(service_id)
            if not service:
                return {"message": "Service not found"}, 404
            return marshal(service, service_fields)
        
        services = Service.query.filter_by(active_flg=True).all()
        return marshal(services, service_fields)

################################## Create Service ###########################################
    @auth_required("token")
    @roles_required("manager")
    def post(self):
        data = request.get_json()
        try:
            from_date_str = data.get('from_date')
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else datetime.now().date()
            
            to_date_str = data.get('to_date')
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if to_date_str else None

            new_service = Service(
                service_desc=data.get('service_desc'),
                service_category=data.get('service_category'),
                from_date=from_date,
                to_date=to_date,
                service_price=data.get('service_price'),
                service_duration=data.get('service_duration'),
                service_products=data.get('service_products')
            )
            db.session.add(new_service)
            update_service_curr_flag(new_service.service_id)
            db.session.commit()
            
            return {"message": "Service created successfully", "service_id": new_service.service_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to create service: {str(e)}"}, 500

################################## Edit Service ###########################################
    @auth_required("token")
    @roles_required("manager")
    def put(self, service_id):
        data = request.get_json()
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404
            
        try:
            service.service_desc = data.get('service_desc', service.service_desc)
            service.service_category = data.get('service_category', service.service_category)
            service.service_price = data.get('service_price', service.service_price)
            service.service_duration = data.get('service_duration', service.service_duration)
            service.service_products = data.get('service_products', service.service_products)
            
            if 'from_date' in data and data['from_date'] is not None and data['from_date'] != "":
                try:
                    service.from_date = datetime.strptime(data['from_date'], '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    return {"message": "Invalid from_date format. Use YYYY-MM-DD"}, 400
            
            if 'to_date' in data:
                if data['to_date'] is None or data['to_date'] == "":
                    service.to_date = None
                else:
                    try:
                        service.to_date = datetime.strptime(data['to_date'], '%Y-%m-%d').date()
                    except (ValueError, TypeError):
                        return {"message": "Invalid to_date format. Use YYYY-MM-DD"}, 400
            update_service_curr_flag(service.service_id)
            db.session.commit()
            
            return {"message": "Service updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update service: {str(e)}"}, 500

################################## Delete Service ###########################################
    @auth_required("token")
    @roles_required("manager")
    def delete(self, service_id):
        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404
            
        # Check if service is used in any appointments or invoices
        has_appointments = Appointment.query.filter_by(service_id=service_id).first()
        has_invoices = Invoice.query.filter_by(service_id=service_id).first()
        
        if has_appointments or has_invoices:
            return {"message": "Cannot delete service with existing appointments or invoices. Consider deactivating it instead."}, 400
            
        try:
            db.session.delete(service)
            db.session.commit()
            return {"message": "Service deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete service: {str(e)}"}, 500

################################## Appointment Resource #####################################
class AppointmentResource(Resource):
################################## Get Appointment #######################################
    @auth_required("token")
    @roles_required("manager")
    def get(self, appointment_id=None):
        cleanup_appointment_history()
        if appointment_id:
            # Fetch single appointment
            appointment = Appointment.query.get(appointment_id)
            if not appointment:
                return {"message": "Appointment not found"}, 404
            
            # Use marshal or manual dict for more control over nested data
            return {
                "appointment_id": appointment.appointment_id,
                "customer_id": appointment.customer_id,
                "customer_name": appointment.customer.customer_name,
                "staff_id": appointment.staff_id,
                "staff_name": appointment.staff.staff_name if appointment.staff else None,
                "datetime": appointment.appointment_datetime.isoformat(),
                "services": [{"id": s.service_id, "name": s.service_desc, "price": s.service_price} 
                             for s in appointment.services if s.active_flg]
            }
        else:
            # Fetch all appointments
            # Filter by date if provided in query params (?date=YYYY-MM-DD)
            date_filter_str = request.args.get('date')
            query = Appointment.query

            if date_filter_str:
                try:
                    filter_date = datetime.strptime(date_filter_str, '%Y-%m-%d').date()
                    query = query.filter(db.func.date(Appointment.appointment_datetime) == filter_date)
                except ValueError:
                    return {"message": "Invalid date format for filter. Use YYYY-MM-DD"}, 400

            appointments = query.all()
            result = []
            for appt in appointments:
                result.append({
                    "appointment_id": appt.appointment_id,
                    "customer_id": appt.customer_id,
                    "customer_name": appt.customer.customer_name,
                    "staff_id": appt.staff_id,
                    "staff_name": appt.staff.staff_name if appt.staff else None,
                    "datetime": appt.appointment_datetime.isoformat(),
                    "services": [{"id": s.service_id, "name": s.service_desc} 
                                 for s in appt.services if s.active_flg]
                })
            return result

################################## Create Appointment #######################################
    @auth_required("token")
    @roles_required("manager")
    def post(self):
        data = request.get_json()
        customer_email = data.get('customer_email')
        staff_id = data.get('staff_id')
        service_ids = data.get('service_ids') # List of service IDs
        datetime_str = data.get('appointment_datetime')

        if not (customer_email and service_ids and datetime_str):
            return {"message": "Missing required fields. Requires: customer_email, appointment_datetime, service_ids"}, 400

        try:
            appt_datetime = datetime.fromisoformat(datetime_str)
        except ValueError:
            return {"message": "Invalid datetime format. Use ISO format YYYY-MM-DDTHH:MM:SS"}, 400

        # Validate customer
        customer = Customer.query.filter_by(customer_email=customer_email).first()
        if not customer: return {"message": "Customer not found"}, 404

        # Validate staff if provided
        if staff_id:
            staff = Staff.query.get(staff_id)
            if not staff: return {"message": "Staff with provided ID not found"}, 404

        # Parse and validate services (must be active)
        if not isinstance(service_ids, list):
            return {"message": "service_ids must be a list of integers"}, 400
            
        services = Service.query.filter(Service.service_id.in_(service_ids), Service.active_flg == True).all()
        
        if len(services) != len(set(service_ids)):
            return {"message": "Some services were either not found, are inactive, or duplicates were provided"}, 400

        try:
            new_appt = Appointment(
                customer_id=customer.customer_id,
                staff_id=staff_id,
                appointment_datetime=appt_datetime
            )
            # Add services to the many-to-many relationship
            new_appt.services.extend(services)
            
            db.session.add(new_appt)
            db.session.commit()
            return {"message": "Appointment created successfully", "appointment_id": new_appt.appointment_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to create appointment: {str(e)}"}, 500

################################## Edit Appointment #######################################
    @auth_required("token")
    @roles_required("manager")

    def put(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {"message": "Appointment not found"}, 404

        data = request.get_json()
        staff_id = data.get('staff_id')
        service_ids = data.get('service_ids') # List of service IDs
        datetime_str = data.get('appointment_datetime')

        try:
            # Handle staff_id updates (including setting to null/None)
            if 'staff_id' in data:
                if staff_id:
                    staff = Staff.query.get(staff_id)
                    if not staff:
                        return {"message": "Staff with provided ID not found"}, 404
                
                appointment.staff_id = staff_id
            
            if datetime_str:
                appointment.appointment_datetime = datetime.fromisoformat(datetime_str)
            
            if 'service_ids' in data:
                if service_ids:
                    if not isinstance(service_ids, list):
                        return {"message": "service_ids must be a list of integers"}, 400
                    
                    # Validate services are active
                    services = Service.query.filter(Service.service_id.in_(service_ids), Service.active_flg == True).all()
                    
                    if len(services) != len(set(service_ids)):
                        return {"message": "Some services were either not found, are inactive, or duplicates were provided"}, 400
                    appointment.services = services
                else:
                    appointment.services = []

            db.session.commit()
            return {"message": "Appointment updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update appointment: {str(e)}"}, 500

################################## Delete Appointment #######################################
    @auth_required("token")
    @roles_required("manager")
    def delete(self, appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {"message": "Appointment not found"}, 404
            
        try:
            db.session.delete(appointment)
            db.session.commit()
            return {"message": "Appointment deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete appointment: {str(e)}"}, 500

################################## Salon Config Resource ####################################
class SalonConfigResource(Resource):
################################## Get Salon Config Data ####################################
    @auth_required("token")
    @roles_required("manager")
    def get(self, setting_id=None):
        if setting_id:
            config = SalonConfig.query.get(setting_id)
            if not config:
                return {"message": "Configuration not found"}, 404
            return marshal(config, salon_config_fields)
        
        configs = SalonConfig.query.all()
        return marshal(configs, salon_config_fields)

################################## Update Salon Config Data ####################################
    @auth_required("token")
    @roles_required("manager")
    def put(self, setting_id):
        config = SalonConfig.query.get(setting_id)
        if not config:
            return {"message": "Configuration not found"}, 404
            
        data = request.get_json()
        try:
            config.param_value = data.get('param_value', config.param_value)
            
            if 'from_date' in data:
                config.from_date = datetime.strptime(data['from_date'], '%Y-%m-%d')
            if 'to_date' in data:
                config.to_date = datetime.strptime(data['to_date'], '%Y-%m-%d')
                
            db.session.commit()
            return {"message": "Configuration updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update configuration: {str(e)}"}, 500
        
################################## Staff Appointments Resource ##############################
class StaffAppointmentResource(Resource):
################################## Get Staff Appointments (in Staff dashboard) ##############
    @auth_required("token")
    @roles_required("staff")
    def get(self):
        cleanup_appointment_history() # Cleanup old appointments before fetching staff-specific data
        # Always use the ID of the currently logged-in staff member
        target_staff_id = current_user.id
        
        staff = Staff.query.get(target_staff_id)
        if not staff:
            return {"message": "Staff member profile not found for current user"}, 404
        
        # Get 'mode' from query params. Options: 'today' (default) or 'all'
        mode = request.args.get('mode', 'today')
        
        query = Appointment.query.filter(Appointment.staff_id == target_staff_id)

        if mode == 'today':
            target_date = date.today()
            appointments = query.filter(db.func.date(Appointment.appointment_datetime) == target_date).all()
            if not appointments:
                return {"message": f"No appointments found for {staff.staff_name} today ({target_date})"}, 404
        elif mode == 'all':
            appointments = query.all()
            if not appointments:
                return {"message": f"No appointments found for {staff.staff_name}"}, 404
        else:
            return {"message": "Invalid mode. Use 'today' or 'all'."}, 400

        result = []
        for appt in appointments:
            result.append({
                "appointment_id": appt.appointment_id,
                "customer_name": appt.customer.customer_name,
                "datetime": appt.appointment_datetime.isoformat(),
                "services": [{"id": s.service_id, "name": s.service_desc} for s in appt.services]
            })
        return result

################################## Staff Attendance Resource ################################
staff_attendance_fields = {
    'register_id': fields.Integer,
    'staff_id': fields.Integer,
    'register_datetime': fields.String,
}

class StaffAttendanceResource(Resource):
################################## Get Staff Attendance  ##############################
    @auth_required("token")
    def get(self, staff_id=None):
        # Determine target user role
        user_roles = [r.name for r in current_user.roles] if current_user else []
        
        # Determine if we should treat this as a Manager request or a Staff request
        # If user is a manager, they get date-based access to all staff
        if "manager" in user_roles:
            date_str = request.args.get('date') # Format: YYYY-MM-DD
            
            if date_str:
                # 1. Manager selecting a particular date
                try:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400
            else:
                # 2. Manager default: Today
                target_date = date.today()

            start_of_day = datetime.combine(target_date, datetime.min.time())
            end_of_day = datetime.combine(target_date, datetime.max.time())
            
            records = StaffAttendance.query.filter(
                StaffAttendance.register_datetime >= start_of_day,
                StaffAttendance.register_datetime <= end_of_day
            ).all()

            if not records:
                return {"message": f"No attendance records found for {target_date}"}, 404

        # If user is a staff (and NOT a manager, or we specifically want staff behavior)
        elif "staff" in user_roles:
            # 3. Particular staff (current_user.id) fetching for current month
            target_staff_id = current_user.id
            today = date.today()
            
            records = StaffAttendance.query.filter(
                StaffAttendance.staff_id == target_staff_id,
                db.extract('month', StaffAttendance.register_datetime) == today.month,
                db.extract('year', StaffAttendance.register_datetime) == today.year
            ).all()

            if not records:
                return {"message": f"No attendance records found for current month for you"}, 404
        else:
            return {"message": "Unauthorized role"}, 403

        return marshal(records, staff_attendance_fields)

        if not records:
                return {"message": f"No attendance records found for current month"}, 404
        else:
            return {"message": "Unauthorized role"}, 403

        return marshal(records, staff_attendance_fields)

    @auth_required("token")
    @roles_required("staff")
    def post(self):
        # Staff marking their own attendance for "now"
        try:
            # Check if already marked today to prevent duplicates (optional logic)
            today = date.today()
            already_marked = StaffAttendance.query.filter(
                StaffAttendance.staff_id == current_user.id,
                db.func.date(StaffAttendance.register_datetime) == today
            ).first()

            if already_marked:
                return {"message": "Attendance already marked for today"}, 400

            new_attendance = StaffAttendance(
                staff_id=current_user.id,
                register_datetime=datetime.now()
            )
            db.session.add(new_attendance)
            db.session.commit()
            return {"message": "Attendance marked successfully", "time": new_attendance.register_datetime.isoformat()}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to mark attendance: {str(e)}"}, 500

################################## Maintenance: Cleanup History ##############################
class AppointmentHistoryCleanup(Resource):
    @auth_required("token")
    @roles_required("manager")
    def delete(self):
        success, result = cleanup_appointment_history()
        
        if success:
            if isinstance(result, int):
                return {"message": f"Successfully deleted {result} appointments based on retention policy."}, 200
            else:
                return {"message": "Retention cleanup completed."}, 200
        else:
            return {"message": f"Cleanup failed: {result}"}, 500

#############################################################################################
# Add API resources to the app

api.add_resource(Owner, '/create-manager') #post
api.add_resource(ManagerResource, '/manager', '/manager/<int:manager_id>')
api.add_resource(ChangePassword, '/change-password')
api.add_resource(ProductResource, '/product', '/product/<int:product_id>')
api.add_resource(CustomerResource, '/customer', '/customer/<int:customer_id>')
api.add_resource(StaffResource, '/staff', '/staff/<int:staff_id>')
api.add_resource(ServiceResource, '/service', '/service/<int:service_id>')
api.add_resource(AppointmentResource, '/appointment', '/appointment/<int:appointment_id>')
api.add_resource(SalonConfigResource, '/salon-config', '/salon-config/<int:setting_id>')
api.add_resource(StaffAppointmentResource, '/staff-appointments')
api.add_resource(StaffAttendanceResource, '/staff-attendance', '/staff-attendance/<int:staff_id>')
api.add_resource(AppointmentHistoryCleanup, '/cleanup-appointments')
api.add_resource(InventoryTransactionResource, '/inventory-transaction', '/inventory-transaction/<int:txn_id>')
