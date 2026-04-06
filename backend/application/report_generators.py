"""
report_generators.py
--------------------
Builds CSV and PDF reports for each supported report type.
All functions must be called from within a Flask application context.
"""

import csv
import io
import os
from datetime import datetime, date, timedelta

from fpdf import FPDF
from sqlalchemy import func

# DejaVuSans ships with most Linux distros and supports the full Unicode BMP,
# including ₹, —, and other non-ASCII characters that break Helvetica in fpdf2.
_FONT_DIR = '/usr/share/fonts/truetype/dejavu'
_FONT_REG  = os.path.join(_FONT_DIR, 'DejaVuSans.ttf')
_FONT_BOLD = os.path.join(_FONT_DIR, 'DejaVuSans-Bold.ttf')
_HAVE_DEJAVU = os.path.isfile(_FONT_REG) and os.path.isfile(_FONT_BOLD)


def _make_pdf(orientation='L'):
    """Return an FPDF instance with the best available Unicode-capable font registered."""
    pdf = FPDF(orientation=orientation, unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=12)
    if _HAVE_DEJAVU:
        pdf.add_font('DejaVu',      '',  _FONT_REG,  uni=True)
        pdf.add_font('DejaVu',      'B', _FONT_BOLD, uni=True)
        pdf._report_font = 'DejaVu'
    else:
        # Fallback: strip non-latin chars before rendering
        pdf._report_font = 'Helvetica'
    return pdf


def _safe(text):
    """Replace characters outside latin-1 when DejaVu is unavailable."""
    if _HAVE_DEJAVU:
        return str(text)
    return str(text).encode('latin-1', errors='replace').decode('latin-1')

from .models import (
    db, Appointment, Invoice, Staff, StaffAttendance,
    Product, InventoryTransaction, Finance,
    CustomerReview, Customer, Service,
)


# ── Date-range helpers ────────────────────────────────────────────────────────

def get_date_range(time_period, custom_start=None, custom_end=None):
    """Return (start datetime, end datetime, human label) for a given period."""
    today = date.today()

    if time_period == 'daily':
        start = datetime.combine(today, datetime.min.time())
        end   = datetime.combine(today, datetime.max.time())
        label = f"Daily - {today.strftime('%d %b %Y')}"

    elif time_period == 'yesterday':
        yesterday = today - timedelta(days=1)
        start = datetime.combine(yesterday, datetime.min.time())
        end   = datetime.combine(yesterday, datetime.max.time())
        label = f"Yesterday - {yesterday.strftime('%d %b %Y')}"

    elif time_period == 'weekly':
        week_start = today - timedelta(days=today.weekday())
        start = datetime.combine(week_start, datetime.min.time())
        end   = datetime.combine(today, datetime.max.time())
        label = f"Weekly - {week_start.strftime('%d %b')} to {today.strftime('%d %b %Y')}"

    elif time_period == 'monthly':
        month_start = today.replace(day=1)
        start = datetime.combine(month_start, datetime.min.time())
        end   = datetime.combine(today, datetime.max.time())
        label = f"Monthly - {month_start.strftime('%B %Y')}"

    elif time_period == 'custom' and custom_start and custom_end:
        cs = datetime.strptime(custom_start, '%Y-%m-%d').date()
        ce = datetime.strptime(custom_end,   '%Y-%m-%d').date()
        start = datetime.combine(cs, datetime.min.time())
        end   = datetime.combine(ce, datetime.max.time())
        label = f"Custom - {cs.strftime('%d %b %Y')} to {ce.strftime('%d %b %Y')}"

    else:
        # Fallback: last 30 days
        start = datetime.combine(today - timedelta(days=30), datetime.min.time())
        end   = datetime.combine(today, datetime.max.time())
        label = f"Last 30 days - to {today.strftime('%d %b %Y')}"

    return start, end, label


# ── Per-report data queries ───────────────────────────────────────────────────

