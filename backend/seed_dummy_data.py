import random
from datetime import date, datetime, timedelta

from main import create_app
from application.models import *
from application.sec import datastore
from flask_security import hash_password

app = create_app()

NUM = 30

# ── Realistic Indian names ────────────────────────────────────────────────────
FEMALE_NAMES = [
    "Priya Sharma", "Anjali Singh", "Kavitha Reddy", "Neha Gupta", "Sunita Patel",
    "Meera Nair", "Ritu Verma", "Deepika Joshi", "Pooja Agarwal", "Sonal Mehta",
    "Divya Iyer", "Sneha Kulkarni", "Lakshmi Rao", "Swati Desai", "Preeti Mishra",
    "Nandita Bose", "Rekha Pillai", "Ananya Chatterjee", "Shilpa Kaur", "Kiran Rao",
    "Nalini Murthy", "Vasudha Singh", "Padmavathi Reddy", "Usha Srinivasan",
    "Geeta Krishnan", "Sangeeta Bhatt", "Radha Menon", "Sumitha Suresh",
    "Yamini Nambiar", "Bindhu Pillai",
]

MALE_NAMES = [
    "Rahul Sharma", "Amit Kumar", "Vikram Singh", "Rohan Gupta", "Suresh Patel",
    "Arjun Nair", "Karthik Reddy", "Nikhil Verma", "Manish Joshi", "Sanjay Agarwal",
]

ALL_NAMES = FEMALE_NAMES + MALE_NAMES  # 40 names total, pick first 30 for staff, next 30 for customers

CUSTOMER_NAMES = [
    "Aditi Sharma", "Bhavna Patel", "Chitra Nair", "Disha Gupta", "Ekta Reddy",
    "Falguni Mehta", "Gargi Iyer", "Hema Kulkarni", "Indira Rao", "Jaya Desai",
    "Kamla Mishra", "Lavanya Bose", "Madhuri Pillai", "Nisha Chatterjee", "Omika Kaur",
    "Pallavi Krishnan", "Qureshi Fatima", "Roshni Bhatt", "Sheetal Menon", "Tanvi Suresh",
    "Uma Nambiar", "Varsha Singh", "Wridhi Sharma", "Xenia Fernandez", "Yashoda Verma",
    "Zeenath Begum", "Asha Shetty", "Bijaya Mohanty", "Chandrika Rao", "Darshana Joshi",
]

# ── Phone numbers (Indian format) ─────────────────────────────────────────────
def indian_phone():
    prefixes = ["98", "97", "96", "95", "94", "93", "91", "90", "89", "88", "87", "86"]
    return "+91-" + random.choice(prefixes) + str(random.randint(10000000, 99999999))

def indian_email(name):
    parts = name.lower().split()
    domains = ["gmail.com", "yahoo.in", "hotmail.com", "outlook.com", "rediffmail.com"]
    suffix = random.randint(10, 999)
    return f"{parts[0]}.{parts[-1]}{suffix}@{random.choice(domains)}"

# ── Date helpers ──────────────────────────────────────────────────────────────
TODAY = date(2026, 4, 4)
RANGE_START = datetime(2026, 1, 1, 9, 0)   # Jan 1, 2026
RANGE_END   = datetime(2026, 5, 5, 18, 0)  # May 5, 2026 (today)

def random_past_dt(days_back_max=94):
    """Random datetime within last ~3 months, during salon hours (9AM–7PM)."""
    delta = random.randint(0, days_back_max)
    hour  = random.randint(9, 18)
    minute = random.choice([0, 15, 30, 45])
    return datetime(2026, 1, 1) + timedelta(days=delta, hours=hour, minutes=minute)

def random_future_dt(days_ahead=14):
    """Random upcoming datetime for booked appointments."""
    delta = random.randint(1, days_ahead)
    hour  = random.randint(9, 18)
    minute = random.choice([0, 15, 30, 45])
    return datetime(2026, 4, 4) + timedelta(days=delta, hours=hour, minutes=minute)


