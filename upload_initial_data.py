from main import app
from application.sec import datastore
from application.models import db, Role
from flask_security import hash_password

with app.app_context():
    # Create all tables
    db.create_all()
    datastore.find_or_create_role(name='admin', description='Administrator with full access')
    datastore.find_or_create_role(name='owner', description='Salon Owner')
    datastore.find_or_create_role(name='manager', description='Salon Manager')
    datastore.find_or_create_role(name='staff', description='Salon Staff')
    datastore.find_or_create_role(name='customer', description='Regular customer')
    db.session.commit()

    if not datastore.find_user(username="admin"):
        datastore.create_user(username="admin", password=hash_password("admin"), roles=["admin"])

    if not datastore.find_user(username="owner"):
        datastore.create_user(username="owner", password=hash_password("owner"), roles=["owner"])

    if not datastore.find_user(username="manager"):
        datastore.create_user(username="manager", password=hash_password("manager"), roles=["manager"])

    if not datastore.find_user(username="staff1"):
        datastore.create_user(username="staff1", password=hash_password("staff1"), roles=["staff"])

    if not datastore.find_user(username="cust1"):
        datastore.create_user(username="cust1", password=hash_password("cust1"), roles=["customer"])

    db.session.commit()