def sales_report_data(start, end):
    headers = [
        'Invoice #', 'Date', 'Customer', 'Services', 'Staff',
        'Invoice Amount (₹)', 'Rewards Used', 'Payable Amount (₹)',
    ]
    invoices = Invoice.query.filter(
        Invoice.invoice_date >= start.date(),
        Invoice.invoice_date <= end.date(),
    ).order_by(Invoice.invoice_date).all()

    rows = []
    for inv in invoices:
        customer_name = inv.customer.customer_name if inv.customer else 'N/A'
        staff_name    = inv.staff.staff_name if inv.staff else 'N/A'

        # Resolve service names from comma-separated IDs
        svc_ids  = [s.strip() for s in (inv.service_ids or '').split(',') if s.strip().isdigit()]
        svc_objs = Service.query.filter(Service.service_id.in_(svc_ids)).all() if svc_ids else []
        svc_names = ', '.join(s.service_desc for s in svc_objs) or 'N/A'

        rows.append([
            inv.invoice_number,
            inv.invoice_date.strftime('%d %b %Y'),
            customer_name,
            svc_names,
            staff_name,
            f"{inv.invoice_amount:.2f}",
            inv.rewards_utilized,
            f"{inv.payable_invoice_amount:.2f}",
        ])

    return headers, rows


def appointments_report_data(start, end):
    STATUS_MAP = {0: 'Booked', 1: 'Completed', 2: 'No-show',
                  3: 'Cancelled', 4: 'Rescheduled', 5: 'Invoiced'}
    headers = ['Appointment ID', 'Date & Time', 'Customer', 'Staff', 'Services', 'Status']

    appts = Appointment.query.filter(
        Appointment.appointment_datetime >= start,
        Appointment.appointment_datetime <= end,
    ).order_by(Appointment.appointment_datetime).all()

    rows = []
    for a in appts:
        svc_names    = ', '.join(s.service_desc for s in a.services) or 'N/A'
        customer_name = a.customer.customer_name if a.customer else 'N/A'
        staff_name    = a.staff.staff_name if a.staff else 'Unassigned'
        rows.append([
            a.appointment_id,
            a.appointment_datetime.strftime('%d %b %Y %H:%M'),
            customer_name,
            staff_name,
            svc_names,
            STATUS_MAP.get(a.status, 'Unknown'),
        ])

    return headers, rows


def staff_report_data(start, end):
    headers = [
        'Staff Name', 'Role', 'Skills',
        'Appointments Handled', 'Completed', 'Attendance Days',
        'Avg Rating',
    ]
    all_staff = Staff.query.order_by(Staff.staff_name).all()
    rows = []

    for s in all_staff:
        appts_total = Appointment.query.filter(
            Appointment.staff_id == s.staff_id,
            Appointment.appointment_datetime >= start,
            Appointment.appointment_datetime <= end,
        ).count()

        appts_completed = Appointment.query.filter(
            Appointment.staff_id == s.staff_id,
            Appointment.appointment_datetime >= start,
            Appointment.appointment_datetime <= end,
            Appointment.status == 1,
        ).count()

        attendance_days = db.session.query(
            func.count(func.distinct(func.date(StaffAttendance.register_datetime)))
        ).filter(
            StaffAttendance.staff_id == s.staff_id,
            StaffAttendance.register_datetime >= start,
            StaffAttendance.register_datetime <= end,
        ).scalar() or 0

        avg_rating = (
            f"{s.staff_cumulative_rating:.1f}" if s.staff_cumulative_rating else 'N/A'
        )

        rows.append([
            s.staff_name,
            s.staff_role,
            s.staff_skills,
            appts_total,
            appts_completed,
            attendance_days,
            avg_rating,
        ])

    return headers, rows


