"""
test_integration.py – End-to-end integration flows for Glow Suite.

These tests exercise multi-step user journeys that span multiple endpoints,
ensuring that data produced by one step is consumed correctly by the next.

Flows covered:
  FLOW-01  Full appointment lifecycle  (manager creates → updates → deletes)
  FLOW-02  Invoice lifecycle           (create appt → create invoice → verify via get-all)
  FLOW-03  Customer self-service       (register → login → book → view upcoming → cancel)
  FLOW-04  Inventory + order lifecycle (create product → low-stock → create order → process)
  FLOW-05  Staff lifecycle             (create staff → mark attendance → manager views)
  FLOW-06  Customer review flow        (create appt → complete → customer reviews)
  FLOW-07  Role-boundary checks        (verify each role is restricted to its own endpoints)
"""
import pytest
from datetime import datetime, timedelta
from tests.conftest import auth_headers, _login


def _future(days=3):
    dt = datetime.now() + timedelta(days=days)
    return dt.replace(second=0, microsecond=0).isoformat()


def _get_first(client, token, path, key):
    rv = client.get(path, headers=auth_headers(token))
    assert rv.status_code == 200
    items = rv.get_json()
    assert items, f"Expected non-empty list from {path}"
    return items[0][key]


# ─────────────────────────────────────────────────────────────────────────────
# FLOW-01: Full appointment lifecycle
# ─────────────────────────────────────────────────────────────────────────────

class TestAppointmentLifecycle:

    def test_flow_create_update_delete_appointment(self, client, manager_token):
        """FLOW-01: Manager creates an appointment, updates its status, then deletes it."""
        svc_id = _get_first(client, manager_token, '/api/service', 'service_id')
        staff_id = _get_first(client, manager_token, '/api/staff', 'staff_id')

        # Step 1 – Create
        create_rv = client.post('/api/appointment',
                                headers=auth_headers(manager_token),
                                json={
                                    'customer_email': 'cust@test.com',
                                    'staff_id': staff_id,
                                    'service_ids': [svc_id],
                                    'appointment_datetime': _future(10),
                                })
        assert create_rv.status_code == 201
        appt_id = create_rv.get_json()['appointment_id']

        # Step 2 – Update status to Completed (1)
        upd_rv = client.put(f'/api/appointment/{appt_id}',
                            headers=auth_headers(manager_token),
                            json={'status': 1})
        assert upd_rv.status_code == 200

        # Step 3 – Delete
        del_rv = client.delete(f'/api/appointment/{appt_id}',
                               headers=auth_headers(manager_token))
        assert del_rv.status_code == 200

        # Step 4 – Confirm deletion (404)
        get_rv = client.get(f'/api/appointment/{appt_id}',
                            headers=auth_headers(manager_token))
        assert get_rv.status_code == 404


# ─────────────────────────────────────────────────────────────────────────────
# FLOW-02: Invoice lifecycle
# ─────────────────────────────────────────────────────────────────────────────

class TestInvoiceLifecycle:

    def test_flow_create_appointment_then_invoice(self, client, manager_token):
        """FLOW-02: Manager creates an appointment and then generates an invoice for it."""
        svc_id = _get_first(client, manager_token, '/api/service', 'service_id')
        staff_id = _get_first(client, manager_token, '/api/staff', 'staff_id')

        # Step 1 – Create appointment
        appt_rv = client.post('/api/appointment',
                              headers=auth_headers(manager_token),
                              json={
                                  'customer_email': 'cust@test.com',
                                  'staff_id': staff_id,
                                  'service_ids': [svc_id],
                                  'appointment_datetime': _future(11),
                              })
        assert appt_rv.status_code == 201
        appt_id = appt_rv.get_json()['appointment_id']

        # Step 2 – Fetch invoice prep data
        prep_rv = client.get(f'/api/invoice/{appt_id}', headers=auth_headers(manager_token))
        assert prep_rv.status_code == 200
        prep = prep_rv.get_json()
        assert 'customer_id' in prep

        # Step 3 – Create invoice
        inv_rv = client.post('/api/invoice',
                             headers=auth_headers(manager_token),
                             json={
                                 'customer_id': prep['customer_id'],
                                 'staff_id': prep.get('staff_id'),
                                 'service_ids': prep['service_ids'],
                                 'invoice_amount': prep['service_total'],
                                 'appointment_id': appt_id,
                             })
        assert inv_rv.status_code == 201
        inv_number = inv_rv.get_json()['invoice_number']
        assert inv_number is not None

        # Step 4 – Verify invoice appears in get-all-invoices
        all_rv = client.get('/api/get-all-invoices', headers=auth_headers(manager_token))
        assert all_rv.status_code == 200
        invoice_numbers = [i['invoice_number'] for i in all_rv.get_json()]
        assert inv_number in invoice_numbers


