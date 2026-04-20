# Glow Suite – Test Matrix

**Framework:** pytest · **DB:** SQLite in-memory · **Auth:** Flask-Security token (`Authentication-Token` header)  
**Total tests:** ~187 passing · **Known bugs documented:** TC-SVC-09

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Passing test |
| ⚠️ | Known bug – test documents the failure |
| `+` | Positive (happy-path) case |
| `-` | Negative / error case |
| `🔒` | Access-control / role-boundary check |

---

## 1. Authentication  (`test_auth.py`)

**Endpoints:** `POST /owner-login` · `POST /manager-login` · `POST /staff-login` · `POST /customer-login` · `POST /register-customer`

| TC ID | Case | Type | Expected | File:Line |
|-------|------|------|----------|-----------|
| TC-AUTH-01 | Owner login – valid credentials | + | 200 + token + role | test_auth.py |
| TC-AUTH-02 | Owner login – wrong password | - | 400 `Wrong password` | test_auth.py |
| TC-AUTH-03 | Owner login – missing username | - | 400 | test_auth.py |
| TC-AUTH-04 | Owner login – unknown user | - | 404 | test_auth.py |
| TC-AUTH-05 | Owner login – manager using owner endpoint | 🔒 | 403 `Access denied` | test_auth.py |
| TC-AUTH-06 | Manager login – valid credentials | + | 200 + token + role | test_auth.py |
| TC-AUTH-07 | Manager login – wrong password | - | 400 | test_auth.py |
| TC-AUTH-08 | Manager login – missing password | - | 400 | test_auth.py |
| TC-AUTH-09 | Manager login – customer using manager endpoint | 🔒 | 403 | test_auth.py |
| TC-AUTH-10 | Staff login – valid credentials | + | 200 + token + role | test_auth.py |
| TC-AUTH-11 | Staff login – owner using staff endpoint | 🔒 | 403 | test_auth.py |
| TC-AUTH-12 | Staff login – unknown user | - | 404 | test_auth.py |
| TC-AUTH-13 | Customer login – valid credentials | + | 200 + token + role | test_auth.py |
| TC-AUTH-14 | Customer login – wrong password | - | 400 | test_auth.py |
| TC-AUTH-15 | Customer login – empty body | - | 400 | test_auth.py |
| TC-AUTH-16 | Register new customer – all fields | + | 201 + customer_id | test_auth.py |
| TC-AUTH-17 | Register – duplicate email | - | 400 `already exists` | test_auth.py |
| TC-AUTH-18 | Register – missing required field (phone) | - | 400 `Missing` | test_auth.py |
| TC-AUTH-19 | Register – invalid dob format | - | 400 `date format` | test_auth.py |
| TC-AUTH-20 | Register – without optional address | + | 201 | test_auth.py |

---

## 2. Change Password  (`test_changepassword.py`)

**Endpoint:** `PUT /api/change-password`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-PWD-01 | New password ≠ confirm password | - | 400 |
| TC-PWD-02 | New password identical to current | - | 400 |
| TC-PWD-03 | Empty new_password | - | 400 |
| TC-PWD-04 | Wrong current password | - | 400 |
| TC-PWD-05 | No token | 🔒 | 401/302 |
| TC-PWD-06 | Valid change – matching passwords | + | 200 *(runs last to avoid token invalidation)* |

---

## 3. Services  (`test_services.py`)