def inventory_report_data(start, end):
    headers = [
        'Product', 'Category', 'Supplier',
        'Current Stock', 'Min Stock', 'Low Stock Alert',
        'Units Used (period)', 'Units Restocked (period)',
    ]
    products = Product.query.order_by(Product.product_category_name, Product.product_desc).all()
    rows = []

    for p in products:
        used = db.session.query(func.sum(InventoryTransaction.quantity)).filter(
            InventoryTransaction.product_id == p.product_id,
            InventoryTransaction.txn_type == 0,          # 0 = staff ordering (usage)
            InventoryTransaction.date_of_txn >= start,
            InventoryTransaction.date_of_txn <= end,
        ).scalar() or 0

        restocked = db.session.query(func.sum(InventoryTransaction.quantity)).filter(
            InventoryTransaction.product_id == p.product_id,
            InventoryTransaction.txn_type == 1,          # 1 = replenishment
            InventoryTransaction.date_of_txn >= start,
            InventoryTransaction.date_of_txn <= end,
        ).scalar() or 0

        rows.append([
            p.product_desc,
            p.product_category_name,
            p.product_supplier_name,
            p.product_curr_qoh,
            p.product_min_qoh,
            'YES' if p.product_low_stock_alert else 'No',
            used,
            restocked,
        ])

    return headers, rows


def financial_report_data(start, end):
    headers = [
        'Month', 'Total Revenue (₹)', 'Product Cost (₹)',
        'Staff Salary (₹)', 'Overheads (₹)', 'Other (₹)', 'Net Profit (₹)',
    ]
    records = Finance.query.filter(
        Finance.reporting_month >= start,
        Finance.reporting_month <= end,
    ).order_by(Finance.reporting_month).all()

    rows = []
    for f in records:
        rows.append([
            f.reporting_month.strftime('%B %Y'),
            f"{f.total_revenue:.2f}",
            f"{f.product_cost:.2f}",
            f"{f.staff_salary:.2f}",
            f"{f.overheads:.2f}",
            f"{f.other:.2f}",
            f"{f.net_profit:.2f}" if f.net_profit is not None else 'N/A',
        ])

    return headers, rows


def feedback_report_data(start, end):
    headers = [
        'Review ID', 'Customer', 'Staff', 'Services',
        'Rating', 'Review', 'Sentiment',
    ]

    def sentiment(rating):
        if rating >= 4:   return 'Positive'
        elif rating == 3: return 'Neutral'
        else:             return 'Negative'

    # CustomerReview doesn't have a created_at date — join via Appointment datetime
    reviews = (
        db.session.query(CustomerReview)
        .join(Appointment, CustomerReview.apppointment_id == Appointment.appointment_id)
        .filter(
            Appointment.appointment_datetime >= start,
            Appointment.appointment_datetime <= end,
        )
        .order_by(Appointment.appointment_datetime.desc())
        .all()
    )

    rows = []
    for r in reviews:
        customer_name = r.customer.customer_name if r.customer else 'N/A'
        staff_name    = r.staff.staff_name if r.staff else 'N/A'
        svc_ids  = [s.strip() for s in (r.service_ids or '').split(',') if s.strip().isdigit()]
        svc_objs = Service.query.filter(Service.service_id.in_(svc_ids)).all() if svc_ids else []
        svc_names = ', '.join(s.service_desc for s in svc_objs) or 'N/A'

        rows.append([
            r.review_id,
            customer_name,
            staff_name,
            svc_names,
            r.rating,
            (r.review or '').replace('\n', ' '),
            sentiment(r.rating),
        ])

    return headers, rows


# ── File builders ─────────────────────────────────────────────────────────────