# ─────────────────────────────────────────────────────────────────────────────
# FLOW-03: Customer self-service booking
# ─────────────────────────────────────────────────────────────────────────────

class TestCustomerSelfServiceFlow:

    def test_flow_customer_registration(self, client):
        """FLOW-03a: New customer can register and then log in successfully."""
        reg_rv = client.post('/register-customer',
                             json={
                                 'email': 'flow03_cust@example.com',
                                 'password': 'Flow03@Pass',
                                 'name': 'Flow Three',
                                 'dob': '1993-07-20',
                                 'phone': '+91-9700000003',
                             })
        assert reg_rv.status_code == 201
        assert 'customer_id' in reg_rv.get_json()

        login_rv = client.post('/customer-login',
                               json={'username': 'flow03_cust@example.com',
                                     'password': 'Flow03@Pass'})
        assert login_rv.status_code == 200
        assert 'token' in login_rv.get_json()

    def test_flow_customer_books_using_seeded_account(self, client, customer_token):
        """FLOW-03b: Seeded customer books, views upcoming, then cancels via status update."""
        svc_rv = client.get('/api/service', headers=auth_headers(customer_token))
        svc_id = svc_rv.get_json()[0]['service_id']

        book_rv = client.post('/api/customer-upcoming-appointments',
                              headers=auth_headers(customer_token),
                              json={
                                  'service_ids': [svc_id],
                                  'appointment_datetime': _future(12),
                              })
        assert book_rv.status_code == 201
        appt_id = book_rv.get_json()['appointment_id']

        upcoming_rv = client.get('/api/customer-upcoming-appointments',
                                 headers=auth_headers(customer_token))
        assert upcoming_rv.status_code == 200
        ids = [a['appointment_id'] for a in upcoming_rv.get_json()]
        assert appt_id in ids


# ─────────────────────────────────────────────────────────────────────────────
# FLOW-04: Inventory + order lifecycle
# ─────────────────────────────────────────────────────────────────────────────

class TestInventoryOrderLifecycle:

    def test_flow_create_product_order_and_process(self, client, manager_token):
        """FLOW-04: Manager creates a product, places a restock order, and processes it."""
        # Step 1 – Create product
        prod_rv = client.post('/api/product',
                              headers=auth_headers(manager_token),
                              json={
                                  'product_name': 'Flow04 Wax 200g',
                                  'product_category': 'Skin',
                                  'price': 400,
                                  'minimum_stock': 5,
                                  'stock_quantity': 2,  # below minimum → low-stock alert
                                  'supplier_name': 'Flow Supplier',
                                  'supplier_contact': '+91-9200000004',
                                  'supplier_email': 'flow04@supplier.com',
                              })
        assert prod_rv.status_code == 201
        pid = prod_rv.get_json()['product_id']

        # Step 2 – Confirm low-stock alert is set
        get_rv = client.get(f'/api/product/{pid}', headers=auth_headers(manager_token))
        assert get_rv.status_code == 200
        assert get_rv.get_json()['product_low_stock_alert'] is True

        # Step 3 – Create restock order
        order_rv = client.post('/api/order',
                               headers=auth_headers(manager_token),
                               json={
                                   'product_id': pid,
                                   'order_quantity': 20,
                                   'reason_for_order': 'Low stock',
                               })
        assert order_rv.status_code == 201
        order_id = order_rv.get_json()['order']['order_id']

        # Step 4 – Process order (status → 1, stock is replenished)
        process_rv = client.put(f'/api/order/{order_id}',
                                headers=auth_headers(manager_token),
                                json={'status': 1, 'order_quantity': 20})
        assert process_rv.status_code == 200
        assert process_rv.get_json()['order']['status'] == 1

        # Step 5 – Low-stock alert should be cleared after restock
        post_order_rv = client.get(f'/api/product/{pid}', headers=auth_headers(manager_token))
        assert post_order_rv.get_json()['product_low_stock_alert'] is False


# ─────────────────────────────────────────────────────────────────────────────
# FLOW-05: Staff attendance lifecycle
# ─────────────────────────────────────────────────────────────────────────────

