from flask_restful import Resource, Api, reqparse, marshal_with, fields, marshal
from flask_security import auth_required, roles_required, roles_accepted, current_user, hash_password, verify_password
from datetime import datetime, timedelta, date
from flask import request, jsonify, send_file, current_app
from flask_mail import Message
import csv
import io
import os
from fpdf import FPDF
from .sec import datastore
from .models import Service, Staff, Customer, User, Product, Appointment, Invoice, InventoryTransaction, StaffAttendance, CustomerReview, Finance, Manager, Owner, CustomerReward, SalonConfig, db, Role, UserRoles, appointment_services, Order, Notification
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


################################## Order Fields ########################################
order_fields = {
    'order_id': fields.Integer,
    'product_id': fields.Integer,
    'product_name': fields.String(attribute='product.product_desc'),
    'product_quantity': fields.Integer(attribute='product.product_curr_qoh'),
    'order_quantity': fields.Integer,
    'order_cost': fields.Float,
    'order_date': fields.DateTime,
    'order_replenishment_date': fields.DateTime,
    'reason_for_order': fields.String,
    'supplier_name': fields.String(attribute='product.product_supplier_name'),
    'supplier_email': fields.String(attribute='product.product_supplier_email'),
    'status': fields.Integer
}

################################## Order API ########################################
##################################Create Orders########################################
class OrderResource(Resource):
    @auth_required("token")
    @roles_required("manager")
    def post(self, order_id=None):
        """
        Create a replenishment order for a product.
        Managers use this to request stock from suppliers.
        """
        data = request.get_json()
        product_id = data.get('product_id')
        order_quantity = data.get('order_quantity')
        reason_for_order = data.get('reason_for_order')

        if not product_id or not order_quantity:
            return {"message": "Missing product_id or order_quantity"}, 400

        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found"}, 404

        try:
            # Create the order record
            new_order = Order(
                product_id=product_id,
                order_quantity=order_quantity,
                order_cost=order_quantity * product.product_price,
                reason_for_order=reason_for_order,
                supplier_name=product.product_supplier_name,
                supplier_email=product.product_supplier_email,
                status=0 # 0 for Pending
            )
            
            
            db.session.add(new_order)
            db.session.commit()

            return {
                "message": "Replenishment order created successfully", 
                "order": marshal(new_order, order_fields),
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to create order: {str(e)}"}, 500

##################################Get Orders########################################
    @auth_required("token")
    @roles_required("manager")
    def get(self, order_id=None):
        if order_id:
            order = Order.query.get(order_id)
            if not order:
                return {"message": "Order not found"}, 404
            return marshal(order, order_fields), 200
        
        orders = Order.query.all()
        return marshal(orders, order_fields), 200

##################################Edit Orders########################################
    @auth_required("token")
    @roles_required("manager")
    def put(self, order_id):
        """
        Update order status (e.g., from Pending (0) to Processed (1), Cancelled (2)).
        """
        order = Order.query.get(order_id)
        if not order:
            return {"message": "Order not found"}, 404

        data = request.get_json()
        new_status = data.get('status')
        new_quantity = data.get('order_quantity')
        new_cost = data.get('order_cost')
        new_replenishment_date_str = data.get('order_replenishment_date')
        reason = data.get('reason_for_order')

        if new_status is not None:
            order.status = new_status
            # If status flips to Processed (1) and no date was provided, default to now
            if new_status == 1 and not order.order_replenishment_date and not new_replenishment_date_str:
                order.order_replenishment_date = datetime.now()
            # If status flips to Cancelled (2), clear the replenishment date
            elif new_status == 2:
                order.order_replenishment_date = None
        
        if new_replenishment_date_str:
            try:
                order.order_replenishment_date = datetime.strptime(new_replenishment_date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    order.order_replenishment_date = datetime.strptime(new_replenishment_date_str, '%Y-%m-%d')
                except ValueError:
                    return {"message": "Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS"}, 400

        if new_quantity is not None and new_status == 1:
            # replenishing the qoh in the inventory_master table if the order is processed (status = 1).
            product = Product.query.get(order.product_id)
            if product:
                product.product_curr_qoh += new_quantity
                update_low_stock_alerts(order.product_id)
                order.order_quantity = new_quantity
                order.order_cost = new_quantity * product.product_price
        #allowing the manager to update the cost in case it differs from the initially calculated cost based on price changes or negotiations with the supplier.
        if new_cost is not None:
            order.order_cost = new_cost
        
        if reason:
            order.reason_for_order = reason

        try:
            db.session.commit()
            return {"message": "Order updated successfully", "order": marshal(order, order_fields)}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update order: {str(e)}"}, 500

##################################Delete Orders########################################
    @auth_required("token")
    @roles_required("manager")
    def delete(self, order_id):
        """
        Delete an order record by order_id.
        Only managers can delete order records.
        """
        order = Order.query.get(order_id)
        if not order:
            return {"message": "Order not found"}, 404

        try:
            db.session.delete(order)
            db.session.commit()
            return {"message": "Order deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete order: {str(e)}"}, 500

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
    'customer_available_rewards': fields.Integer,
    'total_spend': fields.Float
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
                customer_type='Regular',
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
    'no_of_reviews': fields.Integer,
    'is_present_today': fields.Boolean,
    'appointments_today': fields.Integer,
    'active': fields.Boolean(attribute='user.active')
}

################################## Staff API ############################################
class StaffResource(Resource):

################################## Fetch Staff ############################################
    @auth_required("token")
    def get(self, staff_id=None):
        today = date.today()
        
        if staff_id:
            staff = Staff.query.get(staff_id)
            if not staff:
                return {"message": "Staff member not found"}, 404
            
            # Check attendance for today
            attendance = StaffAttendance.query.filter(
                StaffAttendance.staff_id == staff_id,
                StaffAttendance.present_flag == True
            ).first()

            # Count appointments for today
            appointment_count = Appointment.query.filter(
                Appointment.staff_id == staff_id,
                db.func.date(Appointment.appointment_datetime) == today
            ).count()
            
            staff_data = marshal(staff, staff_fields)
            staff_data['is_present_today'] = attendance is not None
            staff_data['appointments_today'] = appointment_count
            staff_data['active'] = staff.user.active
            return staff_data
        
        staff_members = Staff.query.all()
        results = []
        for staff in staff_members:
            attendance = StaffAttendance.query.filter(
                StaffAttendance.staff_id == staff.staff_id,
                StaffAttendance.present_flag == True
            ).first()

            appointment_count = Appointment.query.filter(
                Appointment.staff_id == staff.staff_id,
                db.func.date(Appointment.appointment_datetime) == today
            ).count()
            
            staff_data = marshal(staff, staff_fields)
            staff_data['is_present_today'] = attendance is not None
            staff_data['appointments_today'] = appointment_count
            staff_data['active'] = staff.user.active
            results.append(staff_data)
            
        return results

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
            
        new_user = User(username=username, password=hash_password(password), active=data.get('active', True))
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
            
            if 'active' in data:
                staff.user.active = data['active']
                
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
        
        # Managers can see all services (including deleted/inactive)
        services = Service.query.all()
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
            
        # 1. Correct check for Many-to-Many appointments
        # The 'appointment_services' table handles linking services to appointments
        has_appointments = db.session.query(appointment_services).filter_by(service_id=service_id).first()
        
        # 2. Correct check for Invoices (stored as string like '1,2,3')
        # Search for the service_id within the comma-separated string
        search_pattern = f"%{service_id}%"
        has_invoices = Invoice.query.filter(Invoice.service_ids.like(search_pattern)).first()
        
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
                "status": appointment.status,
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
                    "status": appt.status,
                    "services": [{"id": s.service_id, "name": s.service_desc, "price": s.service_price} 
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
        status = data.get('status')

        try:
            if 'status' in data:
                appointment.status = status
            
            # Handle staff_id updates (including setting to null/None)
            if 'staff_id' in data:
                if staff_id:
                    staff = Staff.query.get(staff_id)
                    if not staff:
                        return {"message": "Staff with provided ID not found"}, 404
                
                appointment.staff_id = staff_id
            
            if datetime_str:
                new_datetime = datetime.fromisoformat(datetime_str)
                if appointment.appointment_datetime != new_datetime:
                    appointment.appointment_datetime = new_datetime
                    appointment.status = 4 # Set to Rescheduled if datetime changes
            
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
            # Allow updating based on param_name for convenience if desired, 
            # but primary logic here updates param_value from the request body.
            # The user provided {"SALON_CLOSE_TIME": "23:00"} which suggests a key-value pair
            # matching param_name and new param_value.
            
            updated = False
            # Check if the param_name matches the request key
            if config.param_name in data:
                config.param_value = str(data[config.param_name])
                updated = True
            
            # Also support standard 'param_value' key
            if 'param_value' in data:
                config.param_value = data['param_value']
                updated = True
            
            if not updated and not any(k in data for k in ['from_date', 'to_date']):
                return {"message": "No valid parameters provided for update"}, 400
            
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
    'present_flag': fields.Boolean
}

class ManagerStaffAttendance(Resource):
################################## Get Staff Attendance for Manager ##############################
    @auth_required("token")
    @roles_required("manager")
    def get(self):
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

        return marshal(records, staff_attendance_fields)

class StaffAttendanceResource(Resource):
################################## Get Staff Attendance for Staff ##############################
    @auth_required("token")
    @roles_required("staff")
    def get(self):
        # Particular staff (current_user.id) fetching for current month
        target_staff_id = current_user.id
        today = date.today()
        
        records = StaffAttendance.query.filter(
            StaffAttendance.staff_id == target_staff_id,
           StaffAttendance.present_flag == True
        ).all()

        if not records:
            return {"message": f"No attendance records found for current month for you"}, 404

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
                StaffAttendance.present_flag == True
            ).first()

            if already_marked:
                return {"message": "Attendance already marked for today"}, 400

            new_attendance = StaffAttendance(
                staff_id=current_user.id,
                register_datetime=datetime.now(),
                present_flag=True
            )
            db.session.add(new_attendance)
            db.session.commit()
            return {"message": "Attendance marked successfully", "time": new_attendance.register_datetime.isoformat()}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to mark attendance: {str(e)}"}, 500