# ── Seed helpers ──────────────────────────────────────────────────────────────
def create_users(role_name, count):
    users = []
    for i in range(count):
        username = f"{role_name}_{i+1:02d}"
        user = datastore.create_user(
            username=username,
            password=hash_password("password")
        )
        role = Role.query.filter_by(name=role_name).first()
        datastore.add_role_to_user(user, role)
        users.append(user)
    db.session.commit()
    return users


# ── Services ─────────────────────────────────────────────────────────────────
SALON_SERVICES = [
    # (name, category, price, duration_min, products_used, rating, reviews)
    ("Ladies Haircut & Styling",    "Hair",   550,  60,  "Wella Shampoo, Streax Serum, L'Oreal Conditioner",       4.7, 128),
    ("Gents Haircut",               "Hair",   200,  30,  "Wella Shampoo, Axe Styling Gel",                          4.5,  95),
    ("Hair Coloring – Global",      "Hair",  1800,  90,  "Schwarzkopf Hair Color, Wella Developer, Olaplex",        4.6,  74),
    ("Hair Highlights",             "Hair",  2800, 120,  "Matrix Hair Dye, Wella Developer, Toner",                 4.8,  52),
    ("Kerasmooth / Keratin Treat.", "Hair",  4500, 150,  "Brazilian Keratin Formula, Schwarzkopf Shampoo",          4.9,  38),
    ("Hair Spa & Deep Condition.",  "Hair",  1100,  60,  "L'Oreal Hair Spa Kit, Streax Serum, Biotique Oil",        4.6,  89),
    ("Blow Dry & Setting",          "Hair",   400,  45,  "Wella Heat Protect Spray, Streax Serum",                  4.4,  67),
    ("Head Massage",                "Hair",   350,  30,  "Figaro Olive Oil, Kesh King Hair Oil",                    4.5, 112),
    ("Eyebrow Threading",           "Skin",    60,  15,  "Aloe Vera Gel",                                           4.3, 245),
    ("Full Face Threading",         "Skin",   180,  20,  "Aloe Vera Gel, Rose Water Toner",                         4.4, 180),
    ("Upper Lip Threading",         "Skin",    40,  10,  "Aloe Vera Gel",                                           4.2, 310),
    ("Basic Cleanup",               "Skin",   450,  30,  "Lotus Herbals Scrub, Biotique Face Pack",                 4.3,  98),
    ("Basic Facial",                "Skin",   750,  60,  "Lotus Herbals Facial Kit, Casmara Mask",                  4.5,  87),
    ("Gold Facial",                 "Skin",  1400,  75,  "Shahnaz Husain Gold Facial Kit, 24K Gold Serum",          4.7,  63),
    ("Diamond Facial",              "Skin",  1900,  90,  "Casmara Diamond Pack, Vitamin C Serum, SPF Cream",        4.8,  44),
    ("De-Tan Pack",                 "Skin",   550,  40,  "Jovees De-Tan Pack, Multani Mitti, Lemon Extract",        4.4,  76),
    ("Full Arms Waxing",            "Skin",   350,  30,  "Rica Brazilian Wax, Pre-wax Oil, Soothing Lotion",        4.2, 134),
    ("Full Legs Waxing",            "Skin",   550,  45,  "Rica Brazilian Wax, Pre-wax Oil, Soothing Lotion",        4.3, 118),
    ("Full Body Waxing",            "Skin",  2200,  90,  "Rica Brazilian Wax, Anne French Cream, Soothing Lotion",  4.5,  42),
    ("Eyebrow Shaping & Tint",      "Skin",   280,  20,  "Refectocil Tint, Brow Fix Gel",                           4.6,  95),
    ("Classic Manicure",            "Nails",  500,  45,  "OPI Nail Polish, Cuticle Oil, Hand Cream",                4.4,  88),
    ("Classic Pedicure",            "Nails",  700,  60,  "OPI Nail Polish, Foot Scrub, Callus Remover",             4.5,  79),
    ("Gel Nail Extension",          "Nails", 2000,  90,  "Gel Builder, UV Gel Top Coat, Nail Tips",                 4.7,  56),
    ("Nail Art (per nail)",         "Nails",  300,  30,  "Nail Art Polish, Dotting Tools, Gel Top Coat",            4.8,  71),
    ("Acrylic Nail Extension",      "Nails", 1800,  90,  "Acrylic Powder, Monomer, UV Lamp Gel",                    4.6,  38),
    ("Swedish Body Massage",        "Spa",   2500,  60,  "Aroma Massage Oil, Ylang-Ylang Essential Oil",            4.8,  45),
    ("Aromatherapy Massage",        "Spa",   3000,  75,  "Lavender Oil, Eucalyptus Oil, Carrier Oil",               4.9,  33),
    ("Body Scrub & Wrap",           "Spa",   2000,  60,  "Coffee Scrub, Dead Sea Salt, Shea Butter Wrap",           4.7,  29),
    ("Bridal Makeup Package",       "Makeup",12000, 180, "Lakme Absolute Foundation, MAC Lipstick, Huda Eyeshadow", 4.9,  22),
    ("Party Makeup",                "Makeup", 3000,  90, "Lakme Foundation, Maybelline Kajal, L'Oreal Setting Spray",4.6, 61),
]