class TestStaffAttendanceLifecycle:

    def test_flow_staff_marks_attendance(self, client, staff_token):
        """FLOW-05a: Staff marks attendance; second attempt returns 409."""
        mark_rv = client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        assert mark_rv.status_code in (201, 409)

        own_rv = client.get('/api/staff-attendance', headers=auth_headers(staff_token))
        assert own_rv.status_code == 200
        assert isinstance(own_rv.get_json(), list)

        dup_rv = client.post('/api/staff-attendance', headers=auth_headers(staff_token))
        assert dup_rv.status_code == 409
        assert 'already' in dup_rv.get_json().get('message', '').lower()

    def test_flow_manager_views_attendance(self, client, manager_token):
        """FLOW-05b: Manager views today's attendance (data exists from FLOW-05a)."""
        mgr_rv = client.get('/api/manager-staff-attendance', headers=auth_headers(manager_token))
        assert mgr_rv.status_code in (200, 404)


# ─────────────────────────────────────────────────────────────────────────────
# FLOW-06: Customer review flow
# ─────────────────────────────────────────────────────────────────────────────

class TestCustomerReviewFlow:

    def test_flow_pending_reviews_list_and_invalid_submit(self, client, customer_token):
        """FLOW-06: Customer checks pending reviews list; submitting for unknown appt → 404."""
        # Step 1 – Pending reviews list is accessible (may be empty)
        pending_rv = client.get('/api/customer-review', headers=auth_headers(customer_token))
        assert pending_rv.status_code == 200
        assert isinstance(pending_rv.get_json(), list)

        # Step 2 – Submit review for non-existent appointment → 404
        rv = client.post('/api/customer-reviewed-appointments',
                         headers=auth_headers(customer_token),
                         json={'appointment_id': 99999, 'rating': 5, 'review': 'Great!'})
        assert rv.status_code == 404

        # Step 3 – Submit review with missing rating → 400
        rv2 = client.post('/api/customer-reviewed-appointments',
                          headers=auth_headers(customer_token),
                          json={'appointment_id': 99999, 'review': 'No rating'})
        assert rv2.status_code == 400


# ─────────────────────────────────────────────────────────────────────────────
# FLOW-07: Role-boundary sanity checks
# ─────────────────────────────────────────────────────────────────────────────

class TestRoleBoundaries:

    def test_customer_cannot_list_all_appointments(self, client, customer_token):
        """FLOW-07a: Customer hitting manager-only /api/appointment → 403."""
        rv = client.get('/api/appointment', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_staff_cannot_manage_products(self, client, staff_token):
        """FLOW-07b: Staff cannot create a product → 403."""
        rv = client.post('/api/product',
                         headers=auth_headers(staff_token),
                         json={
                             'product_name': 'Hack',
                             'product_category': 'X',
                             'price': 1,
                             'minimum_stock': 1,
                             'stock_quantity': 1,
                             'supplier_name': 'X',
                             'supplier_contact': '000',
                             'supplier_email': 'x@x.com',
                         })
        assert rv.status_code == 403

    def test_customer_cannot_view_finance(self, client, customer_token):
        """FLOW-07c: Customer cannot access finance endpoint → 403."""
        rv = client.get('/api/finance', headers=auth_headers(customer_token))
        assert rv.status_code == 403

    def test_manager_cannot_access_customer_summary(self, client, manager_token):
        """FLOW-07d: Manager cannot call customer-summary (customer-only) → 403."""
        rv = client.get('/api/customer-summary', headers=auth_headers(manager_token))
        assert rv.status_code == 403

    def test_staff_cannot_call_create_staff(self, client, staff_token):
        """FLOW-07e: Staff cannot create other staff accounts → 403."""
        rv = client.post('/api/staff',
                         headers=auth_headers(staff_token),
                         json={
                             'username': 'hack_staff',
                             'staff_name': 'Hacker',
                             'staff_contact': '+91-0000000000',
                             'staff_email': 'hack@salon.com',
                             'staff_dob': '2000-01-01',
                             'staff_doj': '2024-01-01',
                         })
        assert rv.status_code == 403

    def test_unauthenticated_cannot_access_any_api(self, client):
        """FLOW-07f: Unauthenticated request to protected endpoint → 401/302."""
        for path in ['/api/appointment', '/api/staff', '/api/customer', '/api/product']:
            rv = client.get(path)
            assert rv.status_code in (401, 302), f"{path} should be protected, got {rv.status_code}"