class MarkStaffAbsent(Resource):
    @auth_required("token")
    @roles_required("manager")
    def post(self):
        # Manager marking absent for current day for all staff members who haven't marked attendance
        try:
            today = date.today()
            all_staff = Staff.query.all()
            
            # Subquery to find staff who have already marked attendance today
            marked_staff_ids = db.session.query(StaffAttendance.staff_id).filter(
                StaffAttendance.present_flag == True
            ).all()
            marked_ids = [s[0] for s in marked_staff_ids]
            
            absent_count = 0
            for staff in all_staff:
                if staff.staff_id not in marked_ids:
                    # Mark as absent (present_flag = False)
                    absent_record = StaffAttendance(
                        staff_id=staff.staff_id,
                        register_datetime=datetime.now(),
                        present_flag=False
                    )
                    db.session.add(absent_record)
                    absent_count += 1
            
            db.session.commit()
            return {"message": f"Bulk attendance processing complete. {absent_count} staff members marked as absent for today."}, 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to mark staff absent: {str(e)}"}, 500
        
########################### Create CSV for Pending Orders Grouped by Supplier ############################
class SupplierOrderReportResource(Resource):
    @auth_required("token")
    @roles_required("manager")
    def get(self):
        # API to aggregate pending orders (status=0) by supplier email and generate CSV files.
        try:
            pending_orders = Order.query.filter_by(status=0).all()
            if not pending_orders:
                return {"message": "No pending orders found."}, 404

            # Aggregate by supplier email
            supplier_data = {}
            for order in pending_orders:
                email = order.supplier_email
                if email not in supplier_data:
                    supplier_data[email] = []
                supplier_data[email].append(order)

            # Define report directory
            report_dir = os.path.join(os.getcwd(), 'reports', 'supplier_orders')
            if not os.path.exists(report_dir):
                os.makedirs(report_dir, exist_ok=True)

            generated_files = []
            for email, orders in supplier_data.items():
                # Get supplier name from first order
                supplier_name = orders[0].supplier_name if orders else "Unknown_Supplier"
                
                # Format month and year
                current_month = date.today().strftime('%B')
                current_year = date.today().year
                
                # Sanitize filename components
                safe_supplier_name = supplier_name.replace(' ', '_').replace('/', '_')
                filename = f"{safe_supplier_name}_{current_month}_{current_year}.csv"
                filepath = os.path.join(report_dir, filename)

                with open(filepath, 'w', newline='') as csvfile:
                    # Header with Supplier Name
                    csvfile.write(f"Supplier Name: {supplier_name}\n")
                    
                    fieldnames = ['product_desc', 'order_quantity', 'order_date', 'reason_for_order']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for order in orders:
                        writer.writerow({
                            'product_desc': order.product.product_desc if order.product else "Unknown",
                            'order_quantity': order.order_quantity,
                            'order_date': order.order_date.isoformat(),
                            'reason_for_order': order.reason_for_order
                        })
                generated_files.append(filename)

            return {
                "message": f"Successfully generated {len(generated_files)} supplier reports.",
                "directory": report_dir,
                "files": generated_files
            }, 200

        except Exception as e:
            return {"message": f"Failed to generate supplier reports: {str(e)}"}, 500
        

#####################################   CSV to PDF Conversion Resource #####################################
class CSVToPDFResource(Resource):
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def post(self):
        if 'file' not in request.files:
            return {"message": "No file part in the request"}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {"message": "No selected file"}, 400
        
        if not file.filename.endswith('.csv'):
            return {"message": "Only CSV files are allowed"}, 400

        try:
            # Read CSV content
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(stream)
            data = list(csv_reader)

            if not data:
                return {"message": "CSV file is empty"}, 400

            # Generate PDF using fpdf2
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Determine column widths
            col_width = pdf.epw / len(data[0]) if data[0] else pdf.epw
            line_height = pdf.font_size * 2

            for row in data:
                for datum in row:
                    pdf.multi_cell(col_width, line_height, str(datum), border=1, ln=3, max_line_height=pdf.font_size)
                pdf.ln(line_height)

            # Return PDF as a download
            pdf_output = io.BytesIO(pdf.output())
            return send_file(
                pdf_output,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"{os.path.splitext(file.filename)[0]}.pdf"
            )

        except Exception as e:
            return {"message": f"Conversion failed: {str(e)}"}, 500

################################## Staff Customer Review API ################################
class StaffCustomerReview(Resource):
    @auth_required("token")
    @roles_required("staff")
    def get(self):
        # Fetch all customer reviews for the particular staff member who is logged in
        target_staff_id = current_user.id
        
        staff = Staff.query.get(target_staff_id)
        if not staff:
            return {"message": "Staff profile not found"}, 404
        
        reviews = CustomerReview.query.filter_by(staff_id=target_staff_id).all()
        
        result = []
        for review in reviews:
            # Map service_ids string to service names
            service_names = []
            if review.service_ids:
                s_ids = [int(sid.strip()) for sid in review.service_ids.split(",") if sid.strip().isdigit()]
                services = Service.query.filter(Service.service_id.in_(s_ids)).all()
                service_names = [s.service_desc for s in services]

            result.append({
                "review_id": review.review_id,
                "customer_name": review.customer.customer_name,
                "rating": review.rating,
                "review": review.review,
                "appointment_id": review.apppointment_id,
                "service_ids": review.service_ids,
                "service_names": service_names
            })
            
        return result, 200

################################## Current Staff Resource #################################
class CurrentStaffResource(Resource):
    @auth_required("token")
    @roles_required("staff")
    def get(self):
        """Fetch the current logged-in staff member's profile information"""
        staff_id = current_user.id
        
        staff = Staff.query.get(staff_id)
        if not staff:
            return {"message": "Staff profile not found"}, 404
        
        staff_data = marshal(staff, staff_fields)
        staff_data['active'] = staff.user.active
        return staff_data, 200

    @auth_required("token")
    @roles_required("staff")
    def put(self):
        """Update the current logged-in staff member's own profile"""
        staff_id = current_user.id
        
        staff = Staff.query.get(staff_id)
        if not staff:
            return {"message": "Staff profile not found"}, 404
        
        data = request.get_json()
        
        try:
            staff.staff_name = data.get('staff_name', staff.staff_name)
            staff.staff_contact = data.get('staff_contact', staff.staff_contact)
            staff.staff_email = data.get('staff_email', staff.staff_email)
            staff.staff_skills = data.get('staff_skills', staff.staff_skills)
            
            if 'staff_dob' in data and data['staff_dob']:
                staff.staff_dob = datetime.strptime(data['staff_dob'], '%Y-%m-%d').date()
            
            db.session.commit()
            return {"message": "Profile updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update profile: {str(e)}"}, 500

################################## Current Customer Resource ###############################
class CurrentCustomerResource(Resource):
    @auth_required("token")
    @roles_required("customer")
    def get(self):
        """Fetch the current logged-in customer's profile information"""
        customer_id = current_user.id
        
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"message": "Customer profile not found"}, 404
        
        customer_data = marshal(customer, customer_fields)
        return customer_data, 200

    @auth_required("token")
    @roles_required("customer")
    def put(self):
        """Update the current logged-in customer's own profile"""
        customer_id = current_user.id
        
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"message": "Customer profile not found"}, 404
        
        data = request.get_json()
        
        try:
            customer.customer_name = data.get('customer_name', customer.customer_name)
            customer.customer_contact = data.get('customer_contact', customer.customer_contact)
            customer.customer_email = data.get('customer_email', customer.customer_email)
            customer.customer_address = data.get('customer_address', customer.customer_address)
            customer.customer_preferences = data.get('customer_preferences', customer.customer_preferences)
            
            if 'customer_dob' in data and data['customer_dob']:
                customer.customer_dob = datetime.strptime(data['customer_dob'], '%Y-%m-%d').date()
            
            db.session.commit()
            return {"message": "Profile updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update profile: {str(e)}"}, 500

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

################################## Salon Daily Appointment Count Resource ##############################
class SalonDailyAppointmentCountResource(Resource):
    @auth_required("token")
    @roles_required("manager")
    def get(self):
        # Fetch daily counts of appointments from the Appointment table
        try:
            results = db.session.query(
                db.func.date(Appointment.appointment_datetime).label('date'),
                db.func.count(Appointment.appointment_id).label('count')
            ).group_by(
                db.func.date(Appointment.appointment_datetime)
            ).order_by(
                'date'
            ).all()

            # Format the results into a list of dictionaries
            daily_counts = [
                {"date": str(row.date), "count": row.count}
                for row in results
            ]
            
            if not daily_counts:
                return [], 200
                
            return daily_counts, 200
        except Exception as e:
            return {"message": f"Error fetching appointment counts: {str(e)}"}, 500

################################## Staff Dashboard API ##############################
class StaffDashboard(Resource):
    @auth_required("token")
    @roles_required("staff")
    def get(self):
        # Fetch the staff ID of the current user
        staff_id = current_user.id
        today = date.today()
        
        # 1. Total number of appointments today
        total_appointments_today = Appointment.query.filter(
            Appointment.staff_id == staff_id,
            db.func.date(Appointment.appointment_datetime) == today
        ).count()
        
        # 2. Total number of completed appointments today
        # Assuming status 3 is 'Completed' based on context in resources.py
        completed_appointments_today = Appointment.query.filter(
            Appointment.staff_id == staff_id,
            db.func.date(Appointment.appointment_datetime) == today,
            Appointment.status == 1
        ).count()
        
        return {
            "total_appointments_today": total_appointments_today,
            "completed_appointments_today": completed_appointments_today
        }, 200

################################## Customer Appointment APIs ##############################