def seed_services():
    for (name, cat, price, dur, prods, rating, reviews) in SALON_SERVICES:
        s = Service(
            service_desc=name,
            service_category=cat,
            service_price=price,
            service_duration=dur,
            service_products=prods,
            service_rating=rating,
            no_of_reviews=reviews,
        )
        db.session.add(s)
    db.session.commit()
    print(f"  Seeded {len(SALON_SERVICES)} services.")


# ── Products / Inventory ──────────────────────────────────────────────────────
SALON_PRODUCTS = [
    # (name, category, price, min_qty, curr_qty, supplier, supplier_contact, supplier_email)
    ("Wella Professionals Shampoo 1L",        "Hair",   850,  5, 22, "Wella India Pvt Ltd",          "+91-2266130000", "orders@wella.in"),
    ("Schwarzkopf IGORA Hair Color 60g",      "Hair",   780,  8, 35, "Henkel India Ltd",             "+91-2240791000", "supply@henkel.in"),
    ("L'Oreal Professionnel Conditioner 1L",  "Hair",   920,  5, 18, "L'Oreal India Pvt Ltd",        "+91-2261771000", "b2b@loreal.in"),
    ("Matrix Hair Dye Cream 90g",             "Hair",   650,  10, 42, "Revlon India Ltd",            "+91-1147025800", "orders@revlon.in"),
    ("Streax Professional Hair Serum 500ml",  "Hair",   480,  6, 28, "Hygienic Research Inst.",      "+91-2267820500", "sales@streax.in"),
    ("Olaplex Bond Multiplier No.1 100ml",    "Hair",  2400,  3, 10, "Nykaa Wholesale",             "+91-2250961000", "bulk@nykaa.com"),
    ("Figaro Olive Oil 200ml",                "Hair",   180,  10, 55, "Figaro India",                "+91-4422340000", "supply@figaro.in"),
    ("Kesh King Hair Oil 300ml",              "Hair",   220,  10, 40, "Emami Ltd",                   "+91-3322139920", "orders@emami.in"),
    ("Wella Heat Protect Spray 150ml",        "Hair",   650,  5, 15, "Wella India Pvt Ltd",          "+91-2266130000", "orders@wella.in"),
    ("Lotus Herbals Facial Kit",              "Skin",   695,  5, 20, "Lotus Herbals Pvt Ltd",        "+91-1146791600", "b2b@lotusherbals.com"),
    ("Shahnaz Husain Gold Facial Kit",        "Skin",  1250,  4, 12, "Shahnaz Husain Group",         "+91-1127010000", "orders@shahnazgroup.com"),
    ("VLCC Diamond Bleach 60g",               "Skin",   280,  12, 48, "VLCC Health Care Ltd",        "+91-1244223700", "sales@vlcc.in"),
    ("Jovees De-Tan Pack 100g",               "Skin",   320,  8, 30, "Jovees Herbal Care",           "+91-1124636640", "orders@jovees.com"),
    ("Casmara Algae Peel-off Mask Kit",       "Skin",  2800,  3, 8,  "Casmara India",               "+91-2226001200", "supply@casmara.in"),
    ("Biotique Bio Mud Facial Pack 75g",      "Skin",   195,  10, 35, "Biotique",                    "+91-1124683401", "bulk@biotique.in"),
    ("Rica Brazilian Wax 400g",               "Skin",   850,  6, 24, "Rica Professional India",      "+91-2265108000", "orders@rica.in"),
    ("Anne French Hair Removal Cream 40g",    "Skin",   120,  15, 60, "Reckitt India Ltd",           "+91-1244224000", "trade@reckitt.in"),
    ("Aloe Vera Soothing Gel 500ml",          "Skin",   280,  8, 32, "WOW Skin Science",             "+91-8042074100", "bulk@wowskin.in"),
    ("Refectocil Eyebrow Tint 15ml",          "Skin",   450,  5, 18, "Refectocil India",             "+91-2226544000", "sales@refectocil.in"),
    ("SPF 50 Sunscreen 60ml",                 "Skin",   380,  8, 28, "Neutrogena India",             "+91-2244765000", "trade@neutrogena.in"),
    ("OPI Nail Lacquer 15ml",                 "Nails",  950,  6, 40, "OPI India",                    "+91-2226005000", "orders@opi.in"),
    ("Sally Hansen Nail Color 14.7ml",        "Nails",  380,  8, 55, "Coty India",                   "+91-2244213000", "supply@coty.in"),
    ("Cuticle Oil Pen 7ml",                   "Nails",  280,  10, 45, "OPI India",                   "+91-2226005000", "orders@opi.in"),
    ("UV Gel Top Coat 15g",                   "Nails",  650,  5, 22, "Born Pretty India",            "+91-7022234500", "bulk@bornpretty.in"),
    ("Gel Builder Clear 30g",                 "Nails",  850,  4, 14, "Born Pretty India",            "+91-7022234500", "bulk@bornpretty.in"),
    ("Aroma Massage Oil 500ml",               "Spa",    680,  4, 16, "Soulflower Wellness",          "+91-2266103000", "orders@soulflower.in"),
    ("Lavender Essential Oil 30ml",           "Spa",    520,  6, 20, "Soulflower Wellness",          "+91-2266103000", "orders@soulflower.in"),
    ("Coffee Body Scrub 200g",                "Spa",    480,  5, 18, "mCaffeine India",              "+91-9867988888", "b2b@mcaffeine.in"),
    ("Lakme Absolute Foundation 30ml",        "Makeup", 750,  4, 14, "Hindustan Unilever Ltd",       "+91-2239830000", "trade@hul.com"),
    ("MAC Studio Fix Powder Plus 15g",        "Makeup",2800,  3,  8,  "MAC Cosmetics India",         "+91-2267181000", "orders@maccosmetics.in"),
]