**Endpoints:** `GET /api/service` · `GET /api/service/<id>` · `POST /api/service` · `PUT /api/service/<id>` · `DELETE /api/service/<id>`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-SVC-01 | List services – manager | + | 200 list with schema fields |
| TC-SVC-02 | List services – no token | 🔒 | 401/302 |
| TC-SVC-03 | Get single service – valid ID | + | 200 + correct data |
| TC-SVC-04 | Get single service – non-existent ID | - | 404 |
| TC-SVC-05 | List services – customer role | + | 200 (customers can browse) |
| TC-SVC-06 | Create service – manager, all fields | + | 201 + service_id |
| TC-SVC-07 | Create service – customer role | 🔒 | 403 |
| TC-SVC-08 | Create service – no token | 🔒 | 401 |
| TC-SVC-09 ⚠️ | Create service – missing price | - | **BUG: returns 201 (NULL price), expected 400** |
| TC-SVC-10 | Update service price – manager | + | 200 `updated` |
| TC-SVC-11 | Update service – non-existent ID | - | 404 |
| TC-SVC-12 | Update service – staff role | 🔒 | 403 |
| TC-SVC-13 | Delete service – manager, no appointments | + | 200 `deleted` |
| TC-SVC-14 | Delete service – non-existent ID | - | 404 |

---

## 4. Staff  (`test_staff.py`, `test_staffattendance.py`, `test_managerstaffattendance.py`)

**Endpoints:** `GET/POST /api/staff` · `GET/PUT/DELETE /api/staff/<id>` · `POST/GET /api/staff-attendance` · `GET /api/manager-staff-attendance`

### 4a. Staff CRUD

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-STAFF-01 | List staff – manager | + | 200 list |
| TC-STAFF-02 | List staff – no token | 🔒 | 401/302 |
| TC-STAFF-03 | Get staff by ID | + | 200 + fields |
| TC-STAFF-04 | Get staff – non-existent ID | - | 404 |
| TC-STAFF-05 | Create staff – manager, all fields | + | 201 + staff_id |
| TC-STAFF-06 | Create staff – duplicate username | - | 409 |
| TC-STAFF-07 | Create staff – staff role | 🔒 | 403 |
| TC-STAFF-08 | Update staff – manager | + | 200 |
| TC-STAFF-09 | Delete staff – manager | + | 200 |

### 4b. Staff Attendance

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-ATTN-01 | Staff marks attendance | + | 201 on first mark |
| TC-ATTN-02 | Staff marks attendance again (duplicate) | - | 409 `already` |
| TC-ATTN-03 | Staff views own attendance | + | 200 list |
| TC-ATTN-04 | No token | 🔒 | 401/302 |

### 4c. Manager Views Attendance

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-MAR-ATTN-01 | Manager lists today's attendance | + | 200 list / 404 empty |
| TC-MAR-ATTN-02 | No token | 🔒 | 302/401 |
| TC-MAR-ATTN-03 | Manager filters by explicit today date | + | 200 / 404 |
| TC-MAR-ATTN-04 | Invalid date format | - | 400 |
| TC-MAR-ATTN-05 | Date with no records (1999-01-01) | - | 404 |
| TC-MAR-ATTN-06 | Staff role accesses manager view | 🔒 | 403 |

---

## 5. Customers  (`test_customers.py`)

**Endpoints:** `GET/POST /api/customer` · `GET/PUT/DELETE /api/customer/<id>` · `GET /api/customer-review` · `GET/POST /api/customer-reviewed-appointments`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-CUST-01 | List customers – manager | + | 200 list with schema fields |
| TC-CUST-02 | List customers – no token | 🔒 | 401/302 |
| TC-CUST-03 | Get customer by ID | + | 200 |
| TC-CUST-04 | Get customer – non-existent | - | 404 |
| TC-CUST-05 | Create customer – manager | + | 201 + customer_id |
| TC-CUST-06 | Create customer – missing email | - | 400 |
| TC-CUST-07 | Create customer – customer role | 🔒 | 403 |
| TC-CUST-08 | Update customer contact | + | 200 |
| TC-CUST-09 | Update customer – non-existent | - | 404 |
| TC-CUST-10 | Delete customer – manager | + | 200 |
| TC-CUST-11 | Pending reviews – no completed appointments | + | 200 empty list |
| TC-CUST-12 | Pending reviews – manager role | 🔒 | 403 |
| TC-CUST-13 | Reviewed appointments list | + | 200 list |
| TC-CUST-14 | Submit review – non-existent appointment | - | 404 |
| TC-CUST-15 | Submit review – missing rating | - | 400 |

---