###################################### For customer to fetch a specific appoint ment data ################
class CustomerAppointment(Resource):
    @auth_required("token")
    @roles_required("customer")
    def get(self, appointment_id):
        appointment = Appointment.query.filter_by(appointment_id=appointment_id, customer_id=current_user.id).first()
        if not appointment:
            return {"message": "Appointment not found or unauthorized"}, 404
        
        return {
            "appointment_id": appointment.appointment_id,
            "staff_id": appointment.staff_id,
            "staff_name": appointment.staff.staff_name if appointment.staff else None,
            "appointment_datetime": appointment.appointment_datetime.isoformat(),
            "status": appointment.status,
            "services": [{"service_id": s.service_id, "service_desc": s.service_desc, "service_price": s.service_price} 
                         for s in appointment.services]
        }

###################################### For customer to update/reschedule a specific appointment  ################
    @auth_required("token")
    @roles_required("customer")
    def put(self, appointment_id):
        appointment = Appointment.query.filter_by(appointment_id=appointment_id, customer_id=current_user.id).first()
        if not appointment:
            return {"message": "Appointment not found or unauthorized"}, 404
        
        if appointment.status not in [0, 4]:
            return {"message": "Only 'Booked' and 'Rescheduled' appointments can be updated"}, 400

        data = request.get_json()
        staff_id = data.get('staff_id')
        service_ids = data.get('service_ids')
        datetime_str = data.get('appointment_datetime')
        status = 4 # Rescheduled status when customer updates the appointment

        try:
            if staff_id is not None:
                appointment.staff_id = staff_id
            
            if datetime_str:
                appointment.appointment_datetime = datetime.fromisoformat(datetime_str)
            if status:
                appointment.status = status
            if service_ids is not None:
                if not isinstance(service_ids, list):
                    return {"message": "service_ids must be a list of integers"}, 400
                
                services = Service.query.filter(Service.service_id.in_(service_ids), Service.active_flg == True).all()
                if len(services) != len(set(service_ids)):
                    return {"message": "Some services were either not found or are inactive"}, 400
                appointment.services = services

            db.session.commit()
            return {"message": "Appointment updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update appointment: {str(e)}"}, 500

###################################### For customer to delete a specific appointment  ################
    @auth_required("token")
    @roles_required("customer")
    def delete(self, appointment_id):
        appointment = Appointment.query.filter_by(appointment_id=appointment_id, customer_id=current_user.id).first()
        if not appointment:
            return {"message": "Appointment not found or unauthorized"}, 404
        
        if appointment.status not in [0, 4]:
            return {"message": "Only 'Booked' and 'Rescheduled' appointments can be cancelled/deleted"}, 400
            
        try:
            db.session.delete(appointment)
            db.session.commit()
            return {"message": "Appointment cancelled and deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to delete appointment: {str(e)}"}, 500

class CustomerUpcomingAppointmentsResource(Resource):
    @auth_required("token")
    @roles_required("customer")
    def get(self):
        # Always use the ID of the currently logged-in customer
        target_customer_id = current_user.id
        
        customer = Customer.query.get(target_customer_id)
        if not customer:
            return {"message": "Customer profile not found"}, 404
        
        # 0: Booked, 4: Rescheduled (both are upcoming appointments)
        upcoming_appointments = Appointment.query.filter_by(customer_id=target_customer_id).filter(
            Appointment.status.in_([0, 4])
        ).all()

        result = []
        for appt in upcoming_appointments:
            result.append({
                "appointment_id": appt.appointment_id,
                "staff_id": appt.staff_id,
                "staff_name": appt.staff.staff_name if appt.staff else "Not Assigned",
                "datetime": appt.appointment_datetime.isoformat(),
                "status": appt.status,
                "services": [
                    {
                        "service_id": s.service_id,
                        "service_name": s.service_desc,
                        "price": s.service_price
                    } for s in appt.services
                ],
                "total_price": sum(s.service_price for s in appt.services)
            })

        return result, 200