def seed_products():
    for (name, cat, price, min_q, curr_q, supplier, s_phone, s_email) in SALON_PRODUCTS:
        low_stock = curr_q <= min_q
        p = Product(
            product_desc=name,
            product_category_name=cat,
            product_price=price,
            product_min_qoh=min_q,
            product_curr_qoh=curr_q,
            product_supplier_name=supplier,
            product_supplier_contact=s_phone,
            product_supplier_email=s_email,
            product_low_stock_alert=low_stock,
        )
        db.session.add(p)
    db.session.commit()
    print(f"  Seeded {len(SALON_PRODUCTS)} products.")


# ── Staff ─────────────────────────────────────────────────────────────────────
STAFF_PROFILES = [
    # (name, role, skills, salary) - divided by 20
    ("Priya Sharma",        "Senior Stylist",      "Ladies Haircut, Hair Coloring, Hair Spa, Blow Dry",         1900),
    ("Anjali Singh",        "Beautician",          "Facial, Waxing, Threading, Cleanup, De-Tan Pack",          1600),
    ("Kavitha Reddy",       "Nail Technician",     "Manicure, Pedicure, Gel Extensions, Nail Art",              1450),
    ("Neha Gupta",          "Makeup Artist",       "Bridal Makeup, Party Makeup, Saree Draping",               2100),
    ("Sunita Patel",        "Spa Therapist",       "Swedish Massage, Aromatherapy, Body Scrub & Wrap",         1750),
    ("Meera Nair",          "Senior Beautician",   "Gold Facial, Diamond Facial, Waxing, Eyebrow Tint",        1800),
    ("Ritu Verma",          "Stylist",             "Ladies Haircut, Blow Dry, Hair Spa, Head Massage",         1400),
    ("Deepika Joshi",       "Beautician",          "Threading, Cleanup, De-Tan, Full Body Waxing",             1350),
    ("Pooja Agarwal",       "Junior Stylist",      "Gents Haircut, Ladies Haircut, Blow Dry",                  1200),
    ("Sonal Mehta",         "Senior Nail Tech",    "Nail Art, Gel Extensions, Acrylic Extensions, Pedicure",   1550),
    ("Divya Iyer",          "Spa Therapist",       "Aromatherapy, Swedish Massage, Head Massage",              1650),
    ("Sneha Kulkarni",      "Beautician",          "Facial, Waxing, Threading, Eyebrow Tint",                  1300),
    ("Lakshmi Rao",         "Senior Stylist",      "Hair Coloring, Highlights, Keratin Treatment, Blow Dry",   2000),
    ("Swati Desai",         "Makeup Artist",       "Party Makeup, Bridal Makeup, HD Makeup",                   1950),
    ("Preeti Mishra",       "Beautician",          "Cleanup, Facial, De-Tan, Waxing",                          1250),
    ("Nandita Bose",        "Junior Stylist",      "Ladies Haircut, Head Massage, Blow Dry",                   1100),
    ("Rekha Pillai",        "Senior Beautician",   "Gold Facial, Cleanup, Waxing, Threading",                  1700),
    ("Ananya Chatterjee",   "Nail Technician",     "Manicure, Pedicure, Nail Art, Gel Top Coat",               1400),
    ("Shilpa Kaur",         "Stylist",             "Hair Coloring, Hair Spa, Blow Dry, Ladies Haircut",        1500),
    ("Kiran Rao",           "Spa Therapist",       "Body Scrub & Wrap, Swedish Massage, Hot Stone Therapy",    1700),
    ("Nalini Murthy",       "Beautician",          "Diamond Facial, Waxing, De-Tan, Eyebrow Shaping",          1350),
    ("Vasudha Singh",       "Junior Nail Tech",    "Manicure, Pedicure, Basic Nail Art",                       1050),
    ("Padmavathi Reddy",    "Senior Stylist",      "Keratin Treatment, Hair Coloring, Blow Dry",               2050),
    ("Usha Srinivasan",     "Beautician",          "Threading, Waxing, Facial, Cleanup",                       1300),
    ("Geeta Krishnan",      "Makeup Artist",       "Bridal Makeup, Party Makeup, Airbrush Makeup",             2200),
    ("Sangeeta Bhatt",      "Stylist",             "Ladies Haircut, Highlights, Hair Spa",                     1500),
    ("Radha Menon",         "Beautician",          "Facial, De-Tan, Cleanup, Waxing",                          1250),
    ("Sumitha Suresh",      "Nail Technician",     "Nail Art, Gel Extensions, Acrylic Nails, Pedicure",        1450),
    ("Yamini Nambiar",      "Junior Stylist",      "Gents Haircut, Head Massage, Blow Dry",                    1100),
    ("Bindhu Pillai",       "Senior Beautician",   "Gold Facial, Waxing, Threading, De-Tan Pack",              1750),
]