def build_csv_bytes(headers, rows):
    """Return a BytesIO containing UTF-8 encoded CSV data."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return io.BytesIO(output.getvalue().encode('utf-8'))


def build_pdf_bytes(title, headers, rows, period_label='', summary_stats=None):
    """Return a BytesIO containing a styled PDF report with Unicode support."""
    GOLD   = (212, 175, 55)
    LIGHT  = (249, 245, 240)
    WHITE  = (255, 255, 255)
    DARK   = (45,  45,  45)
    HEADER = (139, 105, 20)
    FONT   = 'DejaVu' if _HAVE_DEJAVU else 'Helvetica'

    pdf = _make_pdf(orientation='L')
    pdf.add_page()

    # ── Title block ──
    pdf.set_fill_color(*HEADER)
    pdf.rect(0, 0, 297, 28, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font(FONT, 'B', 16)
    pdf.set_xy(0, 5)
    pdf.cell(297, 10, _safe(title), align='C', ln=True)

    if period_label:
        pdf.set_font(FONT, '', 9)
        pdf.set_xy(0, 16)
        pdf.cell(297, 6, _safe(period_label), align='C', ln=True)

    pdf.set_text_color(*DARK)
    pdf.set_font(FONT, '', 8)
    pdf.set_xy(0, 23)
    pdf.cell(297, 4,
             _safe(f"Generated on {datetime.now().strftime('%d %b %Y %H:%M')}"),
             align='C', ln=True)
    pdf.ln(4)

    # ── Optional summary statistics block ──
    if summary_stats:
        pdf.set_fill_color(249, 245, 240)
        pdf.set_font(FONT, 'B', 8)
        pdf.set_text_color(*DARK)
        col_w_s = 277 / len(summary_stats)
        for label, value in summary_stats:
            pdf.set_fill_color(*LIGHT)
            pdf.cell(col_w_s, 12, _safe(f"{label}: {value}"), border=1, fill=True, align='C')
        pdf.ln(14)

    if not rows:
        pdf.set_font(FONT, '', 11)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, 'No data available for this period.', align='C')
        return io.BytesIO(bytes(pdf.output()))

    # ── Column widths ──
    page_w    = 277
    col_count = len(headers)
    col_w     = page_w / col_count

    # ── Header row ──
    pdf.set_fill_color(*GOLD)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font(FONT, 'B', 8)
    for h in headers:
        pdf.cell(col_w, 8, _safe(str(h)), border=1, fill=True, align='C')
    pdf.ln()

    # ── Data rows ──
    pdf.set_text_color(*DARK)
    pdf.set_font(FONT, '', 7)
    for i, row in enumerate(rows):
        pdf.set_fill_color(*(LIGHT if i % 2 == 0 else WHITE))
        for cell in row:
            text = _safe(str(cell) if cell is not None else '')
            if len(text) > 32:
                text = text[:29] + '...'
            pdf.cell(col_w, 6, text, border=1, fill=True)
        pdf.ln()

    return io.BytesIO(bytes(pdf.output()))


# ── Dispatcher ────────────────────────────────────────────────────────────────

REPORT_TITLES = {
    'sales':        'Sales Report',
    'appointments': 'Appointments Report',
    'staff':        'Staff Performance Report',
    'inventory':    'Inventory Report',
    'financial':    'Financial Report',
    'feedback':     'Customer Feedback Report',
}

REPORT_GENERATORS = {
    'sales':        sales_report_data,
    'appointments': appointments_report_data,
    'staff':        staff_report_data,
    'inventory':    inventory_report_data,
    'financial':    financial_report_data,
    'feedback':     feedback_report_data,
}


def generate_report(report_type, time_period, file_format,
                    custom_start=None, custom_end=None):
    """
    Main entry point.
    Returns (BytesIO, filename, mimetype) or raises ValueError.
    """
    if report_type not in REPORT_GENERATORS:
        raise ValueError(f"Unknown report type: {report_type}")
    if file_format not in ('csv', 'pdf'):
        raise ValueError(f"Unsupported format: {file_format}")

    start, end, label = get_date_range(time_period, custom_start, custom_end)
    headers, rows = REPORT_GENERATORS[report_type](start, end)
    title = REPORT_TITLES[report_type]
    period_slug = time_period if time_period != 'custom' else 'custom'
    filename = f"{report_type}_report_{period_slug}.{file_format}"

    if file_format == 'csv':
        file_obj = build_csv_bytes(headers, rows)
        mimetype = 'text/csv'
    else:
        file_obj = build_pdf_bytes(title, headers, rows, label)
        mimetype = 'application/pdf'

    return file_obj, filename, mimetype
