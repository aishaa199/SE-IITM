import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    _tablename_ = 'user'
   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    active = db.Column(db.Boolean, default=True)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))
    
    # Relationships
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    _tablename_ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class UserRoles(db.Model):
    _tablename_ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Service(db.Model):
    __tablename__ = 'service_master'
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_desc = db.Column(db.String(50), nullable=False)
    service_category = db.Column(db.String(50), nullable=False)
    service_price = db.Column(db.Float, nullable=False)
    service_duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    service_products = db.Column(db.String(255), nullable=True)  # Comma-separated list of products used
    service_rating = db.Column(db.Float, default=0.0)  # Average rating for the service
    no_of_reviews = db.Column(db.Integer, default=0)  # Number of reviews for the service

class Staff(db.Model):
    __tablename__ = 'staff_master'
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    staff_name = db.Column(db.String(100), nullable=False)
    staff_contact = db.Column(db.String(20), nullable=False)
    staff_skills = db.Column(db.String(255), nullable=False)
    staff_role = db.Column(db.String(50), nullable=False)
    staff_dob = db.Column(db.DateTime, nullable=False)
    staff_doj = db.Column(db.DateTime, nullable=False)
    staff_cumulative_rating = db.Column(db.Float, default=0.0)
    no_of_reviews = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref=db.backref('staff_profile', uselist=False))


class Customer(db.Model):
    __tablename__ = 'customer_master'
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_contact = db.Column(db.String(20), nullable=False)
    customer_dob = db.Column(db.DateTime, nullable=False)
    customer_reg_date = db.Column(db.DateTime, nullable=False)
    customer_email = db.Column(db.String(120), nullable=True)
    customer_address = db.Column(db.String(255), nullable=True)
    number_of_visits = db.Column(db.Integer, nullable=False, default=0)
    customer_type = db.Column(db.String(50), nullable=False)
    customer_preferences = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('customer_profile', uselist=False))


class Product(db.Model):
    __tablename__ = 'inventory_master'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_desc = db.Column(db.String(150), nullable=False)
    product_category_name = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_min_qoh = db.Column(db.Integer, nullable=False) #Minimum Quantity on hand
    product_curr_qoh = db.Column(db.Integer, nullable=False) #Current Quantity on hand
    product_supplier_name = db.Column(db.String(100), nullable=False)
    product_supplier_contact = db.Column(db.String(20), nullable=False)
    product_supplier_email = db.Column(db.String(120), nullable=False)


class Appointment(db.Model):
    __tablename__ = 'appointments'
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_master.customer_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_master.staff_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service_master.service_id'), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False)

    # Relationships to access related data easily
    customer = db.relationship('Customer', backref=db.backref('appointments', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('appointments', lazy=True))
    service = db.relationship('Service', backref=db.backref('appointments', lazy=True))


class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_master.customer_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_master.staff_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service_master.service_id'), nullable=False)
    other_charges = db.Column(db.Float, nullable=True)
    invoice_amount = db.Column(db.Float, nullable=False)
    total_charges = db.Column(db.Float, nullable=False)

    # Relationships
    customer = db.relationship('Customer', backref=db.backref('invoices', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('invoices', lazy=True))
    service = db.relationship('Service', backref=db.backref('invoices', lazy=True))


class InventoryTransaction(db.Model):
    __tablename__ = 'inventory_transactions'
    txn_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('inventory_master.product_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_master.staff_id'), nullable=False)
    txn_type = db.Column(db.Integer, nullable=False) #0 for ordering, 1 for replenishment, will bw populated based on the role - staff (ordering) or mana7ger (replenishment)
    quantity = db.Column(db.Integer, nullable=False)
    date_of_txn = db.Column(db.DateTime, nullable=False)

    # Relationships
    product = db.relationship('Product', backref=db.backref('transactions', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('inventory_transactions', lazy=True))


class StaffAttendance(db.Model):
    __tablename__ = 'staff_attendance'
    register_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_master.staff_id'), nullable=False)
    register_datetime = db.Column(db.DateTime, nullable=False) #Current Date and time for marking attendance

    # Relationship
    staff_member = db.relationship('Staff', backref=db.backref('attendance_records', lazy=True))


class CustomerReview(db.Model):
    __tablename__ = 'customer_review'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer_master.customer_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_master.staff_id'), nullable=False)
    invoice_number = db.Column(db.Integer, db.ForeignKey('invoices.invoice_number'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # rating 1-5 given by customer for the service experience
    review = db.Column(db.String(255), nullable=True)

    # Relationships
    customer = db.relationship('Customer', backref=db.backref('reviews', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('reviews', lazy=True))
    invoice = db.relationship('Invoice', backref=db.backref('review', uselist=False))


class Finance(db.Model):
    __tablename__ = 'finance'
    reporting_month = db.Column(db.DateTime, primary_key=True) # First day of the reporting month
    product_cost = db.Column(db.Float, nullable=False)
    total_revenue = db.Column(db.Float, nullable=False)
    staff_salary = db.Column(db.Float, nullable=False)
    service_commission = db.Column(db.Float, nullable=False) # Commission earned from services
    overheads = db.Column(db.Float, nullable=False)
    other = db.Column(db.Float, nullable=False)
    net_profit = db.Column(db.Float, nullable=True)


class Manager(db.Model, UserMixin):
    __tablename__ = 'manager_master'
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    manager_name = db.Column(db.String(100), nullable=False)
    manager_contact = db.Column(db.String(20), nullable=False)
    manager_skills = db.Column(db.String(255), nullable=False)
    manager_role = db.Column(db.String(50), nullable=False, default='Manager')
    manager_dob = db.Column(db.DateTime, nullable=False)
    manager_doj = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('manager_profile', uselist=False))


class Owner(db.Model, UserMixin):
    __tablename__ = 'owner_master'
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_contact = db.Column(db.String(20), nullable=False)
    owner_role = db.Column(db.String(50), nullable=False, default='Owner')

    user = db.relationship('User', backref=db.backref('owner_profile', uselist=False))
    



