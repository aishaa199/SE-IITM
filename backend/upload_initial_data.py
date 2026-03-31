from application.sec import datastore
from application.models import db, Role, Owner
from flask_security import hash_password

def seed_initial_data():
    datastore.find_or_create_role(name='admin', description='Administrator with full access')
    datastore.find_or_create_role(name='owner', description='Salon Owner')
    datastore.find_or_create_role(name='manager', description='Salon Manager')
    datastore.find_or_create_role(name='staff', description='Salon Staff')
    datastore.find_or_create_role(name='customer', description='Regular customer')
    db.session.commit()

    if not datastore.find_user(username="admin"):
        datastore.create_user(username="admin", password=hash_password("admin"), roles=["admin"])

    if not datastore.find_user(username="owner"):
        owner_user = datastore.create_user(username="owner", password=hash_password("owner"), roles=["owner"])
        db.session.commit()
        
        # Create corresponding Owner entry
        if not Owner.query.get(owner_user.id):
            new_owner = Owner(
                owner_id=owner_user.id,
                owner_name='owner_name',
                owner_contact='0000000000'
            )
            db.session.add(new_owner)
            db.session.commit()


    db.session.commit()


if __name__ == '__main__':
    from main import create_app

    app = create_app()
    with app.app_context():
        db.create_all()
        seed_initial_data()