def seed_staff(users):
    for i, u in enumerate(users):
        name, role, skills, salary = STAFF_PROFILES[i % len(STAFF_PROFILES)]
        dob = date(random.randint(1985, 2000), random.randint(1, 12), random.randint(1, 28))
        doj = date(random.randint(2022, 2025), random.randint(1, 12), random.randint(1, 28))
        s = Staff(
            staff_id=u.id,
            staff_name=name,
            staff_contact=indian_phone(),
            staff_email=indian_email(name),
            staff_skills=skills,
            staff_role=role,
            staff_dob=dob,
            staff_doj=doj,
            staff_salary=salary,
            staff_cumulative_rating=round(random.uniform(3.8, 4.9), 1),
            no_of_reviews=random.randint(15, 120),
        )
        db.session.add(s)
    db.session.commit()
    print(f"  Seeded {len(users)} staff members.")


# ── Customers ─────────────────────────────────────────────────────────────────
CUSTOMER_PREFS = [
    "Haircut, Facial",
    "Waxing, Threading, Facial",
    "Nail Art, Pedicure, Manicure",
    "Hair Coloring, Highlights, Blow Dry",
    "Bridal Makeup, Facial",
    "Swedish Massage, Body Scrub",
    "Keratin Treatment, Hair Spa",
    "Cleanup, De-Tan, Threading",
    "Gents Haircut, Head Massage",
    "Party Makeup, Eyebrow Tint",
]