## 6. Appointments  (`test_appointments.py`)

**Endpoints:** `GET/POST /api/appointment` · `PUT/DELETE /api/appointment/<id>` · `GET /api/todays-appointments` · `GET/POST /api/customer-upcoming-appointments` · `GET /api/customer-history-appointments` · `GET /api/customer-summary`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-APPT-01 | List appointments – manager | + | 200 list |
| TC-APPT-02 | List appointments – customer | 🔒 | 403 |
| TC-APPT-03 | List appointments – no token | 🔒 | 401/302 |
| TC-APPT-04 | Create appointment – valid email + service | + | 201 + appointment_id |
| TC-APPT-05 | Create appointment – unknown customer email | - | 404 |
| TC-APPT-06 | Create appointment – missing service_ids | - | 400 |
| TC-APPT-07 | Update appointment status to Completed | + | 200 `updated` |
| TC-APPT-08 | Delete appointment – manager | + | 200 |
| TC-APPT-09 | Delete appointment – non-existent | - | 404 |
| TC-APPT-10 | Today's appointments – manager | + | 200 list or empty dict |
| TC-APPT-11 | Today's appointments – staff | + | 200 |
| TC-APPT-12 | Today's appointments – customer | 🔒 | 403 |
| TC-APPT-13 | Customer self-books appointment | + | 201 + appointment_id |
| TC-APPT-14 | Customer books – missing service_ids | - | 400 |
| TC-APPT-15 | Customer views upcoming appointments | + | 200 list |
| TC-APPT-16 | Customer views appointment history | + | 200 list |
| TC-APPT-17 | Customer summary – all fields present | + | 200 + required fields |
| TC-APPT-18 | Customer summary – manager role | 🔒 | 403 |

---

## 7. Inventory  (`test_inventory.py`)

**Endpoints:** `GET/POST /api/product` · `GET/PUT/DELETE /api/product/<id>` · `GET/POST /api/inventory-transactions`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-INV-01 | List products – manager | + | 200 list with schema |
| TC-INV-02 | List products – no token | 🔒 | 401/302 |
| TC-INV-03 | Get product by ID | + | 200 |
| TC-INV-04 | Get product – non-existent | - | 404 |
| TC-INV-05 | Create product – manager, all fields | + | 201 + product_id |
| TC-INV-06 | Create product – customer role | 🔒 | 403 |
| TC-INV-07 | Update product stock – manager | + | 200 |
| TC-INV-08 | Restock clears low-stock alert | + | product_low_stock_alert → False |
| TC-INV-09 | Delete product with linked transactions | - | blocked (400/409) |
| TC-INV-10 | Delete product – non-existent | - | 404 |
| TC-INV-11 | List transactions – manager | + | 200 list |
| TC-INV-12 | Create transaction – staff records usage | + | 201 |
| TC-INV-13 | Create transaction – missing product_id | - | 400 |
| TC-INV-14 | Create transaction – customer role | 🔒 | 403 |
| TC-INV-15 | List transactions with date filter | + | 200 filtered list |

---

## 8. Invoices  (`test_invoice.py`)

**Endpoints:** `GET /api/invoice` · `GET/POST /api/invoice` (with appointment ID) · `GET /api/get-all-invoices`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-INVC-01 | GET /api/invoice – returns uninvoiced appointments | + | 200 list with appointment_id |
| TC-INVC-02 | GET /api/invoice – no token | 🔒 | 302/401 |
| TC-INVC-03 | GET /api/invoice – customer role | 🔒 | 403 |
| TC-INVC-04 | GET /api/invoice/<appt_id> – fetch invoice prep data | + | 200 + customer_id |
| TC-INVC-05 | POST /api/invoice – create invoice | + | 201 + invoice_number |
| TC-INVC-06 | POST /api/invoice – missing customer_id | - | 400 |
| TC-INVC-07 | GET /api/invoice/<appt_id> – existing invoice | + | 200 full record |
| TC-INVC-08 | POST /api/invoice – invalid customer | - | 404 |
| TC-INVC-09 | GET /api/invoice/<appt_id> – appointment not found | - | 404 |

