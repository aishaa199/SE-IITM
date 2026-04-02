import random
from faker import Faker
from datetime import datetime, timedelta

from main import create_app
from application.models import *
from application.sec import datastore
from flask_security import hash_password

fake = Faker()

app = create_app()

NUM = 30


def create_users(role_name, count):
    users = []

    for i in range(count):
        username = f"{role_name}_{i}"

        user = datastore.create_user(
            username=username,
            password=hash_password("password")
        )

        role = Role.query.filter_by(name=role_name).first()
        datastore.add_role_to_user(user, role)

        users.append(user)

    db.session.commit()
    return users


def seed_services():
    categories = ["Hair", "Skin", "Spa", "Nails"]

    for i in range(NUM):
        s = Service(
            service_desc=fake.word().capitalize() + " Service",
            service_category=random.choice(categories),
            service_price=random.randint(200, 2000),
            service_duration=random.choice([30, 45, 60, 90]),
            service_products="Shampoo, Serum",
            service_rating=random.uniform(3.5, 5),
            no_of_reviews=random.randint(5, 200)
        )

        db.session.add(s)

    db.session.commit()


def seed_products():
    categories = ["Hair", "Skin", "Nails", "Spa"]

    for i in range(NUM):
        p = Product(
            product_desc=fake.word() + " product",
            product_category_name=random.choice(categories),
            product_price=random.randint(200, 1000),
            product_min_qoh=10,
            product_curr_qoh=random.randint(10, 100),
            product_supplier_name=fake.company(),
            product_supplier_contact=fake.phone_number(),
            product_supplier_email=fake.email(),
        )

        db.session.add(p)

    db.session.commit()


def seed_staff(users):

    for u in users:

        s = Staff(
            staff_id=u.id,
            staff_name=fake.name(),
            staff_contact=fake.phone_number(),
            staff_email=fake.email(),
            staff_skills="Haircut, Styling",
            staff_role="Stylist",
            staff_dob=fake.date_of_birth(minimum_age=20, maximum_age=40),
            staff_doj=fake.date_this_decade(),
            staff_salary=random.randint(20000, 50000),
            staff_cumulative_rating=random.uniform(3.5, 5),
            no_of_reviews=random.randint(5, 100)
        )

        db.session.add(s)

    db.session.commit()


def seed_customers(users):

    for u in users:

        c = Customer(
            customer_id=u.id,
            customer_name=fake.name(),
            customer_contact=fake.phone_number(),
            customer_dob=fake.date_of_birth(minimum_age=18, maximum_age=60),
            customer_email=fake.email(),
            customer_address=fake.address(),
            number_of_visits=random.randint(1, 20),
            customer_type=random.choice(["Regular", "Premium"]),
            customer_preferences="Haircut, Facial",
            customer_available_rewards=random.randint(0, 500),
            total_spend=random.randint(500, 20000)
        )

        db.session.add(c)

    db.session.commit()


def seed_appointments():

    customers = Customer.query.all()
    staff = Staff.query.all()
    services = Service.query.all()

    for i in range(NUM):

        app = Appointment(
            customer_id=random.choice(customers).customer_id,
            staff_id=random.choice(staff).staff_id,
            appointment_datetime=datetime.now() + timedelta(days=random.randint(-2, 5)),
            status=random.randint(0, 5)
        )

        app.services = random.sample(services, random.randint(1, 3))

        db.session.add(app)

    db.session.commit()


def seed_invoices():

    appointments = Appointment.query.all()

    for a in appointments[:NUM]:

        amount = random.randint(500, 3000)

        inv = Invoice(
            customer_id=a.customer_id,
            staff_id=a.staff_id,
            service_ids="1,2",
            other_charges=random.randint(0, 200),
            rewards_earned=random.randint(10, 50),
            rewards_utilized=random.randint(0, 20),
            current_reward_points=random.randint(50, 300),
            invoice_amount=amount,
            total_invoice_amount=amount + 100,
            payable_invoice_amount=amount,
            status=1,
            appointment_id=a.appointment_id
        )

        db.session.add(inv)

    db.session.commit()


def seed_reviews():

    customers = Customer.query.all()
    staff = Staff.query.all()
    invoices = Invoice.query.all()

    for i in range(NUM):

        r = CustomerReview(
            customer_id=random.choice(customers).customer_id,
            staff_id=random.choice(staff).staff_id,
            service_ids="1,2",
            apppointment_id=random.choice(Appointment.query.all()).appointment_id,
            invoice_number=random.choice(invoices).invoice_number,
            rating=random.randint(3, 5),
            review=fake.sentence()
        )

        db.session.add(r)

    db.session.commit()


def seed_finance():

    for i in range(12):

        revenue = random.randint(50000, 150000)

        f = Finance(
            reporting_month=datetime(2025, i + 1, 1),
            product_cost=random.randint(10000, 30000),
            total_revenue=revenue,
            staff_salary=random.randint(20000, 50000),
            overheads=random.randint(5000, 15000),
            other=random.randint(2000, 5000),
            net_profit=revenue - 40000
        )

        db.session.add(f)

    db.session.commit()


def seed_data():

    print("Seeding data...")

    staff_users = create_users("staff", NUM)
    customer_users = create_users("customer", NUM)

    seed_services()
    seed_products()
    seed_staff(staff_users)
    seed_customers(customer_users)
    seed_appointments()
    seed_invoices()
    seed_reviews()
    seed_finance()

    print("Done seeding!")


if __name__ == "__main__":

    with app.app_context():

        db.create_all()
        seed_data()