ADDRESSES = [
    "12, MG Road, Koramangala, Bengaluru – 560034",
    "45, Linking Road, Bandra West, Mumbai – 400050",
    "8, Green Park Extension, New Delhi – 110016",
    "22, Nungambakkam High Road, Chennai – 600034",
    "67, Jubilee Hills, Hyderabad – 500033",
    "3, Alipore Road, Kolkata – 700027",
    "90, FC Road, Shivajinagar, Pune – 411005",
    "15, C Scheme, Jaipur – 302001",
    "55, Navrangpura, Ahmedabad – 380009",
    "7, Indiranagar, Bengaluru – 560038",
    "33, Aundh, Pune – 411007",
    "19, Sector 15, Chandigarh – 160015",
    "28, Salt Lake City, Kolkata – 700064",
    "41, Lajpat Nagar, New Delhi – 110024",
    "6, Andheri West, Mumbai – 400058",
]

def seed_customers(users):
    used_emails = set()
    for i, u in enumerate(users):
        name = CUSTOMER_NAMES[i % len(CUSTOMER_NAMES)]
        email = indian_email(name)
        while email in used_emails:
            email = indian_email(name)
        used_emails.add(email)

        dob = date(random.randint(1975, 2002), random.randint(1, 12), random.randint(1, 28))
        visits = random.randint(1, 24)
        total_spend = round(random.uniform(800, 45000), 2)
        c = Customer(
            customer_id=u.id,
            customer_name=name,
            customer_contact=indian_phone(),
            customer_dob=dob,
            customer_email=email,
            customer_address=random.choice(ADDRESSES),
            number_of_visits=visits,
            customer_type=random.choice(["Regular", "Regular", "Premium", "Walk-in"]),
            customer_preferences=random.choice(CUSTOMER_PREFS),
            customer_available_rewards=random.randint(0, 800),
            total_spend=total_spend,
        )
        db.session.add(c)
    db.session.commit()
    print(f"  Seeded {len(users)} customers.")


# ── Appointments (spread over Jan–Apr 2026) ───────────────────────────────────
def seed_appointments():
    customers = Customer.query.all()
    staff     = Staff.query.all()
    services  = Service.query.all()

    # 70% past appointments (Jan 1 – Apr 3) → Completed/Invoiced/No-show/Cancelled
    # 30% upcoming (Apr 5 – Apr 18)  → Booked/Rescheduled
    past_count   = int(NUM * 2.5)   # ~75 past appointments for richer analytics
    future_count = int(NUM * 0.5)   # ~15 upcoming

    for _ in range(past_count):
        appt_dt = random_past_dt(days_back_max=93)
        # Weight statuses: mostly Completed or Invoiced
        status = random.choices(
            [1, 5, 2, 3, 4],   # Completed, Invoiced, No-show, Cancelled, Rescheduled
            weights=[40, 35, 10, 10, 5],
        )[0]
        appt = Appointment(
            customer_id=random.choice(customers).customer_id,
            staff_id=random.choice(staff).staff_id,
            appointment_datetime=appt_dt,
            status=status,
            feedback_given=(status in [1, 5] and random.random() > 0.3),
        )
        appt.services = random.sample(services, random.randint(1, 3))
        db.session.add(appt)

    for _ in range(future_count):
        appt_dt = random_future_dt(days_ahead=14)
        status = random.choice([0, 4])  # Booked or Rescheduled
        appt = Appointment(
            customer_id=random.choice(customers).customer_id,
            staff_id=random.choice(staff).staff_id,
            appointment_datetime=appt_dt,
            status=status,
            feedback_given=False,
        )
        appt.services = random.sample(services, random.randint(1, 2))
        db.session.add(appt)

    db.session.commit()
    print(f"  Seeded {past_count + future_count} appointments (Jan–Apr 2026).")