---

## 9. Orders  (`test_orders.py`)

**Endpoints:** `GET/POST /api/order` · `GET/PUT/DELETE /api/order/<id>`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-ORD-01 | List orders – manager | + | 200 list |
| TC-ORD-02 | List orders – no token | 🔒 | 401/302 |
| TC-ORD-03 | Create order – valid product | + | 201 + order.order_id |
| TC-ORD-04 | Create order – customer role | 🔒 | 403 |
| TC-ORD-05 | Create order – missing product_id | - | 400 |
| TC-ORD-06 | Get order by ID | + | 200 |
| TC-ORD-07 | Get order – non-existent | - | 404 |
| TC-ORD-08 | Update order status | + | 200 |
| TC-ORD-09 | Delete order – manager | + | 200 |

---

## 10. Finance  (`test_finance.py`)

**Endpoints:** `POST /api/finance` · `PUT /api/finance` · `GET /api/finance`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-FIN-01 | Generate report – manager, valid date | + | 201 with all revenue fields |
| TC-FIN-02 | Generate report – missing last_date | - | 400 |
| TC-FIN-03 | Update overheads – manager | + | 200 + updated values |
| TC-FIN-04 | Finance endpoint – staff role | 🔒 | 403 |
| TC-FIN-05 | Finance endpoint – no token | 🔒 | 302/401 |
| TC-FIN-06 | List reports – manager | + | 200 list |

---

## 11. Managers  (`test_managers.py`)

**Endpoints:** `POST /api/create-manager` · `GET /api/manager` · `GET/PUT/DELETE /api/manager/<id>`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-MGR-01 | Create manager – owner, all fields | + | 200/201 + username |
| TC-MGR-02 | Create manager – duplicate username | - | 409 |
| TC-MGR-03 | Create manager – missing username | - | 400 |
| TC-MGR-04 | Create manager – missing password | - | 400 |
| TC-MGR-05 | Create manager – manager role | 🔒 | 403 |
| TC-MGR-06 | Create manager – no token | 🔒 | 401/302 |
| TC-MGR-07 | List managers – owner | + | 200 list with schema fields |
| TC-MGR-08 | List managers – manager role | + | 200 |
| TC-MGR-09 | Get manager by ID – owner | + | 200 + manager_id |
| TC-MGR-10 | Get manager – non-existent | - | 404 |
| TC-MGR-11 | Update manager branch – owner | + | 200 `updated` |
| TC-MGR-12 | Update manager – non-existent | - | 404 |
| TC-MGR-13 | Delete manager – owner | + | 200 `deleted` |
| TC-MGR-14 | Delete manager – non-existent | - | 404 |

---

## 12. Salon Config  (`test_salonconfig.py`)

**Endpoint:** `GET/PUT /api/salon-config`

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-CFG-01 | Get salon config – manager | + | 200 |
| TC-CFG-02 | Update salon config – manager | + | 200 |
| TC-CFG-03 | Config – no token | 🔒 | 401/302 |

---

## 13. AI Endpoints  (`test_ai.py`)

**Endpoints:** `POST /ai/manager-chat` · `GET /ai/daily-briefing` · `POST /ai/report-intent` · `POST /ai/customer-chat`  
*All AI calls are stubbed via `unittest.mock.patch('anthropic.Anthropic', ...)`*