##################################Customer Book Appointment API (for Customers to book appointments by themselves) ##############################
    @auth_required("token")
    @roles_required("customer")
    def post(self):
        target_customer_id = current_user.id
        data = request.get_json()
        
        staff_id = data.get('staff_id') # Optional
        service_ids = data.get('service_ids') # List of service IDs
        datetime_str = data.get('appointment_datetime')

        if not (service_ids and datetime_str):
            return {"message": "Missing required fields: appointment_datetime, service_ids"}, 400

        try:
            appt_datetime = datetime.fromisoformat(datetime_str)
        except ValueError:
            return {"message": "Invalid datetime format. Use ISO format YYYY-MM-DDTHH:MM:SS"}, 400

        # Validate customer
        customer = Customer.query.get(target_customer_id)
        if not customer:
            return {"message": "Customer profile not found"}, 404

        # Validate staff if provided
        if staff_id:
            staff = Staff.query.get(staff_id)
            if not staff:
                return {"message": "Staff with provided ID not found"}, 404

        # Parse and validate services (must be active)
        if not isinstance(service_ids, list):
            return {"message": "service_ids must be a list of integers"}, 400
            
        services = Service.query.filter(Service.service_id.in_(service_ids), Service.active_flg == True).all()
        
        if len(services) != len(set(service_ids)):
            return {"message": "Some services were either not found, are inactive, or duplicates were provided"}, 400

        try:
            new_appt = Appointment(
                customer_id=target_customer_id,
                staff_id=staff_id,
                appointment_datetime=appt_datetime,
                status=0 # Booked
            )
            # Add services to the many-to-many relationship
            new_appt.services.extend(services)
            
            db.session.add(new_appt)
            db.session.commit()
            
            # Since rewards depend on available_rewards, we should refresh/sync them
            invalidate_expired_points(target_customer_id)
            
            return {"message": "Appointment booked successfully", "appointment_id": new_appt.appointment_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to book appointment: {str(e)}"}, 500

class CustomerHistoryAppointmentsResource(Resource):
    @auth_required("token")
    @roles_required("customer")
    def get(self):
        # Always use the ID of the currently logged-in customer
        target_customer_id = current_user.id
        
        customer = Customer.query.get(target_customer_id)
        if not customer:
            return {"message": "Customer profile not found"}, 404
        
        # 1: Completed, 2: No-show, 3: Cancelled, 4: Rescheduled, 5: Invoiced (anything not 0)
        history_appointments = Appointment.query.filter(Appointment.customer_id == target_customer_id, Appointment.status != 0).all()

        result = []
        status_map = {
            1: "Completed",
            2: "No-show",
            3: "Cancelled",
            4: "Rescheduled",
            5: "Invoiced"
        }
        for appt in history_appointments:
            staff_name = appt.staff.staff_name if appt.staff else "Not Assigned"
            appt_time = appt.appointment_datetime.isoformat()
            
            # Fetch rating from CustomerReview if an invoice exists
            rating = None
            invoice = Invoice.query.filter_by(customer_id=target_customer_id, staff_id=appt.staff_id, invoice_date=appt.appointment_datetime.date()).first()
            if invoice:
                review = CustomerReview.query.filter_by(invoice_number=invoice.invoice_number).first()
                if review:
                    rating = review.rating

            for service in appt.services:
                result.append({
                    "appointment_id": appt.appointment_id,
                    "service_name": service.service_desc,
                    "staff_name": staff_name,
                    "datetime": appt_time,
                    "price": service.service_price,
                    "status": status_map.get(appt.status, f"Unknown ({appt.status})"),
                    "rating": rating
                })

        return result, 200

class CustomerSummaryResource(Resource):
    @auth_required("token")
    @roles_required("customer")
    def get(self):
        target_customer_id = current_user.id
        
        # Check and allot birthday bonus points if applicable
        birthday_bonus_rewards(target_customer_id)
        
        customer = Customer.query.get(target_customer_id)
        if not customer:
            return {"message": "Customer profile not found"}, 404
        
        upcoming_count = Appointment.query.filter_by(customer_id=target_customer_id, status=0).count()
        past_count = Appointment.query.filter(Appointment.customer_id == target_customer_id, Appointment.status != 0).count()
        
        return {
            "customer_type": customer.customer_type,
            "upcoming_appointments_count": upcoming_count,
            "past_appointments_count": past_count,
            "available_rewards": customer.customer_available_rewards
        }, 200

###############################Customer Review API (for Customers to submit reviews for completed appointments) ##############################
###################################### Fetch pending reviews (appointments completed but not yet reviewed) ######################################
class CustomerReviewResource(Resource):
    @auth_required("token")
    @roles_required("customer")
    def get(self, invoice_number=None):
        target_customer_id = current_user.id
        
        # Fetch invoices for current customer for which feedback_given is false in the appointment table
        # We join Invoice with Appointment to check the feedback_given flag
        query = db.session.query(Invoice).join(
            Appointment, Invoice.appointment_id == Appointment.appointment_id
        ).filter(
            Invoice.customer_id == target_customer_id,
            Appointment.feedback_given == False
        )

        if invoice_number:
            query = query.filter(Invoice.invoice_number == invoice_number)
        
        pending_reviews = query.all()
        
        result = []
        for inv in pending_reviews:
            appt = inv.appointment
            if appt:
                result.append({
                    "invoice_number": inv.invoice_number,
                    "appointment_id": inv.appointment_id,
                    "staff_name": appt.staff.staff_name if appt.staff else (inv.staff.staff_name if inv.staff else "Unknown"),
                    "datetime": appt.appointment_datetime.isoformat(),
                    "services": [s.service_desc for s in appt.services]
                })
        
        if invoice_number and not result:
            return {"message": "Invoice not found, unauthorized, or already reviewed"}, 404

        return result, 200

################################# To Save Custmer Review ############################################
    @auth_required("token")
    @roles_required("customer")
    def post(self, invoice_number):
        target_customer_id = current_user.id
        data = request.get_json()
        
        rating = data.get('rating')
        review_text = data.get('review')

        if rating is None:
            return {"message": "Rating is required"}, 400

        # Fetch invoice details for the specific invoice_number
        invoice = Invoice.query.filter_by(
            customer_id=target_customer_id,
            invoice_number=invoice_number
        ).first()

        if not invoice:
            return {"message": "Invoice not found or unauthorized"}, 404

        appointment = invoice.appointment
        if not appointment:
            return {"message": "Associated appointment not found"}, 404

        if appointment.feedback_given:
            return {"message": "Feedback already given for this invoice"}, 400

        if appointment.status not in [1, 5]:
            return {"message": "Can only review completed or invoiced appointments"}, 400

        try:
            # Create CustomerReview record using fields from the Invoice table
            new_review = CustomerReview(
                customer_id=target_customer_id,
                staff_id=invoice.staff_id,
                apppointment_id=invoice.appointment_id,
                invoice_number=invoice.invoice_number,
                service_ids=invoice.service_ids,
                rating=rating,
                review=review_text
            )
            db.session.add(new_review)
            
            # Update Appointment feedback_given flag
            appointment.feedback_given = True
            
            # Update Staff and Service ratings
            update_staff_rating(invoice.staff_id, rating)
            
            # Use service_ids from invoice to update individual service ratings
            if invoice.service_ids:
                service_id_list = [int(sid.strip()) for sid in invoice.service_ids.split(",") if sid.strip().isdigit()]
                for s_id in service_id_list:
                    update_service_rating(s_id, rating)
            
            db.session.commit()
            return {"message": "Review and rating submitted successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to submit review: {str(e)}"}, 500
    
########################### To fetch appointments for current customer where feedback_given ###########
class CustomerReviewedAppointments(Resource):
    @auth_required("token")
    @roles_accepted("customer", "manager")
    def get(self):
        # For managers, fetch all reviews; for customers, fetch only their own
        if current_user.has_role("manager"):
            # Fetch all reviews for manager view
            reviewed_invoices = db.session.query(Invoice).join(
                Appointment, Invoice.appointment_id == Appointment.appointment_id
            ).filter(
                Appointment.feedback_given == True
            ).all()
        else:
            # Fetch only current customer's reviews
            target_customer_id = current_user.id
            reviewed_invoices = db.session.query(Invoice).join(
                Appointment, Invoice.appointment_id == Appointment.appointment_id
            ).filter(
                Invoice.customer_id == target_customer_id,
                Appointment.feedback_given == True
            ).all()
        
        result = []
        for inv in reviewed_invoices:
            appt = inv.appointment
            if appt:
                # Look for corresponding review in customer_review table using appointment_id or invoice_number
                review = CustomerReview.query.filter_by(
                    customer_id=inv.customer_id,
                    apppointment_id=appt.appointment_id
                ).first()
                
                result.append({
                    "invoice_number": inv.invoice_number,
                    "appointment_id": appt.appointment_id,
                    "customer_name": inv.customer.customer_name if inv.customer else "Unknown",
                    "staff_name": appt.staff.staff_name if appt.staff else "Unknown",
                    "datetime": appt.appointment_datetime.isoformat(),
                    "services": [s.service_desc for s in appt.services],
                    "rating": review.rating if review else None,
                    "review": review.review if review else "No review text"
                })
        return result, 200

##################################### Saving Customer Reviews ######################################
    @auth_required("token")
    @roles_required("customer")
    def post(self):
        target_customer_id = current_user.id
        data = request.get_json()
        
        appointment_id = data.get('appointment_id')
        rating = data.get('rating')
        review_text = data.get('review')

        if not appointment_id or rating is None:
            return {"message": "Missing required fields: appointment_id, rating"}, 400

        appointment = Appointment.query.get(appointment_id)
        if not appointment or appointment.customer_id != target_customer_id:
            return {"message": "Appointment not found or unauthorized"}, 404

        if appointment.feedback_given:
            return {"message": "Feedback already provided for this appointment"}, 400

        try:
            # Find the MOST RECENT invoice for this customer and staff to link to the review
            # This is more robust than strict date matching
            invoice = Invoice.query.filter(
                Invoice.customer_id == target_customer_id,
                Invoice.staff_id == appointment.staff_id
            ).order_by(Invoice.invoice_date.desc()).first()

            invoice_num = invoice.invoice_number if invoice else None

            # Create CustomerReview
            new_review = CustomerReview(
                customer_id=target_customer_id,
                staff_id=appointment.staff_id,
                apppointment_id=appointment.appointment_id,
                invoice_number=invoice_num,
                service_ids=",".join([str(s.service_id) for s in appointment.services]),
                rating=rating,
                review=review_text
            )
            db.session.add(new_review)
            
            # Update Appointment feedback_given flag
            appointment.feedback_given = True
            
            # Update Staff and Service ratings
            update_staff_rating(appointment.staff_id, rating)
            for service in appointment.services:
                update_service_rating(service.service_id, rating)
            
            db.session.commit()
            return {"message": "Feedback submitted successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to submit feedback: {str(e)}"}, 500

################################## Helper functions for Reward calculations ############################################
################################## Update Staff Ratings ############################################
def update_staff_rating(staff_id, new_rating):
    """
    Update staff_cumulative_rating and no_of_reviews in Staff master table.
    Formula: ((current_rating * current_reviews) + new_rating) / (current_reviews + 1)
    """
    staff = Staff.query.get(staff_id)
    if staff:
        current_rating = staff.staff_cumulative_rating or 0.0
        current_reviews = staff.no_of_reviews or 0
        
        updated_rating = ((current_rating * current_reviews) + new_rating) / (current_reviews + 1)
        
        staff.staff_cumulative_rating = round(updated_rating, 2)
        staff.no_of_reviews = current_reviews + 1
        db.session.add(staff)

################################## Update Service Ratings ############################################
def update_service_rating(service_id, new_rating):
    """
    Update service_rating and no_of_reviews in Service master table.
    Formula: ((current_rating * current_reviews) + new_rating) / (current_reviews + 1)
    """
    service = Service.query.get(service_id)
    if service:
        current_rating = service.service_rating or 0.0
        current_reviews = service.no_of_reviews or 0
        
        updated_rating = ((current_rating * current_reviews) + new_rating) / (current_reviews + 1)
        
        service.service_rating = round(updated_rating, 2)
        service.no_of_reviews = current_reviews + 1
        db.session.add(service)

################################### Check and Update VIP Status ############################################
def check_vip_status(customer_id, valid_points_sum):
    """
    Update customer_type based on VIP_POINTS_FOR_REDUMPTION threshold.
    """
    customer = Customer.query.get(customer_id)
    if not customer:
        return
        
    vip_config = SalonConfig.query.filter_by(param_name='VIP_POINTS_FOR_REDUMPTION').first()
    if vip_config:
        threshold = int(vip_config.param_value)
        if valid_points_sum > threshold:
            customer.customer_type = 'VIP'
        else:
            customer.customer_type = 'Regular'
    
    db.session.commit()

################################### Invalidate Expired Points ############################################
def invalidate_expired_points(customer_id):
    """
    1. Update valid_flg for all entries of the customer based on expiry_date.
    2. Calculate and return the sum of credit_points for valid, non-utilized entries.
    """
    today = datetime.now()
    rewards = CustomerReward.query.filter_by(customer_id=customer_id, valid_flg=True, utilized_flg=False).all()
    for reward in rewards:
        if reward.expiry_date < today:
            reward.valid_flg = False
    
    db.session.commit()

    # Calculate total sum of remaining valid, non-utilized points
    valid_points_sum = db.session.query(db.func.sum(CustomerReward.credit_points))\
        .filter(
            CustomerReward.customer_id == customer_id, 
            CustomerReward.valid_flg == True, 
            CustomerReward.utilized_flg == False
        ).scalar() or 0
    
    # Update customer_available_rewards column in customer_master table
    customer = Customer.query.get(customer_id)
    if customer:
        customer.customer_available_rewards = int(valid_points_sum)
        
        # Check for VIP status
        check_vip_status(customer_id, valid_points_sum)
    
    return

###################################Update Customer Rewards based on Expiry and Calculate Available Rewards ##############################
def update_customer_rewards(customer_id, reward_points_utilized=0):
    """
    1. Update valid_flg for all entries of the customer based on expiry_date.
    2. Handle point utilization by marking entries as utilized (utilized_flg=True) 
       or decrementing credit_points in FIFO order (by expiry_date).
    3. Update customer_available_rewards with the sum of credit_points for valid, non-utilized entries.
    """
    # Step 1: Invalidate expired points
    invalidate_expired_points(customer_id)

    # Step 2: Handle Utilization (FIFO based on expiry_date)
    if reward_points_utilized > 0:
        valid_rewards = CustomerReward.query.filter_by(
            customer_id=customer_id, 
            valid_flg=True, 
            utilized_flg=False
        ).order_by(CustomerReward.expiry_date.asc()).all()

        remaining_to_utilize = reward_points_utilized
        for reward in valid_rewards:
            if remaining_to_utilize <= 0:
                break
            
            if remaining_to_utilize >= reward.credit_points:
                # Fully utilize this entry
                remaining_to_utilize -= reward.credit_points
                reward.utilized_flg = True
            else:
                # Partially utilize this entry
                reward.credit_points -= remaining_to_utilize
                remaining_to_utilize = 0
        
        db.session.commit()
    
    # Step 3: Calculate total sum of remaining valid, non-utilized points
    valid_points_sum = db.session.query(db.func.sum(CustomerReward.credit_points))\
        .filter(
            CustomerReward.customer_id == customer_id, 
            CustomerReward.valid_flg == True, 
            CustomerReward.utilized_flg == False
        ).scalar() or 0
    
    customer = Customer.query.get(customer_id)
    if customer:
        customer.customer_available_rewards = int(valid_points_sum)
        db.session.commit()
    
    return int(valid_points_sum)

#############################Calculate Reward Value for Invoice based on Available Points and Salon Configurations ##############################
def calculate_reward_value(invoice_amount, current_reward_points):
    """
    Calculate the reward value to be utilized based on available points and salon configuration.
    """
    # Get parameters from SalonConfig
    redemption_value_per_point = SalonConfig.query.filter_by(param_name='REDUMPTION_VALUE_PER_POINT').first()
    
    if not redemption_value_per_point:
        return 0.0, current_reward_points, invoice_amount
        
    threshold = 0
    value_per_point = float(redemption_value_per_point.param_value)
    
    reward_points_utilized = 0.0
    rem_reward_points = current_reward_points
    payable_invoice_amount = float(invoice_amount)
    
    if current_reward_points >= threshold:
        potential_reward_value = current_reward_points * value_per_point
        if potential_reward_value >= invoice_amount:
            # If reward value exceeds invoice amount, cap it at invoice_amount
            reward_utilized_value = float(invoice_amount)
            # Calculate points equivalent to the utilized value, round to nearest integer
            reward_points_utilized = round(reward_utilized_value / value_per_point)
            
            # Formula for remaining: ensure it doesn't dip below 0
            rem_reward_points = max(0, current_reward_points - reward_points_utilized)
            payable_invoice_amount = 0.0

        else:
            reward_points_utilized = float(current_reward_points)
            rem_reward_points = 0
            payable_invoice_amount = float(invoice_amount) - potential_reward_value
            
    return reward_points_utilized, rem_reward_points, payable_invoice_amount


###########################Calculate Earned Reward Points for Invoice based on Invoice Amount and Salon Configurations, and Create CustomerReward Entry with Expiry Date ##############################
def earned_reward_points(invoice_amount, customer_id):
    """
    Calculate earned reward points based on invoice amount and salon configuration.
    Also creates an entry in the CustomerReward table with an expiry date.
    """
    points_per_currency = SalonConfig.query.filter_by(param_name='POINTS_PER_CURRENCY').first()
    reward_expiry_days_cfg = SalonConfig.query.filter_by(param_name='REWARD_EXPIRY_DAYS').first()
    
    if not points_per_currency:
        return 0
        
    conversion_rate = float(points_per_currency.param_value)
    earned_points = int(float(invoice_amount) * conversion_rate)
    
    if earned_points > 0:
        expiry_days = int(reward_expiry_days_cfg.param_value) if reward_expiry_days_cfg else 30
        expiry_date = datetime.now() + timedelta(days=expiry_days)
        
        new_reward = CustomerReward(
            customer_id=customer_id,
            credit_points=earned_points,
            expiry_date=expiry_date,
            valid_flg=True
        )
        db.session.add(new_reward)
        
    return earned_points

################################Calculate Bonus Reward Points for Customer's First Visit based on Salon Configuration, and Create CustomerReward Entry with Expiry Date ##############################
def first_time_rewards(customer_id):
    """
    Calculate bonus reward points for a customer's first visit.
    Checks salon_config for 'FIRST_VISIT_BONUS_POINTS'.
    Also creates an entry in the CustomerReward table with an expiry date.
    """
    customer = Customer.query.get(customer_id)
    if not customer:
        return 0
        
    # Check if it's the customer's first visit (0 recorded visits)
    if customer.number_of_visits == 0:
        bonus_config = SalonConfig.query.filter_by(param_name='FIRST_VISIT_BONUS_POINTS').first()
        reward_expiry_days_cfg = SalonConfig.query.filter_by(param_name='REWARD_EXPIRY_DAYS').first()
        
        if bonus_config:
            bonus_points = int(bonus_config.param_value)
            if bonus_points > 0:
                expiry_days = int(reward_expiry_days_cfg.param_value) if reward_expiry_days_cfg else 30
                expiry_date = datetime.now() + timedelta(days=expiry_days)
                
                new_reward = CustomerReward(
                    customer_id=customer_id,
                    credit_points=bonus_points,
                    expiry_date=expiry_date,
                    valid_flg=True
                )
                db.session.add(new_reward)
            return bonus_points
            
    return 0

########################### Birthday Bonus Rewards ############################################
def birthday_bonus_rewards(customer_id):
    """
    Calculate and allot birthday bonus points for a customer.
    Checks salon_config for 'BIRTHDAY_BONUS_POINTS'.
    Also creates an entry in the CustomerReward table with an expiry date.
    """
    customer = Customer.query.get(customer_id)
    if not customer:
        return 0
    
    # Check if a birthday reward already exists for this year's birthday
    # We look for a reward whose (expiry_date - expiry_days) is within the 15-day window before this year's birthday
    
    # Calculate this year's birthday
    now = datetime.now()
    try:
        this_year_birthday = datetime(now.year, customer.customer_dob.month, customer.customer_dob.day)
    except ValueError: # Handle Feb 29 for non-leap years
        this_year_birthday = datetime(now.year, 3, 1)
    
    # Target date is 15 days before birthday
    reward_trigger_date = this_year_birthday - timedelta(days=15)
    
    # If today is within the [trigger_date, birthday] window
    if reward_trigger_date.date() <= now.date() <= this_year_birthday.date():
        # Check if already awarded for this year's cycle
        # Since we don't have a 'created_at', we check if any reward exists 
        # where (expiry_date - expiry_days) falls in this year's window
        
        bonus_config = SalonConfig.query.filter_by(param_name='BIRTHDAY_BONUS_POINTS').first()
        reward_expiry_days_cfg = SalonConfig.query.filter_by(param_name='REWARD_EXPIRY_DAYS').first()
        expiry_days = int(reward_expiry_days_cfg.param_value) if reward_expiry_days_cfg else 30
        
        # Look for rewards created between trigger_date and today for this customer
        # This is roughly: trigger_date <= (expiry_date - expiry_days) <= today
        already_awarded = CustomerReward.query.filter(
            CustomerReward.customer_id == customer_id,
            db.func.date(CustomerReward.expiry_date) >= (reward_trigger_date + timedelta(days=expiry_days)).date(),
            db.func.date(CustomerReward.expiry_date) <= (this_year_birthday + timedelta(days=expiry_days)).date(),
            CustomerReward.credit_points == int(bonus_config.param_value) if bonus_config else 0
        ).first()

        if already_awarded:
            return 0
        
        if bonus_config:
            bonus_points = int(bonus_config.param_value)
            if bonus_points > 0:
                expiry_days = int(reward_expiry_days_cfg.param_value) if reward_expiry_days_cfg else 30
                expiry_date = datetime.now() + timedelta(days=expiry_days)
                
                new_reward = CustomerReward(
                    customer_id=customer_id,
                    credit_points=bonus_points,
                    expiry_date=expiry_date,
                    valid_flg=True
                )
                db.session.add(new_reward)
                
                # Update available rewards on customer object
                customer.customer_available_rewards += bonus_points
                
                # Check and update VIP status after birthday points are added
                check_vip_status(customer_id, customer.customer_available_rewards)
                
                db.session.commit()

                return bonus_points
                
    return 0

################################## Finance API ############################################
finance_fields = {
    'reporting_month': fields.DateTime,
    'product_cost': fields.Float,
    'total_revenue': fields.Float,
    'staff_salary': fields.Float,
    'overheads': fields.Float,
    'other': fields.Float,
    'net_profit': fields.Float
}

###############################Create entry for a month with calculated product_cost, total_revenue, staff_salary, and net_profit. Manager can update overheads and other expenses later. ##############################
class FinanceResource(Resource):
    @auth_required("token")
    @roles_required("manager")
    def post(self):
        """
        Create composite financial report for a specific month.
        Expects 'last_date' of the month (YYYY-MM-DD).
        """
        data = request.get_json()
        last_date_str = data.get('last_date')
        if not last_date_str:
            return {"message": "last_date is required (YYYY-MM-DD)"}, 400
        
        try:
            last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
            # Month start is the first day of that month
            month_start = last_date.replace(day=1)
            # Create a datetime object for comparison (model uses DateTime for reporting_month)
            reporting_month = datetime.combine(month_start, datetime.min.time())
            
            # 1. Sum up order_cost for all processed orders specifically in that month
            # Filtered by order_replenishment_date
            product_cost = db.session.query(db.func.sum(Order.order_cost)).filter(
                Order.status == 1, # Processed orders
                Order.order_replenishment_date >= datetime.combine(month_start, datetime.min.time()),
                Order.order_replenishment_date <= datetime.combine(last_date, datetime.max.time())
            ).scalar() or 0.0
            
            total_revenue = db.session.query(db.func.sum(Invoice.total_invoice_amount)).filter(
                Invoice.invoice_date >= month_start,
                Invoice.invoice_date <= last_date
            ).scalar() or 0.0
            
            # Sum up staff salaries
            staff_salary_sum = db.session.query(db.func.sum(Staff.staff_salary)).scalar() or 0.0
            
            # Check if record exists
            finance = Finance.query.get(reporting_month)
            if not finance:
                finance = Finance(reporting_month=reporting_month)
            
            finance.product_cost = float(product_cost)
            finance.total_revenue = float(total_revenue)
            finance.staff_salary = float(staff_salary_sum)
            # Defaults for new records
            if finance.overheads is None: finance.overheads = 0.0
            if finance.other is None: finance.other = 0.0
            
            # Calculate net profit
            raw_profit = finance.total_revenue - (finance.product_cost + finance.staff_salary + finance.overheads + finance.other)
            finance.net_profit = max(0, raw_profit)
            
            db.session.add(finance)
            db.session.commit()
            
            return marshal(finance, finance_fields), 201
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error generating finance report: {str(e)}"}, 500

################################## Edit overheads and other expenses for a month, and recalculate net profit ##############################
    @auth_required("token")
    @roles_required("manager")
    def put(self):
        """
        Update overheads and other expenses for a month.
        Expects 'last_date' or 'reporting_month' to identify the row.
        """
        data = request.get_json()
        date_str = data.get('last_date') # identify by month
        if not date_str:
            return {"message": "last_date is required to identify the month"}, 400
            
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date().replace(day=1)
            reporting_month = datetime.combine(target_date, datetime.min.time())
            
            finance = Finance.query.get(reporting_month)
            if not finance:
                return {"message": "Finance record for this month not yet generated. Use POST first."}, 404
            
            if 'overheads' in data:
                finance.overheads = float(data['overheads'])
            if 'other' in data:
                finance.other = float(data['other'])
                
            # Recalculate net profit
            raw_profit = finance.total_revenue - (finance.product_cost + finance.staff_salary + finance.overheads + finance.other)
            finance.net_profit = max(0, raw_profit)
            
            db.session.commit()
            return marshal(finance, finance_fields), 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating finance: {str(e)}"}, 500

############################# Fetch all finance records, ordered by reporting_month descending (latest first) ##############################
    @auth_required("token")
    @roles_required("manager")
    def get(self):
        """Fetch all finance records or a specific month's record"""
        last_date_str = request.args.get('last_date')
        if last_date_str:
            try:
                target_date = datetime.strptime(last_date_str, '%Y-%m-%d').date().replace(day=1)
                reporting_month = datetime.combine(target_date, datetime.min.time())
                finance = Finance.query.get(reporting_month)
                if not finance:
                    return {"message": "Finance record for this month not found"}, 404
                return marshal(finance, finance_fields), 200
            except Exception as e:
                return {"message": f"Invalid date format: {str(e)}"}, 400

        finances = Finance.query.order_by(Finance.reporting_month.desc()).all()
        return marshal(finances, finance_fields), 200

################################## Invoice API ############################################
invoice_fields = {
    'invoice_number': fields.Integer,
    'invoice_date': fields.String,
    'customer_id': fields.Integer,
    'customer_name': fields.String(attribute='customer.customer_name'),
    'staff_id': fields.Integer,
    'staff_name': fields.String(attribute='staff.staff_name'),
    'service_ids': fields.String,
    'service_descs': fields.String,
    'other_charges': fields.Float,
    'discount_percentage': fields.Float,
    'rewards_earned': fields.Integer,
    'rewards_utilized': fields.Integer,
    'current_reward_points': fields.Integer,
    'invoice_amount': fields.Float,
    'total_charges': fields.Float(attribute='total_invoice_amount'),
    'status': fields.Integer
}

class InvoiceResource(Resource):
################################## Get Invoice Data ###################################
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def get(self, appointment_id=None):
        # If appointment_id is provided, check its status immediately
        if appointment_id:
            appointment = Appointment.query.get(appointment_id)
            if not appointment:
                return {"message": "Appointment not found"}, 404
            invalidate_expired_points(appointment.customer_id)
        """
        Fetch data for an invoice based on appointment_id.
        If no appointment_id is provided, return all appointments that haven't been invoiced yet.
        """
        # Determine customer_id to update rewards if appointment_id is provided
        if appointment_id:
            appointment = Appointment.query.get(appointment_id)
            if appointment:
                invalidate_expired_points(appointment.customer_id)
            else:
                return {"message": "Appointment not found"}, 404
        
        if appointment_id:
            # Re-fetch or continue with appointment object
            appointment = Appointment.query.get(appointment_id)
            
            # Check if an invoice already exists for this appointment
            existing_invoice = Invoice.query.filter_by(appointment_id=appointment_id).first()

            if existing_invoice:
                # Resolve service descriptions for the existing invoice
                res = marshal(existing_invoice, invoice_fields)
                if existing_invoice.service_ids:
                    try:
                        clean_sids = str(existing_invoice.service_ids).strip()
                        s_ids = [int(sid.strip()) for sid in clean_sids.split(",") if sid.strip()]
                        services = Service.query.filter(Service.service_id.in_(s_ids)).all()
                        s_map = {s.service_id: s.service_desc for s in services}
                        res["service_descs"] = ", ".join([s_map.get(sid, "Unknown") for sid in s_ids])
                    except Exception:
                        res["service_descs"] = ""
                else:
                    res["service_descs"] = ""
                return res, 200

            # For manager/staff, return the data required to *create* an invoice
            service_total = sum(s.service_price for s in appointment.services if s.active_flg)
            
            return {
                "customer_id": appointment.customer_id,
                "customer_name": appointment.customer.customer_name,
                "current_available_rewards": appointment.customer.customer_available_rewards,
                "staff_id": appointment.staff_id,
                "staff_name": appointment.staff.staff_name if appointment.staff else "Not Assigned",
                "service_ids": ",".join([str(s.service_id) for s in appointment.services if s.active_flg]),
                "service_descs": ",".join([s.service_desc for s in appointment.services if s.active_flg]),
                "appointment_date": str(appointment.appointment_datetime.date()),
                "services": [{"id": s.service_id, "name": s.service_desc, "price": s.service_price} 
                             for s in appointment.services if s.active_flg],
                "service_total": service_total
            }, 200
        
        # Change: Filter out appointments that already have an invoice
        invoiced_appointment_ids = db.session.query(Invoice.appointment_id).filter(Invoice.appointment_id != None).all()
        invoiced_appointment_ids = [r[0] for r in invoiced_appointment_ids]
        
        # Get all appointments that do NOT have an invoice and have status 0 or 4
        pending_appointments = Appointment.query.filter(
            ~Appointment.appointment_id.in_(invoiced_appointment_ids),
            Appointment.status.in_([0, 4])
        ).all()
        
        result = []
        for appt in pending_appointments:
            result.append({
                "appointment_id": appt.appointment_id,
                "customer_name": appt.customer.customer_name if appt.customer else "Unknown",
                "staff_name": appt.staff.staff_name if appt.staff else "Not Assigned",
                "datetime": appt.appointment_datetime.isoformat(),
                "status": appt.status
            })
            
        return result, 200


################################## Create Invoice #####################################
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def post(self, appointment_id=None):
        """
        Create a new invoice record.
        """
        data = request.get_json()
        
        customer_id = data.get('customer_id')
        staff_id = data.get('staff_id')
        service_ids = data.get('service_ids')
        invoice_amount = data.get('invoice_amount')
        other_charges = data.get('other_charges', 0.0)
        discount_percentage_input = data.get('discount_percentage', 0.0)
        # Always set status to 1 (Completed) when creating a new invoice
        status = 1
        
        # If appointment_id is provided in URL, use it; otherwise check body
        target_appointment_id = appointment_id or data.get('appointment_id')
        
        if not (customer_id and staff_id and service_ids and invoice_amount):
            return {"message": "Missing required fields: customer_id, staff_id, service_ids, invoice_amount"}, 400
            
        customer = Customer.query.get(customer_id)
        if not customer:
            return {"message": "Customer not found"}, 404
        
        # Step 1: Update valid_flg and refresh customer available rewards based on expiration before calculating utilization
        invalidate_expired_points(customer_id)
        # Refresh current points after cleanup
        current_reward_points = customer.customer_available_rewards

        # Initialize base amount and total discount variables
        base_invoice_amount = float(invoice_amount)
        total_discount_amount = 0.0

        # Calculate VIP discount if applicable
        if customer.customer_type == "VIP":
            vip_discount_cfg = SalonConfig.query.filter_by(param_name='VIP_DISCOUNT_PERCENTAGE').first()
            if vip_discount_cfg:
                vip_discount_percentage = float(vip_discount_cfg.param_value)
                total_discount_amount += base_invoice_amount * (vip_discount_percentage / 100)
        
        # Calculate subtotal after VIP/Base charges
        current_total = base_invoice_amount + float(other_charges) - total_discount_amount
        
        # Apply additional manual discount if provided (on top of current subtotal)
        if discount_percentage_input > 0:
            manual_discount = current_total * (float(discount_percentage_input) / 100)
            total_discount_amount += manual_discount
            current_total -= manual_discount

        total_invoice_amount = current_total
        
        # Calculate rewards utilization (Using the final total_invoice_amount after all discounts)
        rewards_utilized_points, rem_reward_points, payable_invoice_amount = calculate_reward_value(total_invoice_amount, current_reward_points)
        

        # Now permanently utilize the points in the CustomerReward table (FIFO)
        if rewards_utilized_points > 0:
            update_customer_rewards(customer_id, reward_points_utilized=int(rewards_utilized_points))
            # Refresh rem_reward_points after actual database utilization
            rem_reward_points = customer.customer_available_rewards

        # Step 2: Calculate rewards earned from transaction (this adds to CustomerReward)
        reward_points_earned = earned_reward_points(payable_invoice_amount, customer_id)
        
        # Step 3: Calculate first time bonus if applicable (this also adds to CustomerReward)
        bonus_points = first_time_rewards(customer_id)
        total_rewards_earned = reward_points_earned + bonus_points
        
        try:
            # Increment customer visits
            customer.number_of_visits += 1
            
            # Handle potential list or single string for service_ids
            formatted_service_ids = service_ids
            if isinstance(service_ids, list):
                formatted_service_ids = ",".join(map(str, service_ids))
            
            # Final point calculation for sync
            # Note: total_rewards_earned are already added to CustomerReward table via helper functions
            # But the 'customer' object hasn't been refreshed to include these new earnings yet
            # because the session hasn't been committed, or we need to update the balance manually.
            invoice_current_reward_points = int(customer.customer_available_rewards) + total_rewards_earned
            check_vip_status(customer_id, invoice_current_reward_points)  #check and update change in VIP status
            new_invoice = Invoice(
                customer_id=customer_id,
                staff_id=staff_id,
                appointment_id=target_appointment_id,
                service_ids=str(formatted_service_ids),
                invoice_date=date.today(),
                invoice_amount=invoice_amount,
                other_charges=other_charges,
                discount_percentage=discount_percentage_input,
                rewards_earned=total_rewards_earned,
                rewards_utilized=int(rewards_utilized_points),
                current_reward_points=current_reward_points,
                total_invoice_amount=total_invoice_amount,
                payable_invoice_amount=payable_invoice_amount,
                status=status
            )
            db.session.add(new_invoice)
            
            # Sync Customer available rewards to match the Invoice's calculated current_reward_points
            customer.customer_available_rewards = invoice_current_reward_points

            # Update customer total spend
            customer.total_spend += total_invoice_amount
            
            # Update appointment status if target_appointment_id is provided
            if target_appointment_id:
                appointment = Appointment.query.get(target_appointment_id)
                if appointment:
                    appointment.status = 5 # Mark as Invoiced
            
            db.session.commit()
            
            return {"message": "Invoice created successfully", "invoice_number": new_invoice.invoice_number}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to create invoice: {str(e)}"}, 500


################################## Today's Appointments API ################################

class TodaysAppointmentsResource(Resource):
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def get(self):
        """
        Fetch details of all appointments scheduled for today.
        """
        today = date.today()
        try:
            # Fetch appointments where the date matches today
            appointments = Appointment.query.filter(
                db.func.date(Appointment.appointment_datetime) == today
            ).order_by(Appointment.appointment_datetime.asc()).all()

            if not appointments:
                return {"message": f"No appointments found for today ({today})"}, 200

            result = []
            for appt in appointments:
                result.append({
                    "appointment_id": appt.appointment_id,
                    "customer_id": appt.customer_id,
                    "customer_name": appt.customer.customer_name,
                    "staff_id": appt.staff_id,
                    "staff_name": appt.staff.staff_name if appt.staff else "Not Assigned",
                    "datetime": appt.appointment_datetime.isoformat(),
                    "status": "Assigned" if appt.staff_id else "Unassigned",
                    "services": [{"id": s.service_id, "name": s.service_desc, "price": s.service_price} 
                                 for s in appt.services]
                })
            return result, 200
        except Exception as e:
            return {"message": f"Error fetching today's appointments: {str(e)}"}, 500


class GetAppointmentIDsForInvoice(Resource):
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def get(self):
        """
        Fetch all appointments from appointment table where status is either 0 or 4.
        """
        appointments = Appointment.query.filter(Appointment.status.in_([0, 4])).all()
        
        result = []
        for appt in appointments:
            result.append({
                "appointment_id": appt.appointment_id,
                "customer_name": appt.customer.customer_name if appt.customer else "Unknown",
                "staff_name": appt.staff.staff_name if appt.staff else "Not Assigned",
                "datetime": appt.appointment_datetime.isoformat(),
                "status": appt.status
            })
            
        return result, 200

############################################## To get all the invoices from invoice table for manager and staff ##############################################
class GetAllInvoices(Resource):
    @auth_required("token")
    @roles_accepted("manager", "staff")
    def get(self):
        """
        Fetch all the invoices from invoice table.
        """
        invoices = Invoice.query.all()
        
        result = []
        for inv in invoices:
            # Resolve service names based on service_ids (comma-separated string)
            service_names = ""
            if inv.service_ids:
                try:
                    # Convert comma-separated string to list of integers
                    id_list = [int(sid.strip()) for sid in inv.service_ids.split(",") if sid.strip()]
                    # Query service descriptions
                    services = Service.query.filter(Service.service_id.in_(id_list)).all()
                    service_names = ", ".join([s.service_desc for s in services])
                except Exception:
                    service_names = "Unknown Service"

            result.append({
                "invoice_number": inv.invoice_number,
                "invoice_date": str(inv.invoice_date),
                "customer_id": inv.customer_id,
                "customer_name": inv.customer.customer_name if inv.customer else "Unknown",
                "staff_id": inv.staff_id,
                "staff_name": inv.staff.staff_name if inv.staff else "Unknown",
                "service_ids": inv.service_ids,
                "service_names": service_names,
                "other_charges": inv.other_charges,
                "discount_percentage": inv.discount_percentage,
                "rewards_earned": inv.rewards_earned,
                "rewards_utilized": inv.rewards_utilized,
                "current_reward_points": inv.current_reward_points,
                "invoice_amount": inv.invoice_amount,
                "total_charges": inv.total_invoice_amount,
                "status": inv.status,
                "appointment_id": inv.appointment_id
            })
            
        return result, 200

############################################## Generate PDF Invoice for Customer ##############################################
class GenerateCustomerInvoice(Resource):
    def get(self, invoice_number):
        """
        Generate a PDF file for a specific invoice number.
        """
        invoice = Invoice.query.get(invoice_number)
        if not invoice:
            return {"message": "Invoice not found"}, 404

        # If logged in as customer, ensure they only access their own invoice
        if any(role.name == 'customer' for role in current_user.roles):
            if invoice.customer_id != current_user.id:
                return {"message": "Access denied"}, 403

        try:
            # Resolve service names
            service_names = []
            if invoice.service_ids:
                id_list = [int(sid.strip()) for sid in invoice.service_ids.split(",") if sid.strip()]
                services = Service.query.filter(Service.service_id.in_(id_list)).all()
                service_names = [s.service_desc for s in services]

            # Generate PDF using FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=12)

            # Title
            pdf.set_font("Helvetica", style="B", size=16)
            pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')
            pdf.ln(10)

            # Invoice Details
            pdf.set_font("Helvetica", size=12)
            pdf.cell(100, 10, txt=f"Invoice Number: {invoice.invoice_number}")
            pdf.cell(100, 10, txt=f"Date: {invoice.invoice_date}", ln=True, align='R')
            pdf.ln(5)

            # Customer Details
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(200, 10, txt="Customer Information:", ln=True)
            pdf.set_font("Helvetica", size=12)
            pdf.cell(200, 10, txt=f"Name: {invoice.customer.customer_name if invoice.customer else 'Unknown'}", ln=True)
            pdf.cell(200, 10, txt=f"Email: {invoice.customer.customer_email if invoice.customer else 'N/A'}", ln=True)
            pdf.ln(5)

            # Staff Details
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(200, 10, txt="Served By:", ln=True)
            pdf.set_font("Helvetica", size=12)
            pdf.cell(200, 10, txt=f"{invoice.staff.staff_name if invoice.staff else 'Unknown'}", ln=True)
            pdf.ln(10)

            # Services Table Header
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(140, 10, txt="Service Description", border=1)
            pdf.cell(50, 10, txt="Price", border=1, ln=True, align='R')

            # Services Table Rows
            pdf.set_font("Helvetica", size=12)
            if invoice.service_ids:
                id_list = [int(sid.strip()) for sid in invoice.service_ids.split(",") if sid.strip()]
                services = Service.query.filter(Service.service_id.in_(id_list)).all()
                for s in services:
                    pdf.cell(140, 10, txt=s.service_desc, border=1)
                    pdf.cell(50, 10, txt=f"{s.service_price:.2f}", border=1, ln=True, align='R')

            pdf.ln(5)

            # Totals
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(140, 10, txt="Subtotal:", align='R')
            pdf.cell(50, 10, txt=f"{invoice.invoice_amount:.2f}", ln=True, align='R')
            
            pdf.cell(140, 10, txt="Other Charges:", align='R')
            pdf.cell(50, 10, txt=f"{invoice.other_charges or 0.0:.2f}", ln=True, align='R')
            
            pdf.cell(140, 10, txt="Discount Percentage:", align='R')
            pdf.cell(50, 10, txt=f"{invoice.discount_percentage or 0.0:.2f}%", ln=True, align='R')
            
            pdf.cell(140, 10, txt="Rewards Utilized:", align='R')
            pdf.cell(50, 10, txt=f"-{invoice.rewards_utilized or 0:.2f}", ln=True, align='R')

            pdf.set_font("Helvetica", style="B", size=14)
            pdf.cell(140, 10, txt="Total Payable Amount:", align='R')
            pdf.cell(50, 10, txt=f"{invoice.payable_invoice_amount:.2f}", ln=True, align='R')

            pdf.ln(10)
            pdf.set_font("Helvetica", style="I", size=10)
            pdf.cell(200, 10, txt="Thank you for choosing our salon!", ln=True, align='C')

            # Define directory and ensure it exists under backend
            # Note: os.getcwd() might be the root or backend depending on how it's run
            # We want it specifically in backend/customer_invoices
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            invoice_dir = os.path.join(base_dir, 'customer_invoices')
            if not os.path.exists(invoice_dir):
                os.makedirs(invoice_dir, exist_ok=True)
            
            filename = f"invoice_{invoice.invoice_number}.pdf"
            filepath = os.path.join(invoice_dir, filename)
            
            # Save to file (overwrites if already exists)
            pdf.output(filepath)
            
            # Update invoice_path in database (include filename)
            invoice.invoice_path = filepath
            db.session.commit()
            
            # --- Automatically Send Email ---
            try:
                msg = Message(
                    subject=f"Invoice for your recent Salon Visit - #{invoice.invoice_number}",
                    recipients=[invoice.customer.customer_email],
                    body=f"Dear {invoice.customer.customer_name},\n\nPlease find attached the invoice for your recent visit.\n\nThank you for choosing our salon!"
                )
                with open(filepath, "rb") as fp:
                    msg.attach(filename, "application/pdf", fp.read())
                
                current_app.mail.send(msg)
                
                # Update status to 2 (Sent) after successful email
                invoice.status = 2
                db.session.commit()
            except Exception as mail_err:
                print(f"Automatic email failed: {str(mail_err)}")

            # Return PDF as a download from the saved path
            return send_file(
                filepath,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )

        except Exception as e:
            return {"message": f"Failed to generate invoice PDF: {str(e)}"}, 500

############################################## Generate Wholesaler Order PDF ##############################################
class GenerateWholesalerOrder(Resource):
    @auth_required("token", "session")
    @roles_required("manager")
    def get(self, supplier_email):
        """
        Generate a PDF for all pending orders (status=0) matching a specific supplier email.
        """
        # Fetch pending orders for this supplier email
        orders = Order.query.filter_by(supplier_email=supplier_email, status=0).all()
        if not orders:
            return {"message": f"No pending orders found for {supplier_email}"}, 404

        try:
            # Prepare PDF metadata
            date_str = datetime.now().strftime("%Y%m%d")
            # Extract part before @, replace dots with underscores, and append date
            email_part = supplier_email.split('@')[0].replace('.', '_')
            filename = f"{email_part}_{date_str}.pdf"
            
            # Define directory and ensure it exists under backend
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            order_dir = os.path.join(base_dir, 'wholesaler_orders')
            if not os.path.exists(order_dir):
                os.makedirs(order_dir, exist_ok=True)
            
            filepath = os.path.join(order_dir, filename)

            # Generate PDF using FPDF
            pdf = FPDF()
            pdf.add_page()
            
            # Wholesaler Name from first record
            wholesaler_name = orders[0].supplier_name
            
            pdf.set_font("Helvetica", style="B", size=16)
            pdf.cell(200, 10, txt=f"PURCHASE ORDER: {wholesaler_name}", ln=True, align='C')
            pdf.set_font("Helvetica", size=10)
            pdf.cell(200, 10, txt=f"Supplier Email: {supplier_email}", ln=True, align='C')
            pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
            pdf.ln(10)

            # Table Header
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(30, 10, txt="Order ID", border=1)
            pdf.cell(110, 10, txt="Product Description", border=1)
            pdf.cell(25, 10, txt="Qty", border=1, align='C')
            pdf.cell(25, 10, txt="Cost", border=1, ln=True, align='R')

            # Table Rows
            pdf.set_font("Helvetica", size=11)
            total_order_cost = 0.0

            for o in orders:
                desc = o.product.product_desc if o.product else "Unknown Product"
                pdf.cell(30, 10, txt=str(o.order_id), border=1)
                pdf.cell(110, 10, txt=desc, border=1)
                pdf.cell(25, 10, txt=str(o.order_quantity), border=1, align='C')
                pdf.cell(25, 10, txt=f"{o.order_cost:.2f}", border=1, ln=True, align='R')
                total_order_cost += o.order_cost
                
                # Assign the path to EACH order record and update status
                o.order_path = filepath
                o.status = 1 # Mark as Processed

            pdf.ln(5)
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(165, 10, txt="Total Estimated Cost:", align='R')
            pdf.cell(25, 10, txt=f"{total_order_cost:.2f}", border=1, ln=True, align='R')

            # Save PDF (overwrites if exists)
            pdf.output(filepath)
            
            # Commit status and path updates to DB
            db.session.commit()

            # --- Automatically Send Email to Manager and Wholesaler ---
            email_recipients = []
            
            # 1. Add Manager email
            if current_user.has_role("manager"):
                manager_profile = Manager.query.filter_by(manager_id=current_user.id).first()
                if manager_profile and manager_profile.manager_email:
                    email_recipients.append(manager_profile.manager_email)
            
            # 2. Add Wholesaler email
            if supplier_email not in email_recipients:
                email_recipients.append(supplier_email)
            
            if email_recipients:
                try:
                    msg = Message(
                        subject=f"Purchase Order Generated - {wholesaler_name}",
                        recipients=email_recipients,
                        body=f"Hello,\n\nPlease find attached the purchase order for {wholesaler_name} ({supplier_email}) generated on {date_str}.\n\nTotal Orders Processed: {len(orders)}"
                    )
                    with open(filepath, "rb") as fp:
                        msg.attach(filename, "application/pdf", fp.read())
                    
                    current_app.mail.send(msg)
                except Exception as mail_err:
                    print(f"PO email dispatch failed: {str(mail_err)}")
            else:
                print("No email recipients found, skipping PO email dispatch.")

            # Return PDF as download
            return send_file(
                filepath,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename
            )

        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to generate wholesaler order: {str(e)}"}, 500

############################################## Send Email API ##############################################
class SendEmail(Resource):
    @auth_required("token")
    @roles_accepted("manager")
    def post(self):
        """
        Send an email with an attachment.
        Expects JSON: { "document_path": "...", "subject": "...", "email_id": "..." }
        """
        data = request.get_json()
        document_path = data.get('document_path')
        subject = data.get('subject')
        email_id = data.get('email_id')

        if not all([document_path, subject, email_id]):
            return {"message": "Missing required fields: document_path, subject, email_id"}, 400

        if not os.path.exists(document_path):
            return {"message": f"File not found: {document_path}"}, 404

        try:
            msg = Message(
                subject=subject,
                recipients=[email_id],
                body=f"Please find the attached document: {os.path.basename(document_path)}"
            )

            with open(document_path, "rb") as fp:
                msg.attach(
                    os.path.basename(document_path),
                    "application/pdf",
                    fp.read()
                )

            current_app.mail.send(msg)

            # --- Update Invoice Status if applicable ---
            if "customer_invoices" in document_path:
                # Extract invoice number from path (e.g., invoice_123.pdf)
                filename = os.path.basename(document_path)
                try:
                    # filename format is "invoice_<number>.pdf"
                    invoice_number_str = filename.replace("invoice_", "").replace(".pdf", "")
                    if invoice_number_str.isdigit():
                        invoice_number = int(invoice_number_str)
                        invoice = Invoice.query.get(invoice_number)
                        if invoice:
                            invoice.status = 2
                            db.session.commit()
                except Exception as status_err:
                    print(f"Failed to update invoice status in SendEmail: {str(status_err)}")

            return {"message": "Email sent successfully"}, 200

        except Exception as e:
            return {"message": f"Failed to send email: {str(e)}"}, 500


############################################## Send Notification API ##############################################
class SendNotification(Resource):
    @auth_required("token")
    @roles_accepted("manager", "staff", "customer")
    def post(self):
        """
        Send a notification (App Notification) which includes storing it in the database.
        Expects JSON: { "subject": "...", "body": "...", "phone_number": "..." }
        """
        data = request.get_json()
        subject = data.get('subject')
        message = data.get('body')
        phone_number = data.get('phone_number')

        if not all([subject, message, phone_number]):
            return {"message": "Missing required fields: subject, body, phone_number"}, 400

        try:
            # Create a new Notification record assigned to the current user
            new_notification = Notification(
                user_id=current_user.id,
                subject=subject,
                message=message,
                phone_number=phone_number,
                is_read=False
            )
            db.session.add(new_notification)
            db.session.commit()

            return {"message": "Notification generated and saved successfully", "id": new_notification.id}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to send notification: {str(e)}"}, 500

    @auth_required("token")
    def get(self):
        """
        Fetch notifications for the current user. 
        By default, only returns Unread notifications. 
        Pass ?include_read=true to see all.
        """
        include_read = request.args.get('include_read', 'false').lower() == 'true'
        
        query = Notification.query.filter_by(user_id=current_user.id)
        if not include_read:
            query = query.filter_by(is_read=False)
            
        notifications = query.order_by(Notification.created_at.desc()).all()
        
        result = []
        for n in notifications:
            result.append({
                "id": n.id,
                "subject": n.subject,
                "message": n.message,
                "phone_number": n.phone_number,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat()
            })
        return result, 200

    @auth_required("token")
    def put(self, notification_id=None):
        """
        Mark a notification as read.
        Expects notification_id in the URL or 'id' in the JSON body.
        """
        target_id = notification_id or request.get_json().get('id')
        if not target_id:
            return {"message": "Notification ID is required"}, 400

        notification = Notification.query.filter_by(id=target_id, user_id=current_user.id).first()
        if not notification:
            return {"message": "Notification not found or access denied"}, 404

        try:
            notification.is_read = True
            db.session.commit()
            return {"message": f"Notification {target_id} marked as read"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": f"Failed to update notification: {str(e)}"}, 500

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
api.add_resource(StaffDashboard, '/staff-dashboard')
api.add_resource(StaffCustomerReview, '/staff-customer-reviews')
api.add_resource(ManagerStaffAttendance, '/manager-staff-attendance')
api.add_resource(MarkStaffAbsent, '/mark-staff-absent')
api.add_resource(SupplierOrderReportResource, '/supplier-order-reports')
api.add_resource(CSVToPDFResource, '/csv-to-pdf')
api.add_resource(StaffAttendanceResource, '/staff-attendance')
api.add_resource(CurrentStaffResource, '/staff-info')
api.add_resource(CurrentCustomerResource, '/customer-info')
api.add_resource(AppointmentHistoryCleanup, '/cleanup-appointments')
api.add_resource(SalonDailyAppointmentCountResource, '/daily-appointment-count')
api.add_resource(CustomerUpcomingAppointmentsResource, '/customer-upcoming-appointments')
api.add_resource(CustomerHistoryAppointmentsResource, '/customer-history-appointments')
api.add_resource(CustomerSummaryResource, '/customer-summary')
api.add_resource(CustomerAppointment, '/customer/appointment/<int:appointment_id>')
api.add_resource(CustomerReviewResource, '/customer-review', '/customer-review/<int:invoice_number>')
api.add_resource(CustomerReviewedAppointments, '/customer-reviewed-appointments')
api.add_resource(InventoryTransactionResource, '/inventory-transaction', '/inventory-transaction/<int:txn_id>')
api.add_resource(OrderResource, '/order', '/order/<int:order_id>')
api.add_resource(InvoiceResource, '/invoice', '/invoice/<int:appointment_id>')
api.add_resource(FinanceResource, '/finance')
api.add_resource(TodaysAppointmentsResource, '/todays-appointments')
api.add_resource(GetAppointmentIDsForInvoice, "/get-appointments-for-invoice")
api.add_resource(GetAllInvoices, "/get-all-invoices")
api.add_resource(GenerateCustomerInvoice, '/generate-invoice-pdf/<int:invoice_number>')
api.add_resource(GenerateWholesalerOrder, '/generate-wholesaler-order/<string:supplier_email>')
api.add_resource(SendEmail, '/send-email')
api.add_resource(SendNotification, '/send-notification', '/send-notification/<int:notification_id>')