# ── Invoices ──────────────────────────────────────────────────────────────────
def seed_invoices():
    # Only invoice completed / invoiced appointments
    completed_appts = Appointment.query.filter(Appointment.status.in_([1, 5])).all()
    invoiced = 0
    for a in completed_appts:
        svc_total = sum(s.service_price for s in a.services)
        other_charges = random.choice([0, 50, 100, 150, 200])
        rewards_earned = int(svc_total * 0.05)
        rewards_used   = random.randint(0, min(50, rewards_earned))
        payable        = svc_total + other_charges - rewards_used
        appt_date      = a.appointment_datetime.date()

        inv = Invoice(
            invoice_date=appt_date,
            customer_id=a.customer_id,
            staff_id=a.staff_id,
            service_ids=",".join(str(s.service_id) for s in a.services),
            other_charges=other_charges,
            rewards_earned=rewards_earned,
            rewards_utilized=rewards_used,
            current_reward_points=rewards_earned - rewards_used,
            invoice_amount=svc_total,
            total_invoice_amount=svc_total + other_charges,
            payable_invoice_amount=payable,
            status=random.choice([1, 2]),    # 1: Invoiced, 2: Sent
            appointment_id=a.appointment_id,
        )
        db.session.add(inv)
        a.status = 5  # mark as Invoiced
        invoiced += 1

    db.session.commit()
    print(f"  Seeded {invoiced} invoices.")


# ── Reviews ───────────────────────────────────────────────────────────────────
REVIEW_TEXTS = [
    "Absolutely loved the service! The staff was very professional and skilled.",
    "Very hygienic salon. The facial made my skin glow for days. Will visit again!",
    "Priya did an amazing job with my hair coloring. Exactly the shade I wanted.",
    "The waxing was done quickly and with minimal pain. Great experience overall.",
    "Loved my bridal makeup. Received so many compliments on my wedding day!",
    "Threading was fast and precise. Very gentle on the skin.",
    "The keratin treatment is worth every rupee. My hair feels silky smooth.",
    "Staff is very friendly and the ambience is relaxing. Enjoyed my spa session.",
    "My nails look stunning! The gel extensions lasted over 3 weeks.",
    "Good service but had to wait a bit longer than expected.",
    "The gold facial was luxurious. My skin feels rejuvenated and fresh.",
    "Excellent haircut! She understood exactly what I wanted.",
    "The Swedish massage was incredibly relaxing. Highly recommended!",
    "Nice place with good hygiene standards. The pedicure was very thorough.",
    "The makeup for my sister's reception was flawless. Very happy with the result.",
    "Took a bit long for the highlights but the result is beautiful!",
    "Very satisfied with the cleanup. Skin feels much cleaner and brighter.",
    "Professional staff, clean environment, and great results. 5 stars!",
    "The body scrub session was refreshing. Would definitely come back for more.",
    "Loved the nail art designs. Very creative and detailed work.",
    "Average experience. The service was okay but expected better for the price.",
    "The de-tan pack worked really well. Noticeable difference after one session.",
    "Head massage was very relaxing after a long week at work.",
    "Salon is well-maintained and the staff is knowledgeable about products.",
    "My go-to salon for all beauty needs. Never disappointed!",
]

def seed_reviews():
    # Review feedback_given appointments that have invoices
    reviewed_appts = Appointment.query.filter(
        Appointment.feedback_given == True
    ).all()

    invoices = Invoice.query.all()
    inv_by_appt = {inv.appointment_id: inv for inv in invoices}

    added = 0
    for a in reviewed_appts:
        inv = inv_by_appt.get(a.appointment_id)
        r = CustomerReview(
            customer_id=a.customer_id,
            staff_id=a.staff_id,
            service_ids=",".join(str(s.service_id) for s in a.services),
            apppointment_id=a.appointment_id,
            invoice_number=inv.invoice_number if inv else None,
            rating=random.choices([3, 4, 5], weights=[10, 35, 55])[0],
            review=random.choice(REVIEW_TEXTS),
        )
        db.session.add(r)
        added += 1

    db.session.commit()
    print(f"  Seeded {added} customer reviews.")