| TC ID | Case | Type | Expected |
|-------|------|------|----------|
| TC-AI-01 | Manager chat – valid message | + | 200 + response string |
| TC-AI-02 | Manager chat – with conversation history | + | 200 + response |
| TC-AI-03 | Manager chat – empty message | - | 400 |
| TC-AI-04 | Manager chat – missing message field | - | 400 |
| TC-AI-05 | Manager chat – customer role | 🔒 | 403 |
| TC-AI-06 | Manager chat – no token | 🔒 | 401/302 |
| TC-AI-07 | Daily briefing – manager | + | 200 non-empty dict |
| TC-AI-08 | Daily briefing – staff role | 🔒 | 403 |
| TC-AI-09 | Daily briefing – no token | 🔒 | 401/302 |
| TC-AI-10 | Report intent – valid message | + | 200/201/422 |
| TC-AI-11 | Report intent – missing message | - | 400 |
| TC-AI-12 | Report intent – customer role | 🔒 | 403 |
| TC-AI-13 | Customer chat – valid message | + | 200 + response |
| TC-AI-14 | Customer chat – empty message | - | 400 |
| TC-AI-15 | Customer chat – manager role | 🔒 | 403 |

---

## 14. Integration Flows  (`test_integration.py`)

End-to-end journeys that span multiple endpoints to verify data flows correctly between steps.

| Flow ID | Description | Steps |
|---------|-------------|-------|
| **FLOW-01** | **Full appointment lifecycle** | Manager creates appt → updates status to Completed → deletes → GET confirms 404 |
| **FLOW-02** | **Invoice lifecycle** | Manager creates appt → GET invoice prep data → POST invoice → verify in GET /api/get-all-invoices |
| **FLOW-03a** | **Customer registration** | POST /register-customer → POST /customer-login → token present |
| **FLOW-03b** | **Customer self-service booking** | Seeded customer books via POST → GET upcoming → appointment_id in list |
| **FLOW-04** | **Inventory + order lifecycle** | Create product (stock < min) → confirm low_stock_alert=True → POST order → PUT order (processed) → confirm alert cleared |
| **FLOW-05a** | **Staff attendance mark** | POST attendance → 201 → duplicate POST → 409 `already` |
| **FLOW-05b** | **Manager views attendance** | GET /api/manager-staff-attendance → 200/404 |
| **FLOW-06** | **Customer review flow** | GET pending reviews → POST review for non-existent appt → 404; POST without rating → 400 |
| **FLOW-07a** | **Role boundary – customer** | Customer GET /api/appointment → 403 |
| **FLOW-07b** | **Role boundary – staff** | Staff POST /api/product → 403 |
| **FLOW-07c** | **Role boundary – customer/finance** | Customer GET /api/finance → 403 |
| **FLOW-07d** | **Role boundary – manager/customer** | Manager GET /api/customer-summary → 403 |
| **FLOW-07e** | **Role boundary – staff/create-staff** | Staff POST /api/staff → 403 |
| **FLOW-07f** | **Unauthenticated sweep** | GET /api/appointment, /api/staff, /api/customer, /api/product → all 401/302 |

---

## Summary

| Module | Tests | Pass | Known Bugs |
|--------|-------|------|------------|
| Authentication | 20 | 20 | — |
| Change Password | 6 | 6 | — |
| Services | 14 | 13 | TC-SVC-09 (missing price validation) |
| Staff + Attendance | 15 | 15 | — |
| Customers | 15 | 15 | — |
| Appointments | 18 | 18 | — |
| Inventory | 15 | 15 | — |
| Invoices | 9 | 9 | — |
| Orders | 9 | 9 | — |
| Finance | 6 | 6 | — |
| Managers | 14 | 14 | — |
| Salon Config | 3 | 3 | — |
| AI Endpoints | 15 | 15 | — |
| Integration Flows | 14 | 14 | — |
| **Total** | **~187** | **~186** | **1** |

### Known Bug: TC-SVC-09

**Endpoint:** `POST /api/service`  
**Condition:** `service_price` omitted from request body  
**Actual:** 201 Created (NULL price stored in DB)  
**Expected:** 400 Bad Request  
**Fix:** Add `if not data.get('service_price'): return {'message': 'service_price is required'}, 400` in `ServiceResource.post()`.

---

## Running the Suite

```bash
# From backend/ directory
pytest tests/ -v

# Run a single module
pytest tests/test_auth.py -v

# Run integration flows only
pytest tests/test_integration.py -v

# Run with coverage
pytest tests/ --cov=application --cov-report=term-missing
```