def seed_finance():
    for (yr, mo, rev, cost, salary, overhead) in MONTHLY_FINANCE:
        revenue = rev + random.randint(-8000, 8000)
        product_cost = cost + random.randint(-2000, 2000)
        staff_salary = salary
        overheads    = overhead + random.randint(-2000, 2000)
        other        = 0.0  # Changed: Don't auto-fill, let manager enter via Edit button
        net_profit   = revenue - product_cost - (staff_salary / 10) - overheads - other
        # (salary divided by 10 since we're tracking one branch portion)

        f = Finance(
            reporting_month=datetime(yr, mo, 1),
            product_cost=round(product_cost, 2),
            total_revenue=round(revenue, 2),
            staff_salary=round(staff_salary / 10, 2),
            overheads=round(overheads, 2),
            other=round(other, 2),
            net_profit=round(net_profit, 2),
        )
        db.session.add(f)

    db.session.commit()
    print(f"  Seeded {len(MONTHLY_FINANCE)} months of finance data (Jan–Apr 2026).")


# ── Staff Attendance ──────────────────────────────────────────────────────────
def seed_staff_attendance():
    staff = Staff.query.all()
    attendance_records = 0
    today_date = datetime(2026, 4, 8)
    
    # Ensure 5-8 staff are present today (2026-04-08)
    staff_list = list(staff)
    random.shuffle(staff_list)
    num_present_today = random.randint(5, min(8, len(staff_list)))
    
    for idx, s in enumerate(staff_list):
        # For today's attendance: mark 5-8 staff as present
        if idx < num_present_today:
            today_time = today_date.replace(hour=random.randint(9, 11), minute=random.randint(0, 59))
            attendance = StaffAttendance(
                staff_id=s.staff_id,
                register_datetime=today_time,
            )
            db.session.add(attendance)
            attendance_records += 1
        
        # Add past attendance records (Jan 1 – Apr 7) - reduced to 30-40 per staff
        for _ in range(random.randint(30, 40)):
            dt = random_past_dt(days_back_max=93)
            # Skip if this happens to be today
            if dt.date() == today_date.date():
                continue
            # Ensure attendance is during working hours (9 AM - 7 PM)
            if dt.hour < 9:
                dt = dt.replace(hour=random.randint(9, 11))
            elif dt.hour > 18:
                dt = dt.replace(hour=random.randint(9, 18))
            
            attendance = StaffAttendance(
                staff_id=s.staff_id,
                register_datetime=dt,
            )
            db.session.add(attendance)
            attendance_records += 1
    
    db.session.commit()
    print(f"  Seeded {attendance_records} staff attendance records (Jan–Apr 2026).")
    print(f"  ✓ Today (2026-04-08): {num_present_today} staff marked present.")


# ── Inventory Transactions ────────────────────────────────────────────────────
def seed_inventory_transactions():
    products = Product.query.all()
    staff    = Staff.query.all()
    services = Service.query.all()

    txn_count = 0
    for _ in range(NUM * 2):
        txn_dt = random_past_dt(days_back_max=93)
        product = random.choice(products)
        s = random.choice(staff)
        txn = InventoryTransaction(
            product_id=product.product_id,
            staff_id=s.staff_id,
            service_id=random.choice(services).service_id,
            txn_type=random.choice([0, 1]),   # 0: ordering, 1: replenishment
            quantity=random.randint(1, 5),
            date_of_txn=txn_dt,
        )
        db.session.add(txn)
        txn_count += 1

    db.session.commit()
    print(f"  Seeded {txn_count} inventory transactions.")


# ── Main ──────────────────────────────────────────────────────────────────────
def seed_data():
    print("\n🌱 Seeding realistic salon data (Jan–May 2026)...\n")

    staff_users    = create_users("staff",    NUM)
    customer_users = create_users("customer", NUM)

    seed_services()
    seed_products()
    seed_staff(staff_users)
    seed_customers(customer_users)
    seed_appointments()
    seed_invoices()
    seed_reviews()
    # seed_finance()  # Disabled: Finance records should be generated manually via POST API, not pre-seeded
    seed_staff_attendance()
    seed_inventory_transactions()

    print("\n✅ Done! Database seeded with realistic Indian salon data.\n")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
